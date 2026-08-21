#!/usr/bin/env python3
"""
Restore modification times on unchanged build output.

Hugo rewrites every generated file on every build, so page-bundle resources get
a fresh mtime even when their bytes are identical, which makes rsync's default
size+mtime quick check useless for deployment. Stamping unchanged files back to
their previous mtime means mtime moves if and only if content moved, so a plain
`rsync -a --delete` is both fast and correct.

Only files whose size or mtime moved since the last run are read; Hugo already
preserves mtimes for `static/` files, so the climbing videos never get hashed.
Run after every build step that writes into public/.

The manifest lives in .cache/ (gitignored); deleting it costs one slower run.
"""

import hashlib
import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).parent.parent
PUBLIC = ROOT / "public"
MANIFEST = ROOT / ".cache" / "mtimes.json"


def digest(path: Path) -> str:
    """SHA-256 of a file."""
    with open(path, "rb") as f:
        return hashlib.file_digest(f, "sha256").hexdigest()


def load_manifest() -> dict[str, list]:
    try:
        return json.loads(MANIFEST.read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def main() -> int:
    if not PUBLIC.is_dir():
        print(f"ERROR: {PUBLIC} does not exist; build first.", file=sys.stderr)
        return 1

    manifest = load_manifest()

    # Matching size and mtime means the file cannot have changed, so it never
    # has to be read.
    untouched: dict[str, list] = {}
    candidates: list[tuple[str, Path, os.stat_result]] = []
    for path in PUBLIC.rglob("*"):
        if path.is_symlink() or not path.is_file():
            continue
        rel = str(path.relative_to(PUBLIC))
        st = path.stat()
        entry = manifest.get(rel)
        if entry and entry[0] == st.st_size and entry[1] == st.st_mtime_ns:
            untouched[rel] = entry
        else:
            candidates.append((rel, path, st))

    with ThreadPoolExecutor() as pool:
        digests = list(pool.map(lambda c: digest(c[1]), candidates))

    restored = 0
    moved: dict[str, list] = {}
    for (rel, path, st), sha in zip(candidates, digests):
        entry = manifest.get(rel)
        if entry and entry[2] == sha:
            # Rewritten byte-for-byte identically: put the old mtime back.
            os.utime(path, ns=(st.st_atime_ns, entry[1]))
            moved[rel] = entry
            restored += 1
        else:
            moved[rel] = [st.st_size, st.st_mtime_ns, sha]

    # Rebuilding from what we just walked also prunes deleted files.
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(json.dumps(untouched | moved))

    print(
        f"Restored mtimes on {restored} unchanged files "
        f"({len(candidates) - restored} changed, {len(untouched)} not re-read)."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
