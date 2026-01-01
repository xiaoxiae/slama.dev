#!/usr/bin/env python3
"""
Font subsetting script using pyftsubset.

Subsets fonts based on characters actually used in the built site.
Run after `hugo --minify` to analyze the built HTML.
"""

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
PUBLIC = ROOT / "public"
STATIC = ROOT / "static"
FA_CSS = ROOT / "static" / "assets" / "css" / "fa.min.css"


def get_html_codepoints() -> set[int]:
    """Get all unicode codepoints used in HTML files."""
    chars = set()
    for html_file in PUBLIC.rglob("*.html"):
        chars.update(html_file.read_text(encoding="utf-8", errors="ignore"))
    return {ord(c) for c in chars if ord(c) >= 0x20}


def get_fa_codepoints() -> set[int]:
    """Get codepoints for FA icons used in HTML."""
    css = FA_CSS.read_text(encoding="utf-8")
    skip = {"solid", "regular", "brands", "light", "thin", "duotone"}

    # Find all fa-* classes in HTML
    icons = set()
    for html_file in PUBLIC.rglob("*.html"):
        content = html_file.read_text(encoding="utf-8", errors="ignore")
        for match in re.finditer(r"fa-([a-z][-a-z0-9]+)", content):
            if match.group(1) not in skip:
                icons.add(match.group(1))

    # Look up each icon's codepoint in CSS
    # Pattern handles: .fa-bolt:before{...} or .fa-bolt:before,.fa-zap:before{...}
    codepoints = set()
    for icon in icons:
        match = re.search(
            rf'\.fa-{re.escape(icon)}:before[^{{]*\{{content:"\\([0-9a-fA-F]+)"\}}', css
        )
        if match:
            codepoints.add(int(match.group(1), 16))

    print(f"  FA icons: {', '.join(sorted(icons))}")
    return codepoints


def to_unicode_range(codepoints: set[int]) -> str:
    """Convert codepoints to pyftsubset unicode range format."""
    if not codepoints:
        return ""
    cps = sorted(codepoints)
    ranges, start, prev = [], cps[0], cps[0]
    for cp in cps[1:]:
        if cp == prev + 1:
            prev = cp
        else:
            ranges.append(
                f"U+{start:04X}" if start == prev else f"U+{start:04X}-{prev:04X}"
            )
            start = prev = cp
    ranges.append(f"U+{start:04X}" if start == prev else f"U+{start:04X}-{prev:04X}")
    return ",".join(ranges)


def subset_font(src: Path, dest: Path, unicodes: str):
    """Subset a font file using pyftsubset."""
    subprocess.run(
        [
            "pyftsubset",
            str(src),
            f"--unicodes={unicodes}",
            "--flavor=woff2",
            f"--output-file={dest}",
            "--layout-features=*",
            "--desubroutinize",
        ],
        check=True,
        capture_output=True,
    )


def find_fonts() -> tuple[list[tuple[Path, Path]], list[tuple[Path, Path]]]:
    """Find all woff2 fonts in static/ and their corresponding paths in public/.

    Returns (normal_fonts, fa_fonts) as lists of (src, dest) tuples.
    """
    normal, fa = [], []
    for src in STATIC.rglob("*.woff2"):
        if "KaTeX" in src.name:
            continue
        rel = src.relative_to(STATIC)
        dest = PUBLIC / rel
        if "fa-" in src.name:
            fa.append((src, dest))
        else:
            normal.append((src, dest))
    return normal, fa


def subset_fonts(fonts: list[tuple[Path, Path]], codepoints: set[int]):
    """Subset fonts to the given codepoints."""
    unicodes = to_unicode_range(codepoints)
    if not unicodes:
        return

    for src, dest in fonts:
        if not dest.exists():
            continue

        orig_size = dest.stat().st_size
        print(f"  {src.name}...", end=" ", flush=True)
        subset_font(src, dest, unicodes)

        new_size = dest.stat().st_size
        pct = (1 - new_size / orig_size) * 100 if orig_size else 0
        print(f"{orig_size // 1024}KB → {new_size // 1024}KB ({pct:.0f}%)")


def remove_unused_formats():
    """Remove non-WOFF2 fonts from output (except KaTeX)."""
    for ext in [".ttf", ".woff", ".eot"]:
        for f in PUBLIC.rglob(f"*{ext}"):
            if "KaTeX" not in f.name:
                f.unlink()


def main():
    if not PUBLIC.exists():
        print("Error: public/ not found. Run `hugo --minify` first.")
        sys.exit(1)

    normal_fonts, fa_fonts = find_fonts()
    print(f"Found {len(normal_fonts)} normal fonts, {len(fa_fonts)} FA fonts")

    print("\nScanning HTML...")
    html_codepoints = get_html_codepoints()
    fa_codepoints = get_fa_codepoints()
    print(f"  {len(html_codepoints)} text chars, {len(fa_codepoints)} FA icons")

    print("\nSubsetting normal fonts...")
    subset_fonts(normal_fonts, html_codepoints)

    print("\nSubsetting FA fonts...")
    subset_fonts(fa_fonts, fa_codepoints)

    print("\nCleaning up...")
    remove_unused_formats()

    print("\nDone!")


if __name__ == "__main__":
    main()
