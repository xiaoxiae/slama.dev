#!/usr/bin/env python3
"""
Unified climbing script for slama.dev Hugo site.

Usage:
    uv run scripts/climbing.py add [wall]  - Add new videos to today's session
    uv run scripts/climbing.py build       - Process videos (rename, trim, encode, poster)
"""

import argparse
import os
import shutil
from collections import OrderedDict
import datetime
from pathlib import Path
from random import choice
from string import ascii_lowercase
from subprocess import Popen
from typing import Literal

import yaml
from PIL import Image
from pydantic import BaseModel, ConfigDict
from unidecode import unidecode


# Type definitions
class VideoMetadata(BaseModel):
    """Climbing video metadata."""

    date: datetime.date | None = None
    name: str | None = None  # For outdoor routes

    sotm: bool = False  # Send of the month
    attempts: int | None = None

    type: Literal["indoor", "outdoor", "kilter", "moon"] = "indoor"
    wall: str | None = None
    location: str | None = None
    color: str | int | None = None

    # Processing flags (temporary)
    new: bool | None = None
    trim: str | None = None  # "start,end"
    encode: bool | None = None
    rotate: Literal["left", "right"] | None = None
    deface: bool | None = None

    model_config = ConfigDict(extra="forbid")


# Paths
SCRIPT_DIR = Path(__file__).parent
HUGO_ROOT = SCRIPT_DIR.parent
DATA_DIR = HUGO_ROOT / "data" / "climbing"
STATIC_DIR = HUGO_ROOT / "static" / "climbing"

CLIMBING_YAML = DATA_DIR / "climbing.yaml"
WALLS_YAML = DATA_DIR / "walls.yaml"
VIDEOS_FOLDER = STATIC_DIR / "videos"

# Legacy paths (for migration period)
VIDEOS_YAML = DATA_DIR / "videos.yaml"

HAS_CUDA = shutil.which("nvidia-smi") is not None


def stubify(string: str) -> str:
    return unidecode(string).lower().replace(" ", "-")


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


def cmd_add(args):
    """Add new videos to today's session in climbing.yaml."""
    # Check if we're using new or legacy format
    if CLIMBING_YAML.exists():
        data = load_yaml(CLIMBING_YAML)
        use_new_format = True
    elif VIDEOS_YAML.exists():
        # Legacy: still using videos.yaml
        data = load_yaml(VIDEOS_YAML)
        use_new_format = False
    else:
        data = {"sessions": {}, "orphaned_videos": {}}
        use_new_format = True

    files = os.listdir(VIDEOS_FOLDER)
    added = 0

    for file in files:
        if not file.lower().endswith((".mp4", ".avi")):
            continue

        full_path = VIDEOS_FOLDER / file

        if use_new_format:
            # Check if video already exists anywhere in the data
            video_exists = False
            for session in data.get("sessions", {}).values():
                for key, val in session.items():
                    if isinstance(val, dict):
                        for v in val.get("videos", []):
                            if v.get("file") == file:
                                video_exists = True
                                break
                        if not video_exists:
                            for grade, grade_data in val.items():
                                if isinstance(grade_data, dict):
                                    for v in grade_data.get("videos", []):
                                        if v.get("file") == file:
                                            video_exists = True
                                            break
            if video_exists:
                continue
        else:
            # Legacy format
            if file in data:
                continue

        # Detect video type
        is_kilter = file.lower().startswith("kilter")
        is_moon = file.lower().startswith("moon")

        if use_new_format:
            # New format: we need to mark video as needing processing
            # For now, add to a temporary processing list
            today = str(datetime.date.today())
            if "sessions" not in data:
                data["sessions"] = {}
            if today not in data["sessions"]:
                data["sessions"][today] = {}

            session = data["sessions"][today]

            # Set wall if not already set
            if "wall" not in session and not is_kilter and not is_moon:
                session["wall"] = args.wall or "Boulderhaus"

            # Add video entry under _pending_videos for processing
            if "_pending_videos" not in session:
                session["_pending_videos"] = []

            video_entry = {
                "file": file,
                "color": "TODO",
                "new": True,
                "trim": "TODO",
            }

            if is_kilter:
                video_entry["type"] = "kilter"
                video_entry.pop("color")
                video_entry["grade"] = "TODO"
            elif is_moon:
                video_entry["type"] = "moon"
                video_entry.pop("color")
                video_entry["grade"] = "TODO"
            elif args.wall and args.wall.lower() == "crimp":
                video_entry.pop("color")  # Crimp doesn't use colors
            else:
                video_entry["encode"] = True
                video_entry["deface"] = True

            session["_pending_videos"].append(video_entry)

            print(
                f"adding new {'Kilter' if is_kilter else 'Moon' if is_moon else ''} file {file}."
            )
            added += 1

        else:
            # Legacy format
            if args.wall and args.wall.lower() == "crimp":
                data[file] = {
                    "date": datetime.date.fromtimestamp(os.path.getmtime(full_path)),
                    "new": True,
                    "encode": True,
                    "trim": "TODO",
                    "wall": "Crimp",
                }
            else:
                data[file] = {
                    "color": "TODO",
                    "date": datetime.date.fromtimestamp(os.path.getmtime(full_path)),
                    "new": True,
                    "encode": True,
                    "trim": "TODO",
                    "deface": True,
                    "wall": args.wall or "Boulderhaus",
                }

            if is_kilter or is_moon:
                data[file].pop("wall", None)
                data[file].pop("deface", None)
                data[file]["type"] = "kilter" if is_kilter else "moon"
                print(f"adding new {'Kilter' if is_kilter else 'Moon'} file {file}.")
            else:
                print(f"adding new file {file}.")

            added += 1

    if use_new_format:
        save_yaml(CLIMBING_YAML, data)
        target = CLIMBING_YAML
    else:
        save_yaml(VIDEOS_YAML, data)
        target = VIDEOS_YAML

    if added:
        print(f"\nAdded {added} new video(s). Edit {target} to fill in details.")
    else:
        print("No new videos found.")


def process_video(name: str, video: VideoMetadata) -> tuple[str, VideoMetadata]:
    """Process a single video (rename, trim, encode, poster). Returns new name."""
    path = VIDEOS_FOLDER / name

    # Rename new files
    if video.new:
        print(f"parsing new climb '{name}'.", flush=True)

        if video.wall:
            location_stub = stubify(video.wall)
        elif video.type == "kilter":
            location_stub = "kilter"
        elif video.type == "moon":
            location_stub = "moon"
        elif video.location:
            location_stub = stubify(video.location)
        else:
            location_stub = "smichoff"

        random_string = get_random_string(8)

        if video.color is not None:
            color_str = str(video.color).replace("+", "p")
            identifier_stub = color_str + "-"
        elif video.name:
            identifier_stub = stubify(video.name) + "-"
        else:
            identifier_stub = ""

        new_name = (
            f"{location_stub}-"
            + identifier_stub
            + ("" if video.date is None else video.date.strftime("%Y-%m-%d") + "-")
            + random_string
            + ".mp4"
        )

        video.new = None
        new_path = VIDEOS_FOLDER / new_name
        os.rename(path, new_path)
        path = new_path
        name = new_name

    tmp_path = VIDEOS_FOLDER / f"tmp_{name}"

    # Trim
    if video.trim:
        start, end = video.trim.split(",")
        Popen(
            ["ffmpeg", "-y", "-i", str(path), "-ss", start, "-to", end, str(tmp_path)]
        ).communicate()
        os.remove(path)
        os.rename(tmp_path, path)
        video.trim = None

    # Encode/rotate
    if video.encode or video.rotate:
        encode_cfg = (
            ["-c:v", "h264_nvenc" if HAS_CUDA else "h264", "-preset", "slow"]
            if video.encode
            else []
        )
        rotate_cfg = (
            ["-vf", f"transpose={'2' if video.rotate == 'left' else '1'}"]
            if video.rotate
            else []
        )
        Popen(
            ["ffmpeg", "-y", "-i", str(path)]
            + encode_cfg
            + rotate_cfg
            + [str(tmp_path)]
        ).communicate()
        os.remove(path)
        os.rename(tmp_path, path)
        video.encode = None
        video.rotate = None

    # Deface
    if video.deface:
        Popen(["deface", str(path), "-t", "0.5", "-o", str(tmp_path)]).communicate()
        old_folder = VIDEOS_FOLDER / "unblurred"
        old_folder.mkdir(exist_ok=True)
        os.rename(path, old_folder / name)
        os.rename(tmp_path, path)
        video.deface = None

    # Generate poster
    poster_webp = VIDEOS_FOLDER / (path.stem + ".webp")
    if not poster_webp.exists():
        print(f"generating a poster for '{name}'.", flush=True)
        poster_jpeg = VIDEOS_FOLDER / (path.stem + ".jpeg")
        Popen(
            [
                "ffmpeg",
                "-i",
                str(path),
                "-vf",
                r"select=eq(n\,0)",
                "-vframes",
                "1",
                "-y",
                str(poster_jpeg),
            ]
        ).communicate()
        im = Image.open(poster_jpeg)
        width, height = im.size
        new_width = 720
        new_height = int(height * (new_width / width))
        Popen(
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
            ]
        ).communicate()
        os.remove(poster_jpeg)

    return name, video


def cmd_build(args):
    """Process videos (rename, trim, encode, generate posters)."""
    # Check which format we're using
    if VIDEOS_YAML.exists():
        # Legacy format: process videos.yaml
        print("=== Processing videos (legacy format) ===")

        config: dict[str, VideoMetadata] = {}
        with open(VIDEOS_YAML) as f:
            raw_config = yaml.safe_load(f) or {}
            for video_name, video_data in raw_config.items():
                if "name" in video_data and video_data["name"] == video_name:
                    video_data["name"] = None
                config[video_name] = VideoMetadata(**video_data)

        # Check for TODOs
        for name in config:
            video_dict = config[name].model_dump()
            for attr, value in video_dict.items():
                if value == "TODO":
                    print("ERROR: the videos.yaml file contains TODOs, not generating.")
                    return

            if not (VIDEOS_FOLDER / name).exists():
                print(f"ERROR: nonexistent video '{name}', not generating.")
                return

        # Process each video
        new_config = {}
        for name, video in config.items():
            new_name, processed_video = process_video(name, video)
            new_config[new_name] = processed_video

        # Save back
        config_dict = {
            name: video.model_dump(
                exclude_none=True,
                exclude_defaults=True,
                exclude={"new", "trim", "encode", "rotate", "deface"},
            )
            for name, video in new_config.items()
        }
        with open(VIDEOS_YAML, "w") as f:
            f.write(yaml.dump(config_dict))

        print("climbing videos generated (and reformatted).", flush=True)

        # Warn about leftover files
        files = set(os.listdir(VIDEOS_FOLDER))
        for file in files:
            if file.lower().endswith(".mp4") and file not in new_config:
                print(f"WARNING: leftover file {file}.", flush=True)

    elif CLIMBING_YAML.exists():
        print("=== Processing videos (climbing.yaml format) ===")
        data = load_yaml(CLIMBING_YAML)

        # Find all pending videos and check for TODOs
        pending_count = 0
        for session_date, session in data.get("sessions", {}).items():
            pending = session.get("_pending_videos", [])
            for video_entry in pending:
                pending_count += 1
                for key, value in video_entry.items():
                    if value == "TODO":
                        print(
                            f"ERROR: climbing.yaml contains TODOs in session {session_date}, not generating."
                        )
                        return
                if not (VIDEOS_FOLDER / video_entry["file"]).exists():
                    print(
                        f"ERROR: nonexistent video '{video_entry['file']}', not generating."
                    )
                    return

        if pending_count == 0:
            print("No pending videos to process.")
            # Still generate posters for any videos missing them
            for session_date, session in data.get("sessions", {}).items():
                for key, val in session.items():
                    if isinstance(val, dict):
                        for v in val.get("videos", []):
                            video_file = v.get("file")
                            if video_file:
                                poster_webp = VIDEOS_FOLDER / (
                                    Path(video_file).stem + ".webp"
                                )
                                if (
                                    not poster_webp.exists()
                                    and (VIDEOS_FOLDER / video_file).exists()
                                ):
                                    video = VideoMetadata()
                                    process_video(video_file, video)
            return

        print(f"Processing {pending_count} pending video(s)...")

        # Process each pending video
        for session_date, session in data.get("sessions", {}).items():
            pending = session.get("_pending_videos", [])
            if not pending:
                continue

            wall = session.get("wall", "Smíchoff")
            processed_videos = []

            for video_entry in pending:
                old_name = video_entry["file"]
                video_type = video_entry.get("type", "indoor")
                color = video_entry.get("color")
                grade = video_entry.get("grade")

                # Build VideoMetadata for processing
                video = VideoMetadata(
                    date=datetime.date.fromisoformat(session_date),
                    type=video_type,
                    wall=wall if video_type == "indoor" else None,
                    color=color if video_type == "indoor" else grade,
                    new=video_entry.get("new"),
                    trim=video_entry.get("trim"),
                    encode=video_entry.get("encode"),
                    rotate=video_entry.get("rotate"),
                    deface=video_entry.get("deface"),
                )

                new_name, processed = process_video(old_name, video)

                processed_videos.append(
                    {
                        "new_name": new_name,
                        "type": video_type,
                        "color": color,
                        "grade": grade,
                        "attempts": video_entry.get("attempts"),
                        "sotm": video_entry.get("sotm"),
                    }
                )

            # Move processed videos to their proper location in the session
            for pv in processed_videos:
                video_ref = {"file": pv["new_name"]}
                if pv.get("attempts"):
                    video_ref["attempts"] = pv["attempts"]
                if pv.get("sotm"):
                    video_ref["sotm"] = pv["sotm"]

                if pv["type"] == "kilter":
                    if "kilter" not in session:
                        session["kilter"] = {"angle": "TODO"}
                    grade = pv["grade"]
                    if grade not in session["kilter"]:
                        session["kilter"][grade] = {"new": 0, "videos": []}
                    if "videos" not in session["kilter"][grade]:
                        session["kilter"][grade]["videos"] = []
                    session["kilter"][grade]["videos"].append(video_ref)
                    session["kilter"][grade]["new"] = (
                        session["kilter"][grade].get("new", 0) + 1
                    )

                elif pv["type"] == "moon":
                    if "moon" not in session:
                        session["moon"] = {"setup": "TODO"}
                    grade = pv["grade"]
                    if grade not in session["moon"]:
                        session["moon"][grade] = {"new": 0, "videos": []}
                    if "videos" not in session["moon"][grade]:
                        session["moon"][grade]["videos"] = []
                    session["moon"][grade]["videos"].append(video_ref)
                    session["moon"][grade]["new"] = (
                        session["moon"][grade].get("new", 0) + 1
                    )

                else:
                    # Regular indoor climbing with color
                    color = pv["color"] or "other"
                    if color not in session:
                        session[color] = {"new": 0, "videos": []}
                    if "videos" not in session[color]:
                        session[color]["videos"] = []
                    session[color]["videos"].append(video_ref)
                    session[color]["new"] = session[color].get("new", 0) + 1

            # Remove _pending_videos
            del session["_pending_videos"]

        save_yaml(CLIMBING_YAML, data)
        print("climbing videos generated (and reformatted).", flush=True)

    else:
        print("ERROR: No climbing.yaml or videos.yaml found.")


def main():
    parser = argparse.ArgumentParser(description="Climbing content management")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="Add new videos")
    add_parser.add_argument("wall", nargs="?", help="Default wall name")
    add_parser.set_defaults(func=cmd_add)

    build_parser = subparsers.add_parser("build", help="Process videos")
    build_parser.set_defaults(func=cmd_build)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
