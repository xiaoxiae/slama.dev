#!/usr/bin/env python3
"""Drone journal: `add` new recordings, `build` them into clips."""

import argparse
import datetime
import math
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import NoReturn

import yaml

from drone_osd import detect_flights, profile_of
from drone_sync import MIN_COVER, describe, goggle_start, sync
from video_common import (
    allocate_sequence,
    file_key,
    find_todos,
    generate_poster,
    load_yaml,
    make_strips,
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
DRONES_YAML = DATA_DIR / "drones.yaml"
VIDEOS_FOLDER = STATIC_DIR / "videos"
SOURCES_FOLDER = VIDEOS_FOLDER / "sources"
# Action camera recordings, synced to the goggles' by drone_sync.py.
CAMERA_FOLDER = VIDEOS_FOLDER / "camera"
STRIPS_FOLDER = VIDEOS_FOLDER / "strips"
# A clip with camera footage is shown combined; these hold its two halves.
FPV_FOLDER = VIDEOS_FOLDER / "fpv"
CAM_FOLDER = VIDEOS_FOLDER / "cam"

SOURCE_EXTENSIONS = (".mp4", ".mov", ".avi")
CAMERA_EXTENSIONS = (".mp4", ".mov")
# HDZero goggles save a thumbnail next to each recording; we delete those too.
THUMBNAIL_EXTENSIONS = (".jpg", ".jpeg")

# PyYAML drops comments, so we write the header back on every save.
DRONE_YAML_HEADER = """\
# Drone journal, managed by scripts/drone.py.
#
# Flights have an optional place, note, clips, camera and discard (files to
# delete; camera/FILE for camera recordings). Clips have a drone (see
# drones.yaml) and cuts ("FILE: START,END", either side can be empty) until
# they're built, then a file, duration and size (plus fpv and cam, the two
# halves of a clip combined with camera footage). Camera maps a recording to
# the camera recordings it overlaps, by offset (camera time = its time + offset):
#
#   camera:
#     hdz_0037.mp4:
#       DJI_20261019123254_0094_D.MP4: -63.2
#
#   clips:
#   - description: low pass over the dam, then the return
#     drone: syl
#     cuts:
#     - VID00004.AVI: 0:12,0:31
#     - VID00005.AVI: 0,10
"""

ENCODE_CRF = "30"
ENCODE_PRESET = "slower"
DENOISE_FILTER = "hqdn3d=4:3:2:2"
MAX_HEIGHT = 720
OUTPUT_FPS = 30
AUDIO_BITRATE = "96k"
# The goggles record much quieter than the camera, so we even them out.
AUDIO_FILTER = (
    "asetpts=PTS-STARTPTS,loudnorm=I=-23:TP=-2,"
    "aformat=sample_rates=48000:channel_layouts=stereo"
)
# Of the combined clip's width, top right.
INSET = 1 / 3

DURATION_TOLERANCE = 0.5
# Keep this below DURATION_TOLERANCE.
RANGE_EPSILON = 0.05

# `- FILE: ,19` isn't valid YAML, so we quote it on load and unquote on save.
OPEN_START_CUT = re.compile(r"^(\s*- \S+: )(,\S*)$", re.M)
QUOTED_OPEN_START_CUT = re.compile(r"^(\s*- \S+: )'(,[^']*)'$", re.M)


def fail(message: str) -> NoReturn:
    print(f"ERROR: {message}", file=sys.stderr)
    sys.exit(1)


FLIGHT_KEY = re.compile(r"^(\d{4}-\d{2}-\d{2})(?:-([1-9]\d*))?$")


def flight_date(key: str) -> str:
    return key[:10]


def flight_index(key: str) -> int:
    match = FLIGHT_KEY.match(key)
    return int(match.group(2) or 0) if match else 0


def normalized_flights(data: dict, places: dict) -> dict:
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
    """Day's last flight if it's at the same place, otherwise a new one."""
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
    # Round first, otherwise 59.996 becomes "0:60.00".
    minutes, seconds = divmod(round(seconds, 2), 60)
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
    place = slugify(str(flight.get("place") or "flight")) or "flight"
    return f"{flight_date(key)}-{place}"


def plan_names(key: str, flight: dict, taken: set[str]) -> list[str]:
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
    return {path.stem.rsplit("-", 1)[-1] for path in folder.glob("*.mp4")}


def discarded(flight: dict) -> list[str]:
    return [str(file) for file in flight.get("discard") or []]


def camera_map(flight: dict) -> dict[str, dict[str, float]]:
    return flight.get("camera") or {}


def known_cameras(data: dict) -> set[str]:
    """Camera recordings referenced anywhere, as `camera/FILE`."""
    found: set[str] = set()
    for flight in (data.get("flights") or {}).values():
        if isinstance(flight, dict):
            found.update(d for d in discarded(flight) if d.startswith("camera/"))
            for cameras in camera_map(flight).values():
                found.update(f"camera/{camera}" for camera in cameras)
    return found


def known_files(data: dict) -> set[str]:
    found: set[str] = set()
    for flight in (data.get("flights") or {}).values():
        if not isinstance(flight, dict):
            continue
        found.update(discarded(flight))
        found.update(camera_map(flight))
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


def seed_clips(files: list[str], detect: bool) -> tuple[list[dict], list[str]]:
    """Clips with the drone read from the OSD, or TODO if it couldn't be."""
    lengths = {}
    for file in files:
        try:
            lengths[file] = float(
                probe(SOURCES_FOLDER / file).get("format", {}).get("duration", 0)
            )
        except RuntimeError as error:
            fail(f"{file}: {error}")

    whole = {
        file: {
            "cuts": [{file: f"0,{format_timestamp(lengths[file])}"}],
            "drone": "TODO",
        }
        for file in files
    }
    if not detect:
        return [whole[file] for file in files], []

    try:
        detection = detect_flights([SOURCES_FOLDER / file for file in files])
    except (RuntimeError, ValueError) as error:
        print(f"WARNING: could not find the flights ({error}); seeding whole files.")
        return [whole[file] for file in files], []

    def edge(seconds: float | None) -> str:
        return "" if seconds is None else format_timestamp(seconds)

    clips = []
    for cuts, (start, end), drone in zip(
        detection.clips, detection.spans, detection.crafts, strict=True
    ):
        clips.append(
            {
                "cuts": [
                    # YAML can't read back a value starting with a comma.
                    {file: f"{format_timestamp(low or 0)},{edge(high)}"}
                    for file, low, high in cuts
                ],
                "drone": drone or "TODO",
            }
        )
        print(
            f"flight {format_timestamp(start)}-{format_timestamp(end)} "
            f"({end - start:.0f}s, {drone or 'drone unread'}): "
            f"{', '.join(file for file, _, _ in cuts)}"
        )
    flown = sum(end - start for start, end in detection.spans)
    print(
        f"{len(clips)} flight(s), {format_timestamp(flown)} of "
        f"{format_timestamp(sum(lengths.values()))} recorded"
        + (f"; dropped {detection.short} too short to count" if detection.short else "")
        + (
            f"; dropped {detection.still} held still (in hand)"
            if detection.still
            else ""
        )
        + "."
    )

    for file in detection.unread:
        print(f"WARNING: no OSD readable in {file} (OSD off?); seeding it whole.")
        clips.append(whole[file])
    if detection.discard:
        print(f"no flight in (to discard): {', '.join(detection.discard)}")
    return clips, detection.discard


def cmd_add(args):
    require_tools("ffmpeg", "ffprobe")
    SOURCES_FOLDER.mkdir(parents=True, exist_ok=True)
    VIDEOS_FOLDER.mkdir(parents=True, exist_ok=True)

    places = load_places()
    data = load_drone_yaml()
    flights = normalized_flights(data, places)
    known = known_files(data)

    date, index = args.date or (str(datetime.date.today()), None)
    place = resolve_place(args.place, places) if args.place else None

    files = sorted(os.listdir(SOURCES_FOLDER))
    recordings = {
        Path(file).stem for file in files if file.lower().endswith(SOURCE_EXTENSIONS)
    }
    new: list[str] = []
    thumbnails: list[str] = []
    for file in files:
        if file in known:
            print(f"skipping {file} (already referenced in drone.yaml).")
            continue
        if (
            file.lower().endswith(THUMBNAIL_EXTENSIONS)
            and Path(file).stem in recordings
        ):
            thumbnails.append(file)
            continue
        if not file.lower().endswith(SOURCE_EXTENSIONS):
            if (SOURCES_FOLDER / file).is_file():
                print(f"ignoring {file} (not one of {', '.join(SOURCE_EXTENSIONS)}).")
            continue
        print(f"adding {file}.")
        new.append(file)

    if not new:
        save_drone_yaml(data)
        print("No new recordings found.")
        return

    previous = previous_chunk(new[0])
    if previous in known:
        print(
            f"WARNING: {new[0]} continues {previous}, which was added before; "
            "a flight running across the two will have been split in half."
        )

    known_camera = known_cameras(data)
    listed = sorted(os.listdir(CAMERA_FOLDER)) if CAMERA_FOLDER.is_dir() else []
    cameras = [
        file
        for file in listed
        if file.lower().endswith(CAMERA_EXTENSIONS)
        and f"camera/{file}" not in known_camera
    ]
    synced = None
    if cameras:
        print(f"syncing to {len(cameras)} camera recording(s)...", flush=True)
        synced = sync(
            [SOURCES_FOLDER / file for file in new],
            [CAMERA_FOLDER / file for file in cameras],
        )
        print("\n".join(describe(synced)))

    days: dict[str, list[str]] = {}
    for file in new:
        day = date
        if synced is not None and synced.clock is not None:
            start = goggle_start(SOURCES_FOLDER / file) + synced.clock
            day = str(datetime.datetime.fromtimestamp(start).date())
            if args.date and day != date:
                fail(f"{file} is from {day} by the camera, not {date}")
        days.setdefault(day, []).append(file)

    keys = []
    for day, group in days.items():
        key = choose_flight(flights, day, place, index if day == date else None)
        keys.append(key)
        flight = flights.setdefault(key, {})
        if place is not None:
            flight["place"] = place
        clips, discard = seed_clips(group, not args.no_detect)
        stems = {Path(file).stem for file in group}
        ours = [file for file in thumbnails if Path(file).stem in stems]
        if ours:
            print(f"thumbnails (to discard): {', '.join(ours)}")
        discard += ours
        if synced is not None:
            offsets = {f: synced.offsets[f] for f in group if f in synced.offsets}
            if offsets:
                flight["camera"] = camera_map(flight) | offsets
        flight.setdefault("clips", []).extend(clips)
        if discard:
            flight["discard"] = discarded(flight) + discard

    if synced is not None and synced.unused:
        print(f"no flight on camera (to discard): {', '.join(synced.unused)}")
        unused = [f"camera/{file}" for file in synced.unused]
        flight["discard"] = discarded(flight) + unused

    save_drone_yaml(data)
    print(f"\nAdded {len(new)} new recording(s) under {', '.join(keys)}.")
    print(f"Check the cuts in {DRONE_YAML}, then run `build`.")


def previous_chunk(file: str) -> str | None:
    match = re.fullmatch(r"(.*?)(\d+)(\.\w+)", file)
    if not match or int(match.group(2)) == 0:
        return None
    prefix, number, suffix = match.groups()
    return f"{prefix}{int(number) - 1:0{len(number)}d}{suffix}"


@dataclass
class Segment:
    """A piece of a clip: a stretch of one recording, and of the camera's if it
    was running."""

    file: str
    start: float
    end: float
    camera: str | None = None
    camera_start: float = 0.0


def clip_segments(
    cuts: list[tuple[str, float, float]],
    camera: dict[str, dict[str, float]],
    camera_lengths: dict[str, float],
) -> list[Segment]:
    segments = []
    for file, start, end in cuts:
        covered = []
        for recording, offset in (camera.get(file) or {}).items():
            low = max(start, -offset)
            high = min(end, camera_lengths[recording] - offset)
            if high - low >= MIN_COVER:
                covered.append((low, high, recording, offset))
        at = start
        for low, high, recording, offset in sorted(covered):
            low = max(low, at)
            if high - low < MIN_COVER:
                continue
            if low > at:
                segments.append(Segment(file, at, low))
            segments.append(Segment(file, low, high, recording, low + offset))
            at = high
        if end > at:
            segments.append(Segment(file, at, end))
    return segments


def has_audio(path: Path) -> bool:
    streams = probe(path).get("streams", [])
    return any(stream.get("codec_type") == "audio" for stream in streams)


def camera_canvas(segments: list[Segment]) -> tuple[int, int] | None:
    """The combined clip's size: the camera's aspect, at most MAX_HEIGHT."""
    recording = next((s.camera for s in segments if s.camera), None)
    if recording is None:
        return None
    stream = video_stream(CAMERA_FOLDER / recording)
    width, height = int(stream["width"]), int(stream["height"])
    out = min(MAX_HEIGHT, height)
    return round(out * width / height / 2) * 2, out


def extract_clip(segments: list[Segment], targets: dict[str, Path]) -> None:
    """Encode `file` (and with the camera, `fpv` and `cam`) in one go.

    Stream-copying breaks on variable frame rate, so we re-encode."""
    command = ["ffmpeg", "-nostdin", "-y"]
    inputs = 0

    def add_input(*args: str) -> int:
        nonlocal inputs
        command.extend(args)
        inputs += 1
        return inputs - 1

    picture = profile_of(SOURCES_FOLDER / segments[0].file).picture
    canvas = camera_canvas(segments)
    graph: list[str] = []
    parts: dict[str, list[str]] = {"file": [], "fpv": [], "cam": []}
    for i, segment in enumerate(segments):
        length = f"{segment.end - segment.start:.3f}"
        source = SOURCES_FOLDER / segment.file
        dvr = add_input("-ss", f"{segment.start:.3f}", "-t", length, "-i", str(source))
        audio = f"[{dvr}:a:0]"
        if not has_audio(source):
            silence = f"anullsrc=r=48000:cl=stereo:d={length}"
            audio = f"[{add_input('-f', 'lavfi', '-i', silence)}:a]"
        graph.append(
            f"[{dvr}:v:0]setpts=PTS-STARTPTS,{picture}"
            f"scale=-2:'min({MAX_HEIGHT},ih)',{DENOISE_FILTER},fps={OUTPUT_FPS},"
            f"setsar=1,format=yuv420p[d{i}]"
        )
        graph.append(f"{audio}{AUDIO_FILTER}[da{i}]")
        if canvas is None:
            parts["file"].append(f"[d{i}][da{i}]")
            continue

        width, height = canvas
        graph.append(f"[d{i}]split[f{i}][dv{i}]")
        graph.append(f"[da{i}]asplit[fa{i}][dva{i}]")
        parts["fpv"].append(f"[f{i}][fa{i}]")
        if segment.camera is None:
            graph.append(
                f"[dv{i}]scale={width}:{height}:force_original_aspect_ratio=decrease,"
                f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2,setsar=1[v{i}]"
            )
            parts["file"].append(f"[v{i}][dva{i}]")
            continue

        graph.append(f"[dva{i}]anullsink")
        camera = add_input(
            "-ss",
            f"{segment.camera_start:.3f}",
            "-t",
            length,
            "-i",
            str(CAMERA_FOLDER / segment.camera),
        )
        inset = round(width * INSET / 2) * 2
        graph += [
            f"[{camera}:v:0]setpts=PTS-STARTPTS,scale={width}:{height},"
            f"fps={OUTPUT_FPS},setsar=1,format=yuv420p,split[c{i}][cv{i}]",
            f"[{camera}:a:0]{AUDIO_FILTER},asplit[ca{i}][cva{i}]",
            f"[dv{i}]scale={inset}:-2[i{i}]",
            f"[cv{i}][i{i}]overlay=W-w:0[v{i}]",
        ]
        parts["file"].append(f"[v{i}][cva{i}]")
        parts["cam"].append(f"[c{i}][ca{i}]")

    encode = [
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
        "-c:a",
        "aac",
        "-b:a",
        AUDIO_BITRATE,
        "-movflags",
        "+faststart",
    ]
    outputs = []
    for name, pieces in parts.items():
        if pieces:
            n = len(pieces)
            graph.append("".join(pieces) + f"concat=n={n}:v=1:a=1[{name}v][{name}a]")
            outputs += ["-map", f"[{name}v]", "-map", f"[{name}a]", *encode]
            outputs.append(str(targets[name]))

    command += ["-filter_complex", ";".join(graph), *outputs]
    run(command, targets["file"], label=targets["file"].name)


def verify_clip(path: Path, expected_duration: float) -> float:
    # ffmpeg can exit 0 with no frames written, and we delete the source after.
    require_frames(path, path.name)

    duration = float(probe(path).get("format", {}).get("duration", 0))
    if abs(duration - expected_duration) > DURATION_TOLERANCE:
        raise RuntimeError(
            f"'{path.name}' is {duration:.2f}s, expected {expected_duration:.2f}s"
        )
    return duration


def process_flight(
    key: str, flight: dict, segments_by_clip: list[list[Segment]], names: list[str]
) -> list[dict]:
    staged: list[tuple[Path, Path]] = []
    entries: list[dict] = []
    created: list[Path] = []
    try:
        clips = pending_clips(flight)
        for clip, segments, name in zip(clips, segments_by_clip, names, strict=True):
            duration = sum(s.end - s.start for s in segments)
            covered = sum(s.end - s.start for s in segments if s.camera)
            folders = {"file": VIDEOS_FOLDER}
            if covered:
                folders |= {"fpv": FPV_FOLDER, "cam": CAM_FOLDER}
            targets = {}
            for kind, folder in folders.items():
                folder.mkdir(parents=True, exist_ok=True)
                targets[kind] = folder / f"tmp_{name}"
                created.append(targets[kind])

            print(f"clip {describe_clip(clip)}:", flush=True)
            for s in segments:
                camera = f" + {s.camera} [{s.camera_start:g}s-]" if s.camera else ""
                print(f"  {s.file} [{s.start:g}s-{s.end:g}s]{camera}", flush=True)
            extract_clip(segments, targets)
            measured = verify_clip(targets["file"], duration)
            if covered:
                verify_clip(targets["fpv"], duration)
                verify_clip(targets["cam"], covered)

            stream = video_stream(targets["file"])
            entry: dict = {
                "file": name,
                "duration": round(measured),
                "drone": clip["drone"],
                "size": f"{stream['width']}x{stream['height']}",
            }
            if covered:
                entry |= {"fpv": f"fpv/{name}", "cam": f"cam/{name}"}
            if clip.get("description"):
                entry["description"] = clip["description"]
            entries.append(entry)
            staged += [(path, path.with_name(name)) for path in targets.values()]

        for temp_path, final_path in staged:
            os.rename(temp_path, final_path)
            created.append(final_path)
            if final_path.parent == VIDEOS_FOLDER:
                created.append(generate_poster(final_path))
    except BaseException:
        for path in created:
            path.unlink(missing_ok=True)
        raise

    return entries


def validate_flight(
    key: str, flight: dict, places: dict, drones: dict
) -> list[list[Segment]] | None:
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
        if clip.get("drone") not in drones:
            fail(
                f"{key}: clip {describe_clip(clip)} has drone {clip.get('drone')!r}, "
                f"not one of {DRONES_YAML.name} ({', '.join(map(str, drones))})"
            )
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

    both = set(files) & set(discarded(flight))
    if both:
        fail(f"{key}: {', '.join(sorted(both))} is both discarded and cut from")

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

    camera_lengths: dict[str, float] = {}
    for file in files:
        for camera in camera_map(flight).get(file) or {}:
            camera_path = CAMERA_FOLDER / camera
            if not camera_path.exists():
                fail(f"{key}: nonexistent camera recording '{camera}'")
            camera_lengths[camera] = float(
                probe(camera_path).get("format", {}).get("duration", 0)
            )

    segments_by_clip: list[list[Segment]] = []
    for clip in clips:
        try:
            cuts = parse_clip(clip, lengths)
        except ValueError as error:
            fail(f"{key}: {error}")
        segments_by_clip.append(clip_segments(cuts, camera_map(flight), camera_lengths))
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

    return segments_by_clip


def make_flight_strips(flights: dict) -> None:
    make_strips(
        {
            key: [
                VIDEOS_FOLDER / clip["file"]
                for clip in flight.get("clips") or []
                if isinstance(clip, dict) and clip.get("file")
            ]
            for key, flight in flights.items()
        },
        STRIPS_FOLDER,
        height=64,
    )


def cmd_build(args):
    require_tools("ffmpeg", "ffprobe", "cwebp")

    VIDEOS_FOLDER.mkdir(parents=True, exist_ok=True)
    SOURCES_FOLDER.mkdir(parents=True, exist_ok=True)

    places = load_places()
    drones = load_yaml(DRONES_YAML)
    data = load_drone_yaml()
    flights = normalized_flights(data, places)
    pending = {
        key: flight
        for key, flight in flights.items()
        if isinstance(flight, dict) and (pending_clips(flight) or discarded(flight))
    }

    if not pending:
        print("No pending flights to process.")
        make_flight_strips(flights)
        return

    ready: dict[str, list[list[Segment]]] = {}
    owner: dict[str, str] = {}
    for key, flight in pending.items():
        segments_by_clip = validate_flight(key, flight, places, drones)
        if segments_by_clip is None:
            continue
        ready[key] = segments_by_clip
        files = {s.file for segments in segments_by_clip for s in segments}
        for file in files | set(discarded(flight)):
            if file in owner:
                fail(f"'{file}' is used by both {owner[file]} and {key}")
            owner[file] = key

    taken = existing_keys(VIDEOS_FOLDER)
    total = 0
    try:
        for key, segments_by_clip in ready.items():
            flight = pending[key]
            used = {s.file for segments in segments_by_clip for s in segments}
            names = plan_names(key, flight, taken)
            taken |= {Path(name).stem.rsplit("-", 1)[-1] for name in names}
            entries = process_flight(key, flight, segments_by_clip, names)
            built = iter(entries)

            flight["clips"] = [
                next(built) if is_pending(clip) else clip
                for clip in flight.get("clips") or []
            ]
            used |= set(discarded(flight))
            flight.pop("discard", None)
            cameras = {c for cs in camera_map(flight).values() for c in cs}
            flight.pop("camera", None)
            save_drone_yaml(data)

            # Another flight's recordings may still need a camera recording.
            still_needed = known_cameras(data)
            used |= {f"camera/{c}" for c in cameras} - still_needed
            for file in sorted(used):
                # Discarded camera recordings are camera/FILE, the rest bare.
                folder = VIDEOS_FOLDER if "/" in file else SOURCES_FOLDER
                (folder / file).unlink(missing_ok=True)
            total += len(entries)
    except RuntimeError as error:
        print(f"\nERROR: {error}", file=sys.stderr)
        print(
            "The recordings were left in place; fix the clip and re-run.",
            file=sys.stderr,
        )
        sys.exit(1)

    make_flight_strips(flights)
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
    add_parser.add_argument(
        "--no-detect",
        action="store_true",
        help="Seed one whole-length clip per recording instead of one per flight "
        "found in the OSD",
    )
    add_parser.set_defaults(func=cmd_add)

    build_parser = subparsers.add_parser("build", help="Cut clips out of recordings")
    build_parser.set_defaults(func=cmd_build)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
