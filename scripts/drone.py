#!/usr/bin/env python3
"""
Drone journal: `add [place]` registers recordings in sources/, `build` splices
each clip's cuts into a video and folds it into drone.yaml.
"""

import argparse
import datetime
import math
import os
import re
import sys
from pathlib import Path
from typing import NoReturn

import yaml

from video_common import (
    allocate_sequence,
    file_key,
    find_todos,
    generate_poster,
    load_yaml,
    probe,
    require_frames,
    require_tools,
    run,
    slugify,
    video_stream,
)

SCRIPT_DIR = Path(__file__).parent
HUGO_ROOT = SCRIPT_DIR.parent
DATA_DIR = HUGO_ROOT / "data" / "drone"
STATIC_DIR = HUGO_ROOT / "static" / "drone"

DRONE_YAML = DATA_DIR / "drone.yaml"
PLACES_YAML = DATA_DIR / "places.yaml"
VIDEOS_FOLDER = STATIC_DIR / "videos"
SOURCES_FOLDER = VIDEOS_FOLDER / "sources"

SOURCE_EXTENSIONS = (".mp4", ".mov", ".avi")

# PyYAML drops comments, so the header is re-emitted on every save.
DRONE_YAML_HEADER = """\
# Drone journal, written by scripts/drone.py (see `add` / `build`).
# Rendered by layouts/shortcodes/drone-journal.html.
#
# A flight is an optional `place` (a key of places.yaml, or an `alias` set
# there, which this script swaps for the key on its next run; leave it out for a
# spot not worth naming), an optional `note`, and a list
# of `clips`; each clip is an optional `description` plus an ordered list of
# `cuts`, spliced into one video in the order written. A cut is
# "FILE: START,END" (timestamps as SS, M:SS or H:MM:SS), a range of a recording
# in static/drone/videos/sources/. Either side may be left empty to run from the
# start (",19") or to the end ("1:50,") of the recording.
#
#   clips:
#   - description: low pass over the dam, then the return
#     cuts:
#     - VID00004.AVI: 0:12,0:31
#     - VID00005.AVI: 0,10
#
# Flights are keyed by date. A day with several flights numbers them
# `YYYY-MM-DD-1`, `YYYY-MM-DD-2`, ...; `add` does that itself, renaming the bare
# date to `-1` when a second place is flown that day. The number is only part of
# the key (and the page anchor), never of the filenames.
#
# `add` seeds one clip per new recording spanning its whole length: trim it,
# split it, or merge it into another. `build` cuts every clip of a flight,
# records them here and only then deletes the recordings they used, naming each
# `<date>-<place>-<key>.mp4` with a key that ascends with the clip's position
# below, so the videos folder sorts into journal order.
"""

ENCODE_CRF = "30"
ENCODE_PRESET = "slower"
DENOISE_FILTER = "hqdn3d=4:3:2:2"
MAX_HEIGHT = 720
OUTPUT_FPS = 30
KEEP_AUDIO = False

DURATION_TOLERANCE = 0.5
# Must stay below DURATION_TOLERANCE, or a short clip would pass verification.
RANGE_EPSILON = 0.05

# `- FILE: ,19` is not valid YAML; quoted on load, unquoted on save.
OPEN_START_CUT = re.compile(r"^(\s*- \S+: )(,\S*)$", re.M)
QUOTED_OPEN_START_CUT = re.compile(r"^(\s*- \S+: )'(,[^']*)'$", re.M)


def fail(message: str) -> NoReturn:
    print(f"ERROR: {message}", file=sys.stderr)
    sys.exit(1)


# A flight key is a date, numbered `-1`, `-2`, ... only when a day has several.
FLIGHT_KEY = re.compile(r"^(\d{4}-\d{2}-\d{2})(?:-([1-9]\d*))?$")


def flight_date(key: str) -> str:
    return key[:10]


def flight_index(key: str) -> int:
    """0 for a bare date, else the flight's number within the day."""
    match = FLIGHT_KEY.match(key)
    return int(match.group(2) or 0) if match else 0


def normalized_flights(data: dict, places: dict) -> dict:
    """Flights keyed by str, validated, with place aliases swapped for keys."""
    flights = data.get("flights") or {}
    if not isinstance(flights, dict):
        fail("'flights' in drone.yaml is not a mapping of flight key -> flight")
    flights = {str(key): flight for key, flight in flights.items()}
    data["flights"] = flights

    bare: set[str] = set()
    numbered: set[str] = set()
    for key in flights:
        if not FLIGHT_KEY.match(key):
            fail(f"flight key '{key}' is not YYYY-MM-DD or YYYY-MM-DD-N")
        (numbered if flight_index(key) else bare).add(flight_date(key))
    for date in sorted(bare & numbered):
        fail(f"{date} is both a flight of its own and numbered; rename it to {date}-1")

    for key, flight in flights.items():
        place = flight.get("place") if isinstance(flight, dict) else None
        if isinstance(place, str) and place not in places:
            canonical = place_key(place, places)
            if canonical is not None:
                print(f"{key}: place '{place}' is an alias of '{canonical}'.")
                flight["place"] = canonical

    return flights


def day_flights(flights: dict, date: str) -> list[str]:
    """Keys of the flights on `date`, in flight order."""
    keys = [key for key in flights if flight_date(key) == date]
    return sorted(keys, key=flight_index)


def rename_flight(flights: dict, old: str, new: str) -> None:
    if new in flights:
        fail(f"cannot rename flight {old} to {new}: it already exists")
    renamed = {new if key == old else key: flight for key, flight in flights.items()}
    flights.clear()
    flights.update(renamed)
    print(f"renaming flight {old} to {new}.")


def choose_flight(
    flights: dict, date: str, place: str | None, index: int | None
) -> str:
    """The key new recordings of `place` on `date` go under, renaming as needed.

    Pure: `flights` is the mapping to be edited, and the chosen key may not
    exist in it yet. With no explicit `index`, the day's latest flight is reused
    when it is at the same place (so `add` can be re-run as recordings are
    dropped in); a different place starts the next flight of the day.
    """
    existing = day_flights(flights, date)

    if index is None:
        if not existing:
            return date
        latest = existing[-1]
        if flights[latest].get("place") == place:
            return latest
        index = flight_index(latest) + 1 if flight_index(latest) else 2

    if existing == [date]:
        rename_flight(flights, date, f"{date}-1")
    return f"{date}-{index}"


def parse_timestamp(value: str) -> float:
    parts = str(value).strip().split(":")
    if not 1 <= len(parts) <= 3:
        raise ValueError(f"bad timestamp '{value}'")

    seconds = 0.0
    for index, part in enumerate(parts):
        try:
            number = float(part)
        except ValueError:
            raise ValueError(f"bad timestamp '{value}'") from None
        if not math.isfinite(number) or number < 0:
            raise ValueError(f"bad timestamp '{value}'")
        if index > 0 and number >= 60:
            raise ValueError(f"bad timestamp '{value}' (minutes/seconds must be < 60)")
        seconds = seconds * 60 + number

    return seconds


def format_timestamp(seconds: float) -> str:
    minutes, seconds = divmod(seconds, 60)
    return f"{int(minutes)}:{seconds:05.2f}"


def cut_file(item) -> str:
    if not isinstance(item, dict) or len(item) != 1:
        raise ValueError(f"cut {item!r} is not of the form 'FILE: START,END'")
    return str(next(iter(item)))


def parse_cut(item, lengths: dict[str, float]) -> tuple[str, float, float]:
    file = cut_file(item)
    range_text = item[next(iter(item))]
    if file not in lengths:
        raise ValueError(f"cut refers to '{file}', which was not probed")

    start_text, separator, end_text = str(range_text).strip().partition(",")
    if not separator:
        raise ValueError(f"cut '{file}: {range_text}' is missing the START,END range")
    start = parse_timestamp(start_text) if start_text.strip() else 0.0
    end = parse_timestamp(end_text) if end_text.strip() else lengths[file]
    if end <= start:
        raise ValueError(f"cut '{file}: {range_text}' ends at or before it starts")

    return file, start, end


def parse_clip(clip, lengths: dict[str, float]) -> list[tuple[str, float, float]]:
    if not isinstance(clip, dict):
        raise ValueError(f"clip {clip!r} is not a mapping")
    cuts = clip.get("cuts")
    if not isinstance(cuts, list) or not cuts:
        raise ValueError(f"clip {describe_clip(clip)} needs a non-empty list of cuts")
    return [parse_cut(item, lengths) for item in cuts]


def describe_clip(clip: dict) -> str:
    description = clip.get("description")
    return f"'{description}'" if description else "(no description)"


def is_pending(clip) -> bool:
    return isinstance(clip, dict) and "file" not in clip and "cuts" in clip


def pending_clips(flight: dict) -> list[dict]:
    return [clip for clip in flight.get("clips") or [] if is_pending(clip)]


def clip_prefix(key: str, flight: dict) -> str:
    """Everything before the key. Date first, so the folder sorts by day."""
    place = slugify(str(flight.get("place") or "flight")) or "flight"
    return f"{flight_date(key)}-{place}"


def plan_names(key: str, flight: dict, taken: set[str]) -> list[str]:
    """A filename per pending clip, keyed so the flight sorts in list order.

    Built clips pin the keys around each pending run, so a clip added to a
    flight that was already built still lands in the right place.
    """
    prefix = clip_prefix(key, flight)
    clips = flight.get("clips") or []
    keys = [
        None if is_pending(clip) else file_key(str(clip.get("file", "")))
        for clip in clips
    ]
    allocated = allocate_sequence(keys, taken)
    return [
        f"{prefix}-{allocated[index]}.mp4"
        for index, clip in enumerate(clips)
        if is_pending(clip)
    ]


def existing_keys(folder: Path) -> set[str]:
    """Keys already on disk, so a fresh draw can never collide with one."""
    return {path.stem.rsplit("-", 1)[-1] for path in folder.glob("*.mp4")}


def known_files(data: dict) -> set[str]:
    found: set[str] = set()
    for flight in (data.get("flights") or {}).values():
        if not isinstance(flight, dict):
            continue
        for clip in flight.get("clips") or []:
            if isinstance(clip, dict):
                for cut in clip.get("cuts") or []:
                    if isinstance(cut, dict):
                        found.update(str(k) for k in cut)
    return found


def load_drone_yaml() -> dict:
    if not DRONE_YAML.exists():
        return {"flights": {}}
    text = OPEN_START_CUT.sub(r'\1"\2"', DRONE_YAML.read_text())
    return yaml.safe_load(text) or {"flights": {}}


def save_drone_yaml(data: dict) -> None:
    text = yaml.dump(data, default_flow_style=False, allow_unicode=True, width=1000)
    text = QUOTED_OPEN_START_CUT.sub(r"\1\2", text)
    DRONE_YAML.write_text(DRONE_YAML_HEADER + text)


def load_places() -> dict:
    """places.yaml, checked so no alias doubles as another place's key or alias."""
    places = load_yaml(PLACES_YAML)
    owner: dict[str, str] = {}
    for key, place in places.items():
        alias = place.get("alias") if isinstance(place, dict) else None
        for label in (str(key), alias):
            if not isinstance(label, str):
                continue
            slug = slugify(label)
            if owner.get(slug, str(key)) != str(key):
                fail(
                    f"{PLACES_YAML.name}: '{label}' names both {owner[slug]} and {key}"
                )
            owner[slug] = str(key)
    return places


def place_key(name: str, places: dict) -> str | None:
    """The key of the place `name` refers to: a key, display name or alias."""
    slug = slugify(name)
    for key in places:
        if slugify(str(key)) == slug:
            return str(key)
    for key, place in places.items():
        if not isinstance(place, dict):
            continue
        for label in (place.get("name"), place.get("alias")):
            if isinstance(label, str) and slugify(label) == slug:
                return str(key)
    return None


def resolve_place(name: str, places: dict) -> str:
    key = place_key(name, places)
    if key is None:
        fail(
            f"'{name}' is not in {PLACES_YAML.name}; add it there first "
            f"(known: {', '.join(str(k) for k in places)})"
        )
    return key


def cmd_add(args):
    require_tools("ffprobe")
    SOURCES_FOLDER.mkdir(parents=True, exist_ok=True)
    VIDEOS_FOLDER.mkdir(parents=True, exist_ok=True)

    places = load_places()
    data = load_drone_yaml()
    flights = normalized_flights(data, places)
    known = known_files(data)

    date, index = args.date or (str(datetime.date.today()), None)
    place = resolve_place(args.place, places) if args.place else None
    key: str | None = None
    added = 0

    for file in sorted(os.listdir(SOURCES_FOLDER)):
        if not file.lower().endswith(SOURCE_EXTENSIONS):
            if (SOURCES_FOLDER / file).is_file():
                print(f"ignoring {file} (not one of {', '.join(SOURCE_EXTENSIONS)}).")
            continue
        if file in known:
            print(f"skipping {file} (already referenced in drone.yaml).")
            continue

        if key is None:
            key = choose_flight(flights, date, place, index)
        flight = flights.setdefault(key, {})
        if place is not None:
            flight["place"] = place

        try:
            length = float(
                probe(SOURCES_FOLDER / file).get("format", {}).get("duration", 0)
            )
        except RuntimeError as error:
            fail(f"{file}: {error}")
        flight.setdefault("clips", []).append(
            {"cuts": [{file: f"0,{format_timestamp(length)}"}]}
        )

        print(f"adding {file} ({format_timestamp(length)}).")
        added += 1

    save_drone_yaml(data)

    if added:
        print(f"\nAdded {added} new recording(s) under {key}.")
        print(f"Edit the cuts in {DRONE_YAML}, then run `build`.")
    else:
        print("No new recordings found.")


def extract_clip(cuts: list[tuple[str, float, float]], target: Path) -> None:
    # One pass with the concat filter: stream-copying separately cut parts breaks
    # on the recorder's variable frame rate.
    command = ["ffmpeg", "-nostdin", "-y"]
    for file, start, end in cuts:
        command += [
            "-ss",
            f"{start:.3f}",
            "-t",
            f"{end - start:.3f}",
            "-i",
            str(SOURCES_FOLDER / file),
        ]

    scale = f"scale=-2:'min({MAX_HEIGHT},ih)'"
    graph = "".join(f"[{i}:v]{scale}[s{i}];" for i in range(len(cuts)))
    graph += "".join(f"[s{i}]" for i in range(len(cuts)))
    graph += f"concat=n={len(cuts)}:v=1:a=0,{DENOISE_FILTER}[v]"

    command += [
        "-filter_complex",
        graph,
        "-map",
        "[v]",
        # Strip the take-off GPS.
        "-map_metadata",
        "-1",
        "-map_chapters",
        "-1",
        "-c:v",
        "libx264",
        "-crf",
        ENCODE_CRF,
        "-preset",
        ENCODE_PRESET,
        "-pix_fmt",
        "yuv420p",
        "-r",
        str(OUTPUT_FPS),
        "-fps_mode",
        "cfr",
        "-movflags",
        "+faststart",
    ]
    if KEEP_AUDIO:
        audio = "".join(f"[{i}:a]" for i in range(len(cuts)))
        command[command.index("-filter_complex") + 1] = (
            graph + f";{audio}concat=n={len(cuts)}:v=0:a=1[a]"
        )
        command += ["-map", "[a]", "-c:a", "aac", "-b:a", "96k"]
    else:
        command += ["-an"]
    command += [str(target)]

    run(command, target, label=target.name)


def verify_clip(path: Path, expected_duration: float) -> None:
    # ffmpeg exits 0 on a zero-frame output, and the recording is deleted after.
    require_frames(path, path.name)

    duration = float(probe(path).get("format", {}).get("duration", 0))
    if abs(duration - expected_duration) > DURATION_TOLERANCE:
        raise RuntimeError(
            f"'{path.name}' is {duration:.2f}s, expected {expected_duration:.2f}s"
        )


def process_flight(
    key: str, flight: dict, cuts_by_clip: list[list], names: list[str]
) -> list[dict]:
    """All-or-nothing: any failure removes every file this call created."""
    staged: list[tuple[Path, Path, dict]] = []
    created: list[Path] = []
    try:
        clips = [clip for clip in flight["clips"] if is_pending(clip)]
        for clip, cuts, name in zip(clips, cuts_by_clip, names, strict=True):
            duration = sum(end - start for _, start, end in cuts)

            final_path = VIDEOS_FOLDER / name
            temp_path = VIDEOS_FOLDER / f"tmp_{final_path.name}"
            created.append(temp_path)

            print(f"clip {describe_clip(clip)}:", flush=True)
            for file, start, end in cuts:
                print(f"  {file} [{start:g}s-{end:g}s]", flush=True)
            extract_clip(cuts, temp_path)
            verify_clip(temp_path, duration)

            entry: dict = {"file": final_path.name}
            if clip.get("description"):
                entry["description"] = clip["description"]
            staged.append((temp_path, final_path, entry))

        for temp_path, final_path, _ in staged:
            os.rename(temp_path, final_path)
            created.append(final_path)
            created.append(generate_poster(final_path))
    except BaseException:
        for path in created:
            path.unlink(missing_ok=True)
        raise

    return [entry for _, _, entry in staged]


def validate_flight(key: str, flight: dict, places: dict) -> list[list] | None:
    todos = find_todos(flight)
    if todos:
        print(f"WARNING: skipping {key}, it still contains placeholders:")
        for todo in todos:
            print(f"  - {todo}")
        return None

    place = flight.get("place")
    if place is not None and place not in places:
        fail(f"{key}: place '{place}' is not in {PLACES_YAML.name}")

    clips = pending_clips(flight)
    files: list[str] = []
    for clip in clips:
        cuts = clip.get("cuts")
        if not isinstance(cuts, list) or not cuts:
            fail(f"{key}: clip {describe_clip(clip)} needs a non-empty list of cuts")
        for item in cuts:
            try:
                file = cut_file(item)
            except ValueError as error:
                fail(f"{key}: {error}")
            if file not in files:
                files.append(file)

    lengths: dict[str, float] = {}
    sizes: dict[str, tuple[int, int]] = {}
    for file in files:
        source_path = SOURCES_FOLDER / file
        if not source_path.exists():
            fail(f"{key}: nonexistent recording '{file}'")
        try:
            lengths[file] = float(
                probe(source_path).get("format", {}).get("duration", 0)
            )
            stream = video_stream(source_path)
            sizes[file] = (int(stream["width"]), int(stream["height"]))
        except RuntimeError as error:
            fail(f"{key}: {file}: {error}")

    cuts_by_clip: list[list] = []
    for clip in clips:
        try:
            cuts = parse_clip(clip, lengths)
        except ValueError as error:
            fail(f"{key}: {error}")
        cuts_by_clip.append(cuts)
        if len({sizes[file] for file, _, _ in cuts}) > 1:
            fail(
                f"{key}: clip {describe_clip(clip)} mixes recordings of different "
                "resolutions: "
                + ", ".join(
                    f"{file} {sizes[file][0]}x{sizes[file][1]}" for file, _, _ in cuts
                )
            )
        for file, _, end in cuts:
            if end > lengths[file] + RANGE_EPSILON:
                fail(
                    f"{key}: a cut of clip {describe_clip(clip)} ends at {end:g}s "
                    f"but '{file}' is only {lengths[file]:.1f}s long"
                )

    return cuts_by_clip


def cmd_build(args):
    require_tools("ffmpeg", "ffprobe", "cwebp")

    VIDEOS_FOLDER.mkdir(parents=True, exist_ok=True)
    SOURCES_FOLDER.mkdir(parents=True, exist_ok=True)

    places = load_places()
    data = load_drone_yaml()
    flights = normalized_flights(data, places)
    pending = {
        key: flight
        for key, flight in flights.items()
        if isinstance(flight, dict) and pending_clips(flight)
    }

    if not pending:
        print("No pending flights to process.")
        return

    ready: dict[str, list[list]] = {}
    owner: dict[str, str] = {}
    for key, flight in pending.items():
        cuts_by_clip = validate_flight(key, flight, places)
        if cuts_by_clip is None:
            continue
        ready[key] = cuts_by_clip
        for file in {file for cuts in cuts_by_clip for file, _, _ in cuts}:
            if file in owner:
                fail(f"'{file}' is used by both {owner[file]} and {key}")
            owner[file] = key

    taken = existing_keys(VIDEOS_FOLDER)
    total = 0
    try:
        for key, cuts_by_clip in ready.items():
            flight = pending[key]
            used = {file for cuts in cuts_by_clip for file, _, _ in cuts}
            names = plan_names(key, flight, taken)
            taken |= {Path(name).stem.rsplit("-", 1)[-1] for name in names}
            entries = process_flight(key, flight, cuts_by_clip, names)
            built = iter(entries)

            flight["clips"] = [
                next(built) if is_pending(clip) else clip for clip in flight["clips"]
            ]
            save_drone_yaml(data)

            for file in sorted(used):
                os.remove(SOURCES_FOLDER / file)
            total += len(entries)
    except RuntimeError as error:
        print(f"\nERROR: {error}", file=sys.stderr)
        print(
            "The recordings were left in place; fix the clip and re-run.",
            file=sys.stderr,
        )
        sys.exit(1)

    print(f"\n{total} drone clip(s) generated.", flush=True)


def parse_flight_key(value: str) -> tuple[str, int | None]:
    match = FLIGHT_KEY.match(value)
    if not match:
        raise argparse.ArgumentTypeError(f"'{value}' is not YYYY-MM-DD or YYYY-MM-DD-N")
    try:
        date = str(datetime.date.fromisoformat(match.group(1)))
    except ValueError as error:
        raise argparse.ArgumentTypeError(str(error)) from None
    return date, int(match.group(2)) if match.group(2) else None


def main():
    parser = argparse.ArgumentParser(description="Drone content management")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="Register new recordings")
    add_parser.add_argument(
        "place",
        nargs="?",
        help="Place key or alias (see places.yaml); omit for a spot not worth naming",
    )
    add_parser.add_argument(
        "--date",
        type=parse_flight_key,
        help="Flight date (YYYY-MM-DD), or YYYY-MM-DD-N to target one flight of "
        "a day with several; defaults to today",
    )
    add_parser.set_defaults(func=cmd_add)

    build_parser = subparsers.add_parser("build", help="Cut clips out of recordings")
    build_parser.set_defaults(func=cmd_build)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
