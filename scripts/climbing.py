#!/usr/bin/env python3
"""
Unified climbing script for slama.dev Hugo site.

Usage:
    uv run python scripts/climbing.py add [crimp]  - Detect new videos and create YAML entries
    uv run python scripts/climbing.py build        - Convert videos and generate journal
"""

import argparse
import os
from datetime import date
from pathlib import Path
from random import choice
from string import ascii_lowercase

import yaml
from unidecode import unidecode


# Paths relative to hugo/ root
SCRIPT_DIR = Path(__file__).parent
HUGO_ROOT = SCRIPT_DIR.parent
DATA_DIR = HUGO_ROOT / "data" / "climbing"
STATIC_DIR = HUGO_ROOT / "static" / "climbing"
CONTENT_DIR = HUGO_ROOT / "content" / "climbing"

VIDEOS_YAML = DATA_DIR / "videos.yaml"
JOURNAL_YAML = DATA_DIR / "journal.yaml"
VIDEOS_FOLDER = STATIC_DIR / "videos"


def stubify(string: str) -> str:
    return unidecode(string).lower().replace(" ", "-")


def get_random_string(length: int) -> str:
    return "".join(choice(ascii_lowercase) for _ in range(length))


def cmd_add(args):
    """Detect new videos and create YAML entries."""
    config = {}
    if VIDEOS_YAML.exists():
        with open(VIDEOS_YAML) as f:
            config = yaml.safe_load(f.read()) or {}

    files = os.listdir(VIDEOS_FOLDER)
    added = 0

    for file in files:
        if file.lower().endswith((".mp4", ".avi")) and file not in config:
            full_path = VIDEOS_FOLDER / file

            if args.wall and args.wall.lower() == "crimp":
                config[file] = {
                    "date": date.fromtimestamp(os.path.getmtime(full_path)),
                    "new": None,
                    "encode": None,
                    "trim": "TODO",
                    "wall": "Crimp",
                }
            else:
                config[file] = {
                    "color": "TODO",
                    "date": date.fromtimestamp(os.path.getmtime(full_path)),
                    "new": None,
                    "encode": None,
                    "trim": "TODO",
                    "deface": None,
                    "wall": args.wall or "Boulderhaus",
                }

            kilter = file.lower().startswith("kilter")
            moon = file.lower().startswith("moon")

            if kilter or moon:
                config[file].pop("wall", None)
                config[file].pop("deface", None)
                config[file]["type"] = "kilter" if kilter else "moon"
                print(f"adding new {'Kilter' if kilter else 'Moon'} file {file}.")
            else:
                print(f"adding new file {file}.")

            added += 1

    with open(VIDEOS_YAML, "w") as f:
        f.write(yaml.dump(config))

    if added:
        print(f"\nAdded {added} new video(s). Edit {VIDEOS_YAML} to fill in details.")
    else:
        print("No new videos found.")


def cmd_build(args):
    """Convert videos and generate journal."""
    # Run climbing_videos.py
    print("=== Processing videos ===")

    # Run climbing_journal.py
    print("\n=== Generating journal ===")


def main():
    parser = argparse.ArgumentParser(description="Climbing content management")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # add command
    add_parser = subparsers.add_parser(
        "add", help="Detect new videos and create YAML entries"
    )
    add_parser.add_argument(
        "wall", nargs="?", help="Default wall name (e.g., 'crimp', 'boulderhaus')"
    )
    add_parser.set_defaults(func=cmd_add)

    # build command
    build_parser = subparsers.add_parser(
        "build", help="Convert videos and generate journal"
    )
    build_parser.set_defaults(func=cmd_build)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
