#!/usr/bin/env python3
"""Shared helpers for the video-backed journals (climbing.py, drone.py)."""

import json
import os
import re
import shutil
import sys
from pathlib import Path
from random import choice
from string import ascii_lowercase
from subprocess import DEVNULL, PIPE, Popen

import yaml
from PIL import Image
from unidecode import unidecode

HAS_CUDA = shutil.which("nvidia-smi") is not None


def _nvidia_lib_path() -> str | None:
    try:
        import nvidia
    except ImportError:
        return None
    base = Path(nvidia.__file__).parent
    libs = [str(d / "lib") for d in base.iterdir() if (d / "lib").is_dir()]
    return os.pathsep.join(libs) if libs else None


NVIDIA_LIB_PATH = _nvidia_lib_path()


TOOL_HINTS = {
    "ffmpeg": "system package 'ffmpeg'",
    "ffprobe": "system package 'ffmpeg'",
    "cwebp": "system package providing cwebp (on Arch: `sudo pacman -S libwebp-utils`)",
    "deface": "project dependency (`uv sync`)",
}


def require_tools(*tools: str) -> None:
    missing = [t for t in tools if shutil.which(t) is None]
    if missing:
        print("ERROR: missing required tool(s):", file=sys.stderr)
        for t in missing:
            print(f"  - {t}: {TOOL_HINTS.get(t, 'not found on PATH')}", file=sys.stderr)
        sys.exit(1)


def _tail(errors: bytes | None, lines: int = 3) -> str:
    text = (errors or b"").decode(errors="replace").replace("\r", "\n").strip()
    if not text:
        return ""
    kept = [line for line in text.splitlines() if line.strip()]
    return "\n  " + "\n  ".join(kept[-lines:]) if kept else ""


def run(cmd: list[str], output_path: Path | None = None, *, label="", env=None) -> None:
    proc = Popen(cmd, stdin=DEVNULL, stdout=DEVNULL, stderr=PIPE, env=env)
    _, errors = proc.communicate()

    suffix = f" for '{label}'" if label else ""
    if proc.returncode != 0:
        raise RuntimeError(f"{cmd[0]} exited {proc.returncode}{suffix}{_tail(errors)}")
    if output_path is not None and not output_path.exists():
        raise RuntimeError(f"{cmd[0]} produced no output{suffix}{_tail(errors)}")


def probe(path: Path) -> dict:
    proc = Popen(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_format",
            "-show_streams",
            "-of",
            "json",
            str(path),
        ],
        stdin=DEVNULL,
        stdout=PIPE,
        stderr=DEVNULL,
    )
    out, _ = proc.communicate()
    if proc.returncode != 0:
        raise RuntimeError(f"ffprobe failed on '{path.name}'")
    return json.loads(out or "{}")


def video_stream(path: Path) -> dict:
    for stream in probe(path).get("streams", []):
        if stream.get("codec_type") == "video":
            return stream
    raise RuntimeError(f"no video stream in '{path.name}'")


def stubify(string: str) -> str:
    return unidecode(string).lower().replace(" ", "-")


def slugify(string: str) -> str:
    # Stricter than stubify, which climbing filenames depend on.
    return re.sub(r"[^a-z0-9]+", "-", unidecode(string).lower()).strip("-")


def get_random_string(length: int) -> str:
    return "".join(choice(ascii_lowercase) for _ in range(length))


def load_yaml(path: Path) -> dict:
    if not path.exists():
        return {}
    with open(path) as f:
        return yaml.safe_load(f) or {}


def save_yaml(path: Path, data: dict):
    with open(path, "w") as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, width=1000)


def collect_known_files(data) -> set[str]:
    found: set[str] = set()

    def walk(node):
        if isinstance(node, dict):
            file = node.get("file")
            if isinstance(file, str):
                found.add(file)
            for value in node.values():
                walk(value)
        elif isinstance(node, list):
            for item in node:
                walk(item)

    walk(data)
    return found


def find_todos(data) -> list[str]:
    found: list[str] = []

    def walk(node, path):
        if isinstance(node, dict):
            for key, value in node.items():
                walk(value, f"{path}.{key}" if path else str(key))
        elif isinstance(node, list):
            for i, item in enumerate(node):
                walk(item, f"{path}[{i}]")
        elif isinstance(node, str) and node.strip().upper().startswith("TODO"):
            found.append(path)

    walk(data, "")
    return found


def count_frames(path: Path) -> int:
    proc = Popen(
        [
            "ffprobe",
            "-v",
            "error",
            "-select_streams",
            "v:0",
            "-count_frames",
            "-show_entries",
            "stream=nb_read_frames",
            "-of",
            "default=nokey=1:noprint_wrappers=1",
            str(path),
        ],
        stdin=DEVNULL,
        stdout=PIPE,
        stderr=DEVNULL,
    )
    out, _ = proc.communicate()
    text = (out or b"").decode().strip()
    return int(text) if text.isdigit() else 0


def require_frames(path: Path, label: str = "") -> None:
    # ffmpeg exits 0 on a seek past the end, muxing a valid container with no frames.
    if count_frames(path) < 1:
        suffix = f" for '{label}'" if label else ""
        raise RuntimeError(
            f"produced no frames{suffix} (is the range past the end of the input?)"
        )


def generate_poster(video_path: Path, max_width: int = 720) -> Path:
    poster_webp = video_path.with_suffix(".webp")
    if poster_webp.exists():
        return poster_webp

    print(f"generating a poster for '{video_path.name}'.", flush=True)
    poster_jpeg = video_path.with_suffix(".jpeg")
    run(
        [
            "ffmpeg",
            "-i",
            str(video_path),
            "-vf",
            r"select=eq(n\,0)",
            "-vframes",
            "1",
            "-y",
            str(poster_jpeg),
        ],
        poster_jpeg,
        label=video_path.name,
    )

    with Image.open(poster_jpeg) as im:
        width, height = im.size
    new_width = min(max_width, width)
    new_height = int(height * (new_width / width))

    run(
        [
            "cwebp",
            "-q",
            "5",
            "-resize",
            str(new_width),
            str(new_height),
            str(poster_jpeg),
            "-o",
            str(poster_webp),
        ],
        poster_webp,
        label=video_path.name,
    )
    os.remove(poster_jpeg)
    return poster_webp
