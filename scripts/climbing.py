#!/usr/bin/env python3
"""
Unified climbing script for slama.dev Hugo site.

Usage:
    uv run scripts/climbing.py add [wall]  - Add new videos to today's session
    uv run scripts/climbing.py build       - Process videos (rename, trim, encode, poster)
"""

import argparse
import os
import sys
import datetime
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict

from video_common import (
    HAS_CUDA,
    NVIDIA_LIB_PATH,
    allocate_sequence,
    collect_known_files,
    file_key,
    generate_poster,
    load_yaml,
    require_frames,
    require_tools,
    run,
    save_yaml,
    stubify,
)


# Type definitions
class VideoMetadata(BaseModel):
    """Climbing video metadata."""

    date: datetime.date | None = None
    name: str | None = None  # For outdoor routes

    sotm: bool = False  # Send of the month
    attempts: int | None = None

    type: Literal["indoor", "outdoor", "kilter", "moon", "tension"] = "indoor"
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

# Training boards, mapped to the per-session setting they're recorded with.
# Videos end up under a session key of the same name, grouped by grade instead
# of color.
BOARD_PARAMETER = {"kilter": "angle", "moon": "setup", "tension": "angle"}

# Board settings that don't need filling in by hand (the Tension Board is
# always at 40°); anything else starts as TODO.
BOARD_DEFAULT = {"tension": 40}

# Filename prefixes that mark a board video, mapped to the board type.
BOARD_PREFIX = {
    "kilter": "kilter",
    "moon": "moon",
    "tension": "tension",
    "tb": "tension",
}


def resolve_wall_name(name: str) -> str:
    """Map a wall argument to its display name from walls.yaml (crimp -> Crimp).

    Matched on the stub, so both the walls.yaml key and the display name work,
    with or without diacritics. Unknown walls just get their first letter
    capitalized.
    """
    stub = stubify(name)

    for key, wall in load_yaml(WALLS_YAML).items():
        display = wall.get("name") if isinstance(wall, dict) else None

        if stub in (stubify(key), stubify(display or "")):
            return display or key

    return name[:1].upper() + name[1:]


def cmd_add(args):
    """Add new videos to today's session in climbing.yaml."""
    data = load_yaml(CLIMBING_YAML) or {"sessions": {}, "orphaned_videos": {}}

    files = os.listdir(VIDEOS_FOLDER)
    added = 0

    known_files = collect_known_files(data)
    wall_name = resolve_wall_name(args.wall) if args.wall else "Boulderhaus"

    for file in files:
        if not file.lower().endswith((".mp4", ".avi")):
            continue

        # Skip videos already referenced anywhere (sessions or orphaned)
        if file in known_files:
            continue

        # Detect video type
        board_type = next(
            (t for p, t in BOARD_PREFIX.items() if file.lower().startswith(p)), None
        )

        today = str(datetime.date.today())
        session = data.setdefault("sessions", {}).setdefault(today, {})

        # Set wall if not already set
        if "wall" not in session and board_type is None:
            session["wall"] = wall_name

        video_entry = {
            "file": file,
            "color": "TODO",
            "new": True,
            "trim": "TODO",
        }

        if board_type:
            video_entry["type"] = board_type
            video_entry.pop("color")
            video_entry["grade"] = "TODO"
        elif wall_name == "Crimp":
            video_entry.pop("color")  # Crimp doesn't use colors
        else:
            video_entry["encode"] = True
            video_entry["deface"] = True

        session.setdefault("_pending_videos", []).append(video_entry)

        print(
            f"adding new {board_type.capitalize() + ' ' if board_type else ''}file {file}."
        )
        added += 1

    # Keep pending videos sorted by filename for stable, readable diffs
    for session in data.get("sessions", {}).values():
        if "_pending_videos" in session:
            session["_pending_videos"].sort(key=lambda v: v["file"])
    save_yaml(CLIMBING_YAML, data)

    if added:
        print(f"\nAdded {added} new video(s). Edit {CLIMBING_YAML} to fill in details.")
    else:
        print("No new videos found.")


def video_prefix(video: VideoMetadata) -> str:
    """Everything before the key. Date first, so the folder sorts by session."""
    if video.wall:
        location_stub = stubify(video.wall)
    elif video.type in BOARD_PARAMETER:
        location_stub = video.type
    elif video.location:
        location_stub = stubify(video.location)
    else:
        location_stub = "smichoff"

    if video.color is not None:
        identifier_stub = str(video.color).replace("+", "p") + "-"
    elif video.name:
        identifier_stub = stubify(video.name) + "-"
    else:
        identifier_stub = ""

    date_stub = "" if video.date is None else video.date.strftime("%Y-%m-%d") + "-"
    return date_stub + location_stub + "-" + identifier_stub


def session_files(session: dict) -> set[str]:
    """Every video already recorded in a session (pending ones excluded)."""
    return collect_known_files(
        {key: value for key, value in session.items() if key != "_pending_videos"}
    )


def plan_session_names(session: dict, videos: list[VideoMetadata]) -> list[str]:
    """A filename per new video, keyed to sort after the session's existing ones.

    Allocated across the whole session rather than per colour, so sorting a
    session's videos by name reproduces capture order even though the yaml
    splits them into colour and grade buckets.
    """
    known = [key for key in map(file_key, session_files(session)) if key is not None]
    keys = sorted(known) + [None] * len(videos)
    allocated = allocate_sequence(keys, existing_keys())[len(known) :]
    return [
        f"{video_prefix(video)}{key}.mp4"
        for video, key in zip(videos, allocated, strict=True)
    ]


def existing_keys() -> set[str]:
    """Keys already on disk, so a fresh draw can never collide with one."""
    folders = [VIDEOS_FOLDER, VIDEOS_FOLDER / "unblurred"]
    return {
        path.stem.rsplit("-", 1)[-1]
        for folder in folders
        if folder.is_dir()
        for path in folder.glob("*.mp4")
    }


def process_video(
    name: str, video: VideoMetadata, new_name: str | None = None
) -> tuple[str, VideoMetadata]:
    """Process a single video (rename, trim, encode, poster). Returns new name."""
    path = VIDEOS_FOLDER / name

    # Rename new files
    if video.new:
        print(f"parsing new climb '{name}'.", flush=True)

        video.new = None
        new_path = VIDEOS_FOLDER / new_name
        os.rename(path, new_path)
        path = new_path
        name = new_name

    tmp_path = VIDEOS_FOLDER / f"tmp_{name}"

    def produce(command: list[str], label: str, env=None) -> None:
        """Run a stage into tmp_path, or raise leaving nothing behind."""
        try:
            run(command, tmp_path, label=label, env=env)
            require_frames(tmp_path, label)
        except RuntimeError:
            tmp_path.unlink(missing_ok=True)
            raise

    # Trim
    if video.trim:
        start, end = video.trim.split(",")
        produce(
            ["ffmpeg", "-y", "-i", str(path), "-ss", start, "-to", end, str(tmp_path)],
            f"{name} (trim {video.trim})",
        )
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
        produce(
            ["ffmpeg", "-y", "-i", str(path)]
            + encode_cfg
            + rotate_cfg
            + [str(tmp_path)],
            f"{name} (encode)",
        )
        os.remove(path)
        os.rename(tmp_path, path)
        video.encode = None
        video.rotate = None

    # Deface
    if video.deface:
        deface_cmd = ["deface", str(path), "-t", "0.5", "-o", str(tmp_path)]
        deface_env = os.environ.copy()
        if NVIDIA_LIB_PATH:
            # Run detection on the GPU (onnxrt + CUDA); deface falls back to CPU
            # on its own if the CUDA provider can't be loaded.
            deface_cmd += ["--backend", "onnxrt", "--ep", "CUDAExecutionProvider"]
            existing = deface_env.get("LD_LIBRARY_PATH", "")
            deface_env["LD_LIBRARY_PATH"] = NVIDIA_LIB_PATH + (
                os.pathsep + existing if existing else ""
            )
        # Only swap files if deface actually produced output, so a failed run
        # never strands the original outside of videos/.
        try:
            produce(deface_cmd, name, env=deface_env)
        except RuntimeError as error:
            raise RuntimeError(f"{error}; leaving original in place") from error
        old_folder = VIDEOS_FOLDER / "unblurred"
        old_folder.mkdir(exist_ok=True)
        os.rename(path, old_folder / name)
        os.rename(tmp_path, path)
        video.deface = None

    generate_poster(path)

    return name, video


def cmd_build(args):
    """Process videos (rename, trim, encode, generate posters)."""
    # ffmpeg (trim/encode/poster frame) and cwebp (poster encode) are always
    # needed; bail before touching any files if they're missing. deface is
    # checked below, only when a video actually requests it.
    require_tools("ffmpeg", "cwebp")

    if not CLIMBING_YAML.exists():
        print(f"ERROR: no {CLIMBING_YAML} found, not generating.", file=sys.stderr)
        sys.exit(1)

    data = load_yaml(CLIMBING_YAML)

    # Find all pending videos and check for TODOs
    pending_count = 0
    needs_deface = False
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
            if video_entry.get("deface"):
                needs_deface = True

    if needs_deface:
        require_tools("deface")

    if pending_count == 0:
        print("No pending videos to process.")
        # Still generate posters for any videos missing them
        for session_date, session in data.get("sessions", {}).items():
            for key, val in session.items():
                if isinstance(val, dict):
                    for v in val.get("videos", []):
                        video_file = v.get("file")
                        if video_file and (VIDEOS_FOLDER / video_file).exists():
                            generate_poster(VIDEOS_FOLDER / video_file)
        return

    print(f"Processing {pending_count} pending video(s)...")

    # Flatten every pending video across all sessions into a work list;
    # assembly into the yaml happens afterwards.
    tasks = []  # (session, video_entry, VideoMetadata, new_name)
    for session_date, session in data.get("sessions", {}).items():
        wall = session.get("wall", "Smíchoff")
        session_tasks = []
        for video_entry in session.get("_pending_videos", []):
            video_type = video_entry.get("type", "indoor")
            color = video_entry.get("color")
            grade = video_entry.get("grade")
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
            session_tasks.append((session, video_entry, video))

        # Plan the whole session at once: each key has to land after the keys
        # already in the session, and the run has to stay ascending.
        names = plan_session_names(session, [video for _, _, video in session_tasks])
        tasks.extend(
            (*task, name) for task, name in zip(session_tasks, names, strict=True)
        )

    # ffmpeg already saturates all cores on a single CPU encode, so running
    # videos concurrently buys nothing on a CPU-only box; process serially in
    # their original per-session sequence.
    results = []
    for task in tasks:
        _session, video_entry, video, planned_name = task
        new_name, _ = process_video(video_entry["file"], video, planned_name)
        print(f"processed '{video_entry['file']}' -> '{new_name}'.", flush=True)
        results.append((task, new_name))

    # Assemble processed videos into their sessions (sequential and cheap).
    for (session, video_entry, _video, _planned), new_name in results:
        video_type = video_entry.get("type", "indoor")
        grade = video_entry.get("grade")

        video_ref = {"file": new_name}
        if video_entry.get("attempts"):
            video_ref["attempts"] = video_entry["attempts"]
        if video_entry.get("sotm"):
            video_ref["sotm"] = video_entry["sotm"]

        if video_type in BOARD_PARAMETER:
            board = session.setdefault(
                video_type,
                {BOARD_PARAMETER[video_type]: BOARD_DEFAULT.get(video_type, "TODO")},
            )
            grade_data = board.setdefault(grade, {"new": 0, "videos": []})
            grade_data.setdefault("videos", []).append(video_ref)
            grade_data["new"] = grade_data.get("new", 0) + 1

        else:
            # Regular indoor climbing with color
            color = video_entry.get("color") or "other"
            if color not in session:
                session[color] = {"new": 0, "videos": []}
            if "videos" not in session[color]:
                session[color]["videos"] = []
            session[color]["videos"].append(video_ref)
            session[color]["new"] = session[color].get("new", 0) + 1

    # Remove _pending_videos from every session that had them
    for session in data.get("sessions", {}).values():
        session.pop("_pending_videos", None)

    save_yaml(CLIMBING_YAML, data)
    print("climbing videos generated (and reformatted).", flush=True)


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
