#!/usr/bin/env python3
"""Finds flights in goggle recordings by reading the Betaflight OSD."""

import argparse
import hashlib
import json
import os
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path
from subprocess import DEVNULL, PIPE, Popen

# Recordings are read one thread each; BLAS threads would only oversubscribe.
for variable in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(variable, "1")

import numpy as np  # noqa: E402
from numpy.lib.stride_tricks import sliding_window_view  # noqa: E402
from PIL import Image  # noqa: E402

from video_common import HAS_CUDA, probe, video_stream  # noqa: E402

SCRIPT_DIR = Path(__file__).parent
HUGO_ROOT = SCRIPT_DIR.parent
CACHE_DIR = HUGO_ROOT / ".cache" / "drone-osd"

# Bump when the reading code changes, to invalidate cached readings.
OSD_VERSION = 3

FPS = 5

FRAME_W, FRAME_H = 640, 480


@dataclass(frozen=True)
class Profile:
    """A kind of recording: how its frame maps onto the 640x480 OSD grid all
    the positions below are in, and the templates its OSD font is matched to."""

    name: str
    to_frame: str
    # What the journal keeps of a frame, as ffmpeg filters ending in a comma.
    picture: str = ""

    @property
    def templates(self) -> Path:
        return SCRIPT_DIR / f"drone_osd-{self.name}.npz"


# Named after the recorder, not the video link: the HDZero goggles record
# analog flights too.
PROFILES = {
    "analog": Profile("analog", f"scale={FRAME_W}:{FRAME_H}"),
    # 1280x720, the grid spanning x 189-1097 (32 px columns, measured).
    "hdzero-dvr": Profile(
        "hdzero-dvr",
        f"crop=ih*1.2611:ih:(iw-ih*1.2611)/2+ih*0.0042:0,scale={FRAME_W}:{FRAME_H}",
        # The 4:3 picture, without the goggles' own icons in the bars aside.
        picture="crop=ih*4/3:ih,",
    ),
}


def profile_of(path: Path) -> Profile:
    stream = video_stream(path)
    widescreen = int(stream["width"]) / int(stream["height"]) > 1.5
    return PROFILES["hdzero-dvr" if widescreen else "analog"]


# Current is right-aligned in cells 21-26 as ` 6.12A` or `10.45A`.
CELL_W, CELL_X0 = 22.4, 9.0
CELL_Y, CELL_H = 404, 28
AMPS_CELLS = range(21, 27)
WORDS = {
    "stats": ((276, 118, 116, 25), "D"),
    "armed": ((276, 226, 108, 25), "D"),
    "crashflip-switch": ((186, 118, 116, 25), "T"),
    "crash-flip": ((208, 118, 116, 25), "T"),
}
CELL_SLACK, WORD_SLACK = 2, 4

CROP = (176, 108, 444, 332)

# Text is bright with a dark outline, unlike a bright sky or a white shirt.
WHITE = 190
OUTLINE, CONTRAST = 3, 100
BLANK_PIXELS = 4
MATCH = 0.75

# Detection, in seconds; see CLAUDE.md for how these were measured.
FLY_AMPS = 1.0
MIN_IDLE = 7.0  # recoveries idled <= 6.0 s, pickups >= 7.6 s (2026-09-23, HDZero)
MAX_BLACKOUT = 15.0
PRE_ROLL = 1.0
POST_ROLL = 2.0
MIN_FLIGHT = 8.0  # seconds flown; failed hops and flip attempts had <= 6 s
MIN_PIECE = 0.5
MAX_SEAM = 1.0  # a longer gap between two recordings ends any flight

STATIC_DIFF = 22
MOSTLY_STATIC = 0.5

GLYPHS = "0123456789.A"
AMPS_TEXT = re.compile(r"( \d|\d\d)\.\d\dA")
DISARMED, TURTLE, STATIC = "D", "T", "S"


def box_slice(box: tuple[int, int, int, int], slack: int) -> tuple[slice, slice]:
    x, y, w, h = box
    if not (
        CROP[0] <= x - slack
        and x + w + slack <= CROP[0] + CROP[2]
        and CROP[1] <= y - slack
        and y + h + slack <= CROP[1] + CROP[3]
    ):
        raise ValueError(f"{box} grown by {slack} px is not within CROP {CROP}")
    return (
        slice(y - slack - CROP[1], y + h + slack - CROP[1]),
        slice(x - slack - CROP[0], x + w + slack - CROP[0]),
    )


def cell_box(cell: int) -> tuple[int, int, int, int]:
    return (round(CELL_X0 + cell * CELL_W), CELL_Y, round(CELL_W), CELL_H)


def shifted(template: np.ndarray, slack: int) -> np.ndarray:
    h, w = template.shape
    out = np.zeros((2 * slack + 1, 2 * slack + 1, h + 2 * slack, w + 2 * slack))
    for dy in range(2 * slack + 1):
        for dx in range(2 * slack + 1):
            out[dy, dx, dy : dy + h, dx : dx + w] = template
    return out.reshape(-1, (h + 2 * slack) * (w + 2 * slack)).astype(np.float32)


def text_mask(frames: np.ndarray, box: tuple[int, int, int, int], slack: int):
    rows, cols = box_slice(box, slack + OUTLINE)
    region = frames[:, rows, cols].astype(np.int16)
    darkest = region
    for axis in (1, 2):
        window = sliding_window_view(darkest, 2 * OUTLINE + 1, axis=axis)
        darkest = window.min(-1)
    inner = region[:, OUTLINE:-OUTLINE, OUTLINE:-OUTLINE]
    return (inner >= WHITE) & (darkest <= inner - CONTRAST)


def best_dice(windows: np.ndarray, placements: np.ndarray) -> np.ndarray:
    flat = windows.reshape(len(windows), -1).astype(np.float32)
    overlap = flat @ placements.T
    sizes = flat.sum(1, keepdims=True) + placements.sum(1)
    return (2 * overlap / np.maximum(sizes, 1)).max(1)


@dataclass
class Templates:
    glyphs: list[np.ndarray]
    words: dict[str, np.ndarray]
    digest: str

    @classmethod
    def load(cls, profile: Profile) -> "Templates":
        path = profile.templates
        if not path.exists():
            raise RuntimeError(
                f"no OSD templates at {path.relative_to(HUGO_ROOT)}; "
                "see `uv run scripts/drone_osd.py learn --help`"
            )
        data = np.load(path)
        return cls(
            glyphs=[shifted(glyph, CELL_SLACK) for glyph in data["glyphs"]],
            words={word: shifted(data[word], WORD_SLACK) for word in WORDS},
            digest=hashlib.sha1(path.read_bytes()).hexdigest(),
        )


def read_glyphs(frames: np.ndarray, templates: Templates) -> list[list[str | None]]:
    stacked = np.stack(
        [text_mask(frames, cell_box(c), CELL_SLACK) for c in AMPS_CELLS], 1
    )
    n, count = stacked.shape[:2]
    windows = stacked.reshape(n * count, *stacked.shape[2:])

    scores = np.stack([best_dice(windows, g) for g in templates.glyphs], 1)
    best = scores.argmax(1)
    blank = windows.reshape(len(windows), -1).sum(1) < BLANK_PIXELS

    out: list[str | None] = []
    for index in range(len(windows)):
        if blank[index]:
            out.append(" ")
        elif scores[index, best[index]] >= MATCH:
            out.append(GLYPHS[best[index]])
        else:
            out.append(None)
    return [out[i * count : (i + 1) * count] for i in range(n)]


def parse_amps(cells: list[str | None]) -> float | None:
    if None in cells:
        return None
    text = "".join(cell or "" for cell in cells)
    return float(text[:-1]) if AMPS_TEXT.fullmatch(text) else None


def classify(frames: np.ndarray, templates: Templates) -> list:
    """Per frame: amps, DISARMED, TURTLE, STATIC or None."""
    readings: list = [parse_amps(cells) for cells in read_glyphs(frames, templates)]

    jumps = np.abs(np.diff(frames.astype(np.int16), axis=2)).mean((1, 2))
    for index in np.flatnonzero(jumps > STATIC_DIFF):
        if readings[index] is None:
            readings[index] = STATIC

    # TURTLE last: ARMED can flash along with it.
    for word, (box, reading) in sorted(WORDS.items(), key=lambda w: w[1][1]):
        mask = text_mask(frames, box, WORD_SLACK)
        for index in np.flatnonzero(best_dice(mask, templates.words[word]) >= MATCH):
            readings[index] = reading
    return readings


def decode(
    path: Path,
    fps: float = FPS,
    chunk: int = 256,
    seek: float = 0,
    limit: int = 0,
    threads: int = 1,
):
    x, y, w, h = CROP
    command = ["ffmpeg", "-nostdin", "-v", "error", "-threads", str(threads)]
    # HEVC decodes 13x faster on the GPU; MJPEG, which NVDEC refuses here, just
    # falls back to the CPU.
    if HAS_CUDA:
        command += ["-hwaccel", "cuda"]
    command += ["-ss", str(seek), "-i", str(path)]
    if limit:
        command += ["-frames:v", str(limit)]
    command += [
        "-an",
        "-vf",
        f"fps={fps},{profile_of(path).to_frame},crop={w}:{h}:{x}:{y},format=gray",
        "-f",
        "rawvideo",
        "-",
    ]
    proc = Popen(command, stdin=DEVNULL, stdout=PIPE, stderr=DEVNULL)
    assert proc.stdout is not None
    size = w * h
    try:
        while True:
            data = proc.stdout.read(size * chunk)
            if not data:
                break
            frames = len(data) // size
            yield np.frombuffer(data[: frames * size], np.uint8).reshape(frames, h, w)
    finally:
        proc.stdout.close()
        proc.wait()
    if proc.returncode != 0:
        raise RuntimeError(f"ffmpeg exited {proc.returncode} reading '{path.name}'")


def cache_key(path: Path, profile: Profile, templates: Templates) -> dict:
    stat = path.stat()
    return {
        "size": stat.st_size,
        # The goggles restart their numbering, so the name alone is not enough.
        "mtime": stat.st_mtime,
        "profile": profile.to_frame,
        "templates": templates.digest,
        "version": OSD_VERSION,
        "tunables": [FPS, CELL_W, CELL_X0, CELL_Y, CELL_H, AMPS_CELLS.start]
        + [WORDS, CELL_SLACK, WORD_SLACK, *CROP]
        + [WHITE, OUTLINE, CONTRAST, BLANK_PIXELS, MATCH, STATIC_DIFF],
    }


def read_recording(path: Path, threads: int = 1) -> list:
    profile = profile_of(path)
    templates = Templates.load(profile)
    cache = CACHE_DIR / f"{path.name}.json"
    # As JSON stores it (tuples come back as lists), or it would never match.
    key = json.loads(json.dumps(cache_key(path, profile, templates)))
    if cache.exists():
        try:
            cached = json.loads(cache.read_text())
            if cached.get("key") == key:
                return cached["readings"]
        except (ValueError, KeyError):
            pass

    readings: list = []
    for frames in decode(path, threads=threads):
        readings += classify(frames, templates)

    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache.write_text(json.dumps({"key": key, "readings": readings}))
    return readings


@dataclass
class Session:
    files: list[str]
    lengths: list[float]
    readings: list[list]
    # When each recording ended by the clock, if the goggles keep time.
    ends: list[float] | None = None

    @property
    def offsets(self) -> list[float]:
        """Where each recording starts on the session timeline: back to back,
        or with the real gaps between them where the clock can be trusted."""
        if self.ends is None:
            return list(np.cumsum([0.0] + self.lengths[:-1]))
        first = self.ends[0] - self.lengths[0]
        return [end - length - first for end, length in zip(self.ends, self.lengths)]

    @property
    def seams(self) -> list[float]:
        """Offsets of the recordings that start after a real gap."""
        offsets = self.offsets
        return [
            offsets[i + 1]
            for i in range(len(offsets) - 1)
            if offsets[i + 1] - (offsets[i] + self.lengths[i]) > MAX_SEAM
        ]


def recording_ends(paths: list[Path], lengths: list[float]) -> list[float] | None:
    """The mtimes, if they read as when each recording ended. The analog
    goggles have no clock (2090 dates, overlapping recordings); HDZero does,
    and splits a session into files wherever the video link dropped."""
    ends = [path.stat().st_mtime for path in paths]
    if max(ends) > time.time():
        return None
    for i in range(len(ends) - 1):
        if ends[i + 1] - lengths[i + 1] < ends[i] - MAX_SEAM:
            return None
    return ends


def read_session(paths: list[Path]) -> Session:
    cores = os.cpu_count() or 4
    # Without a GPU, a few long HEVC files would otherwise leave cores idle.
    threads = max(1, cores // max(len(paths), 1))

    def work(path: Path) -> tuple[float, list]:
        length = float(probe(path).get("format", {}).get("duration", 0))
        return length, read_recording(path, threads)

    with ThreadPoolExecutor(max_workers=cores) as pool:
        results = list(pool.map(work, paths))
    lengths = [length for length, _ in results]
    return Session(
        files=[path.name for path in paths],
        lengths=lengths,
        readings=[readings for _, readings in results],
        ends=recording_ends(paths, lengths),
    )


def state(reading) -> str:
    if isinstance(reading, float):
        return "F" if reading >= FLY_AMPS else "I"
    return {DISARMED: "I", TURTLE: "T", STATIC: "?", None: "?"}[reading]


def is_break(states: str, times: np.ndarray) -> bool:
    """Whether a gap between two flying samples separates two flights."""
    step = 1 / FPS
    start = 0
    for part in states.split("T"):
        first, last = part.find("I"), part.rfind("I")
        if first != -1:
            span = times[start + last] - times[start + first] + step
            if span >= MIN_IDLE and 2 * part.count("I") >= last - first + 1:
                return True
        start += len(part) + 1
    return any(len(run) * step > MAX_BLACKOUT for run in re.findall(r"\?+", states))


def split_flights(
    times: np.ndarray, readings: list, seams: list[float] = ()
) -> tuple[list, int]:
    step = 1 / FPS
    states = list(state(reading) for reading in readings)
    # A lone flying sample is a misread.
    for index, current in enumerate(states):
        near = states[max(index - 2, 0) : index] + states[index + 1 : index + 3]
        if current == "F" and "F" not in near:
            states[index] = "?"
    states = "".join(states)

    runs: list[list[int]] = []
    previous = -1

    def across(a: float, b: float) -> bool:
        return any(a < seam <= b for seam in seams)

    for index in (match.start() for match in re.finditer("F", states)):
        gap = slice(previous + 1, index)
        if (
            not runs
            or across(times[previous], times[index])
            or is_break(states[gap], times[gap])
        ):
            runs.append([index, index])
        else:
            runs[-1][1] = index
        previous = index

    flights = []
    short = 0
    for first, last in runs:
        end = times[last] + step
        # Flying time, not span: hops and crash-flips between re-arms add up to
        # a long span with little flying in it.
        if states[first : last + 1].count("F") * step < MIN_FLIGHT:
            short += 1
            continue
        before = first
        while before > 0 and times[first] - times[before - 1] <= PRE_ROLL:
            if readings[before - 1] == STATIC or across(
                times[before - 1], times[before]
            ):
                break
            before -= 1
        after = last
        while after + 1 < len(times) and times[after + 1] - end < POST_ROLL:
            if readings[after + 1] == STATIC or across(times[after], times[after + 1]):
                break
            after += 1
        flights.append([times[before], times[after] + step])

    total = times[-1] + step if len(times) else 0.0
    for index, flight in enumerate(flights):
        low = flights[index - 1][1] if index else 0.0
        flight[0] = max(flight[0], low)
        flight[1] = min(flight[1], total)
        if index + 1 < len(flights):
            middle = (flight[1] + flights[index + 1][0]) / 2
            if flight[1] > flights[index + 1][0]:
                flight[1] = flights[index + 1][0] = middle
    return [tuple(f) for f in flights], short


def to_cuts(session: Session, start: float, end: float) -> list:
    cuts = []
    for file, offset, length in zip(session.files, session.offsets, session.lengths):
        low, high = max(start, offset), min(end, offset + length)
        if high - low < MIN_PIECE:
            continue
        cuts.append(
            (
                file,
                None if low - offset < MIN_PIECE else low - offset,
                None if offset + length - high < MIN_PIECE else high - offset,
            )
        )
    return cuts


@dataclass
class Detection:
    clips: list[list]
    spans: list[tuple[float, float]]
    short: int
    unread: list[str]
    discard: list[str]


def detect_flights(paths: list[Path]) -> Detection:
    session = read_session(paths)
    times, readings = [], []
    for offset, file_readings in zip(session.offsets, session.readings):
        times += [offset + i / FPS for i in range(len(file_readings))]
        readings += file_readings
    spans, short = split_flights(np.array(times), readings, session.seams)
    clips = [to_cuts(session, start, end) for start, end in spans]

    used = {file for cuts in clips for file, _, _ in cuts}
    unread, discard = [], []
    for file, file_readings in zip(session.files, session.readings):
        if file in used:
            continue
        static = file_readings.count(STATIC) / max(len(file_readings), 1)
        read = any(r not in (None, STATIC) for r in file_readings)
        (discard if read or static >= MOSTLY_STATIC else unread).append(file)

    return Detection(clips, spans, short, unread, discard)


# --- Learning the templates -------------------------------------------------


def cluster(masks: list[np.ndarray], threshold: float = 0.9) -> list[list[int]]:
    reps: list[np.ndarray] = []
    members: list[list[int]] = []
    for index, mask in enumerate(masks):
        core = mask[CELL_SLACK:-CELL_SLACK, CELL_SLACK:-CELL_SLACK]
        if reps:
            scores = best_dice(np.stack(reps), shifted(core, CELL_SLACK))
            best = int(scores.argmax())
            if scores[best] >= threshold:
                members[best].append(index)
                continue
        reps.append(mask)
        members.append([index])
    return sorted(members, key=len, reverse=True)


def learn_masks(paths: list[Path]) -> list[np.ndarray]:
    def work(path: Path) -> list[np.ndarray]:
        found = []
        for frames in decode(path, fps=1):
            for cell in AMPS_CELLS:
                for mask in text_mask(frames, cell_box(cell), CELL_SLACK):
                    if mask.sum() >= BLANK_PIXELS:
                        found.append(mask)
        return found

    with ThreadPoolExecutor(max_workers=os.cpu_count() or 4) as pool:
        return [mask for masks in pool.map(work, paths) for mask in masks]


def grab_word(specs: list[str], box: tuple[int, int, int, int], sources: Path):
    return np.mean([grab_frame_box(spec, box, sources) for spec in specs], 0) >= 0.5


def grab_frame_box(spec: str, box: tuple[int, int, int, int], sources: Path):
    file, _, seconds = spec.partition("@")
    frames = next(decode(sources / file, seek=float(seconds), limit=1))
    return text_mask(frames, box, 0)[0]


def cmd_learn(args):
    paths = sorted(args.recordings)
    profiles = {profile_of(path) for path in paths}
    if len(profiles) != 1:
        sys.exit(f"learn from one kind of recording at a time, not {profiles}")
    templates = profiles.pop().templates
    masks = learn_masks(paths)
    clusters = [c for c in cluster(masks) if len(c) >= args.min_count]
    print(f"{len(masks)} glyphs in {len(clusters)} clusters (>= {args.min_count}).")

    if not args.labels:
        size = masks[0].shape
        tile = np.zeros((len(clusters), size[0] + 4, size[1] + 4), np.uint8)
        for index, members in enumerate(clusters):
            mean = np.mean([masks[i] for i in members], 0)
            tile[index, 2:-2, 2:-2] = (mean * 255).astype(np.uint8)
            print(f"  {index:3}: {len(members)} samples")
        columns = 10
        rows = -(-len(clusters) // columns)
        sheet = np.zeros((rows * tile.shape[1], columns * tile.shape[2]), np.uint8)
        for index in range(len(clusters)):
            r, c = divmod(index, columns)
            sheet[
                r * tile.shape[1] : (r + 1) * tile.shape[1],
                c * tile.shape[2] : (c + 1) * tile.shape[2],
            ] = tile[index]
        Image.fromarray(sheet).resize(
            (sheet.shape[1] * 4, sheet.shape[0] * 4), Image.NEAREST
        ).save(args.montage)
        print(f"Clusters are numbered row by row in {args.montage}, ten per row.")
        print("Pass --labels '0=7,1=3,...' (cluster=glyph, glyphs 0-9 . A).")
        return

    missing = [word for word in WORDS if not getattr(args, word.replace("-", "_"))]
    if missing:
        sys.exit(f"--labels needs {' '.join('--' + w for w in missing)} too")
    labels: dict[str, list[np.ndarray]] = {}
    for pair in args.labels.split(","):
        index, _, glyph = pair.strip().partition("=")
        if glyph not in GLYPHS:
            sys.exit(f"'{glyph}' is not one of {GLYPHS}")
        members = clusters[int(index)]
        labels.setdefault(glyph, []).extend(masks[i] for i in members)
    missing = [g for g in GLYPHS if g not in labels]
    if missing:
        sys.exit(f"no cluster labelled {' '.join(missing)}")

    crop = (slice(CELL_SLACK, -CELL_SLACK), slice(CELL_SLACK, -CELL_SLACK))
    glyphs = np.stack([np.mean(labels[g], 0)[crop] >= 0.5 for g in GLYPHS])
    sources = paths[0].parent
    np.savez_compressed(
        templates,
        glyphs=glyphs,
        **{
            word: grab_word(getattr(args, word.replace("-", "_")), box, sources)
            for word, (box, _) in WORDS.items()
        },
    )
    print(f"Saved {templates.relative_to(HUGO_ROOT)}.")


def cmd_read(args):
    session = read_session(sorted(args.recordings))
    for file, readings in zip(session.files, session.readings):
        known = sum(r is not None for r in readings)
        print(f"{file}: {known}/{len(readings)} read")
        if args.verbose:
            for index, reading in enumerate(readings):
                print(f"  {index / FPS:7.1f}  {reading}")


def main():
    parser = argparse.ArgumentParser(description="Read the drone OSD")
    subparsers = parser.add_subparsers(dest="command", required=True)

    learn = subparsers.add_parser("learn", help="(Re)build the OSD templates")
    learn.add_argument("recordings", nargs="+", type=Path)
    learn.add_argument("--labels", help="cluster=glyph pairs, comma-separated")
    for word in WORDS:
        learn.add_argument(
            f"--{word}",
            action="append",
            metavar="FILE@SECONDS",
            help=f"a frame showing {word.upper()} (repeat to average a few)",
        )
    learn.add_argument("--min-count", type=int, default=20)
    learn.add_argument("--montage", default="osd-clusters.png")
    learn.set_defaults(func=cmd_learn)

    read = subparsers.add_parser("read", help="Print the readings of recordings")
    read.add_argument("recordings", nargs="+", type=Path)
    read.add_argument("-v", "--verbose", action="store_true")
    read.set_defaults(func=cmd_read)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
