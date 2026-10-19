#!/usr/bin/env python3
"""Find flights in goggle recordings by reading the Betaflight OSD."""

import argparse
import functools
import hashlib
import json
import os
import re
import sys
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path
from subprocess import DEVNULL, PIPE, Popen

# We already run one thread per recording.
for variable in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(variable, "1")

import numpy as np  # noqa: E402
from numpy.lib.stride_tricks import sliding_window_view  # noqa: E402
from PIL import Image  # noqa: E402

from video_common import HAS_CUDA, probe  # noqa: E402

SCRIPT_DIR = Path(__file__).parent
HUGO_ROOT = SCRIPT_DIR.parent
CACHE_DIR = HUGO_ROOT / ".cache" / "drone-osd"

# Bump to invalidate the cache.
OSD_VERSION = 8

FPS = 5


@dataclass(frozen=True, eq=False)
class Layout:
    """Where the OSD elements are on the frame a profile decodes to."""

    width: int
    height: int
    # Current, e.g. ` 6.12A` or `10.45A`, right-aligned in these cells of a row.
    cell_w: float
    cell_x0: float
    cell_y: int
    cell_h: int
    amps_cells: range
    # word: ((x, y, w, h), the reading it stands for)
    words: dict[str, tuple[tuple[int, int, int, int], str]]
    # The craft name, e.g. `SYL`, left-aligned from this cell of its row.
    craft_cell: int
    craft_y: int
    # Where we measure motion and static.
    crop: tuple[int, int, int, int]
    cell_slack: int = 2
    word_slack: int = 4
    # The part of a cell we read, if narrower (so the slack misses neighbours).
    glyph_w: int | None = None
    # Fewer lit pixels than this is a blank cell (not the dot).
    blank_pixels: int = 4

    @property
    def glyph_size(self) -> tuple[int, int]:
        return self.cell_h, self.glyph_w or round(self.cell_w)


# Betaflight's SD OSD (30x16), on a 640x480 frame.
SD_LAYOUT = Layout(
    width=640,
    height=480,
    cell_w=22.4,
    cell_x0=9.0,
    cell_y=404,
    cell_h=28,
    amps_cells=range(21, 27),
    words={
        "stats": ((276, 118, 116, 25), "D"),
        "armed": ((276, 226, 108, 25), "D"),
        "crashflip-switch": ((186, 118, 116, 25), "T"),
        "crash-flip": ((208, 118, 116, 25), "T"),
    },
    craft_cell=1,
    craft_y=44,
    crop=(176, 108, 444, 332),
)

# The goggles' HD OSD over the whole 1280x720 frame, scaled to 960x540, where
# its pitch is 18 px and the picture density about that of SD_LAYOUT. It
# shifts by up to 3 px between recordings, hence the extra slack.
HD_LAYOUT = Layout(
    width=960,
    height=540,
    cell_w=18,
    cell_x0=8,
    cell_y=479,
    cell_h=17,
    amps_cells=range(43, 49),
    words={"stats": ((438, 182, 92, 17), "D")},
    craft_cell=3,
    craft_y=74,
    crop=(329, 122, 472, 374),
    cell_slack=3,
    word_slack=5,
    glyph_w=13,
    blank_pixels=2,
)


@dataclass(frozen=True, eq=False)
class Profile:
    """How a recorder's frame maps onto an OSD layout."""

    name: str
    to_frame: str
    layout: Layout
    # ffmpeg filters (ending in a comma) for the part of the frame we keep.
    picture: str = ""
    # Whether a flight can continue into the next file. On HDZero a new file
    # means the link dropped or the goggles restarted.
    chunked: bool = False

    @property
    def templates(self) -> Path:
        return SCRIPT_DIR / f"drone_osd-{self.name}.npz"


# By recorder and OSD, not video link (the HDZero goggles record analog too).
PROFILES = {
    "analog": Profile("analog", "scale=640:480", SD_LAYOUT, chunked=True),
    # 1280x720, OSD grid spans x 189-1097 (measured).
    "hdzero-dvr": Profile(
        "hdzero-dvr",
        "crop=ih*1.2611:ih:(iw-ih*1.2611)/2+ih*0.0042:0,scale=640:480",
        SD_LAYOUT,
        # Crop to 4:3 to drop the goggles' icons on the sides.
        picture="crop=ih*4/3:ih,",
    ),
    "hdzero-hd": Profile("hdzero-hd", "scale=960:540", HD_LAYOUT),
}
# Set by --profile, for recordings without a recognisable OSD yet.
FORCED_PROFILE: Profile | None = None

# Where only the HD OSD has text: left of the 4:3 picture (the craft name),
# right of it (the amps) and its STATS.
HD_MARKS = ((56, 70, 50, 24), (852, 474, 46, 24), HD_LAYOUT.words["stats"][0])
# Lit pixels in a mark, and marked frames of those sampled, for an HD OSD.
HD_INK, HD_SAMPLES, HD_FRAMES = 16, 20, 2


@functools.cache
def profile_of(path: Path) -> Profile:
    if FORCED_PROFILE is not None:
        return FORCED_PROFILE
    info = probe(path)
    stream = next(s for s in info["streams"] if s.get("codec_type") == "video")
    if int(stream["width"]) / int(stream["height"]) <= 1.5:
        return PROFILES["analog"]
    hd = PROFILES["hdzero-hd"]
    length = float(info.get("format", {}).get("duration", 0))
    sampled = decode(path, hd, fps=HD_SAMPLES / max(length, 1), keyframes=True)
    frames = np.concatenate(list(sampled))
    marked = np.zeros(len(frames), bool)
    for box in HD_MARKS:
        marked |= text_mask(frames, box, 0).sum((1, 2)) >= HD_INK
    return hd if marked.sum() >= HD_FRAMES else PROFILES["hdzero-dvr"]


# OSD text is white with a dark outline, which a bright sky isn't.
WHITE = 190
OUTLINE, CONTRAST = 3, 100
BLANK_PIXELS = 4
MATCH = 0.75

# Measured: disarmed < 0.3 A, armed on the ground 0.5-0.9 A, flying > 1.5 A.
FLY_AMPS = 1.0
MIN_IDLE = 7.0  # crash recoveries idle <= 6 s, picking it up >= 7.6 s
MAX_BLACKOUT = 15.0
PRE_ROLL = 1.0
POST_ROLL = 2.0
MIN_FLIGHT = 8.0  # failed hops and flip attempts are <= 6 s
# Less motion than this means I was holding it and throttling (flights 17-21,
# in hand 9.6).
MIN_MOTION = 13.0
MIN_PIECE = 0.5
MAX_SEAM = 1.0  # longer gap between recordings = separate flights

# Mean difference of neighbouring pixels: footage < 20, static 25-50.
STATIC_DIFF = 22
MOSTLY_STATIC = 0.5

# The HD OSD's `AMP` is learned as the A.
GLYPHS = "0123456789.A"
AMPS_TEXT = re.compile(r"( \d|\d\d)\.\d\dA")
DISARMED, TURTLE, STATIC = "D", "T", "S"


def box_slice(
    box: tuple[int, int, int, int], slack: int, shape: tuple[int, ...]
) -> tuple[slice, slice]:
    x, y, w, h = box
    height, width = shape[-2:]
    if not (
        0 <= x - slack
        and x + w + slack <= width
        and 0 <= y - slack
        and y + h + slack <= height
    ):
        raise ValueError(f"{box} grown by {slack} px is not within the frame")
    return slice(y - slack, y + h + slack), slice(x - slack, x + w + slack)


def cell_box(layout: Layout, cell: int) -> tuple[int, int, int, int]:
    x = round(layout.cell_x0 + cell * layout.cell_w)
    height, width = layout.glyph_size
    return (x, layout.cell_y, width, height)


def craft_box(layout: Layout, name: str) -> tuple[int, int, int, int]:
    x = round(layout.cell_x0 + layout.craft_cell * layout.cell_w)
    return (x, layout.craft_y, round(len(name) * layout.cell_w), layout.cell_h)


def cropped(frames: np.ndarray, layout: Layout) -> np.ndarray:
    x, y, w, h = layout.crop
    return frames[:, y : y + h, x : x + w]


def shifted(template: np.ndarray, slack: int) -> np.ndarray:
    h, w = template.shape
    out = np.zeros((2 * slack + 1, 2 * slack + 1, h + 2 * slack, w + 2 * slack))
    for dy in range(2 * slack + 1):
        for dx in range(2 * slack + 1):
            out[dy, dx, dy : dy + h, dx : dx + w] = template
    return out.reshape(-1, (h + 2 * slack) * (w + 2 * slack)).astype(np.float32)


def text_mask(frames: np.ndarray, box: tuple[int, int, int, int], slack: int):
    rows, cols = box_slice(box, slack + OUTLINE, frames.shape)
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
    # By craft name, lowercase.
    crafts: dict[str, np.ndarray]
    digest: str
    layout: Layout

    @classmethod
    def load(cls, profile: Profile) -> "Templates":
        path = profile.templates
        if not path.exists():
            raise RuntimeError(
                f"no OSD templates at {path.relative_to(HUGO_ROOT)}; "
                "see `uv run scripts/drone_osd.py learn --help`"
            )
        data = np.load(path)
        layout = profile.layout
        return cls(
            glyphs=[shifted(glyph, layout.cell_slack) for glyph in data["glyphs"]],
            words={
                word: shifted(data[word], layout.word_slack) for word in layout.words
            },
            crafts={
                key.removeprefix("craft-"): shifted(data[key], layout.word_slack)
                for key in data.files
                if key.startswith("craft-")
            },
            digest=hashlib.sha1(path.read_bytes()).hexdigest(),
            layout=layout,
        )


def read_glyphs(frames: np.ndarray, templates: Templates) -> list[list[str | None]]:
    layout = templates.layout
    stacked = np.stack(
        [
            text_mask(frames, cell_box(layout, c), layout.cell_slack)
            for c in layout.amps_cells
        ],
        1,
    )
    n, count = stacked.shape[:2]
    windows = stacked.reshape(n * count, *stacked.shape[2:])

    scores = np.stack([best_dice(windows, g) for g in templates.glyphs], 1)
    best = scores.argmax(1)
    blank = windows.reshape(len(windows), -1).sum(1) < layout.blank_pixels

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
    # The small A (HD: AMP) loses its outline against bright foliage, and the
    # dot is a few pixels; both are always there.
    cells = [*cells[:-1], "A"]
    if cells[-4] in (None, " "):
        cells[-4] = "."
    if None in cells:
        return None
    text = "".join(cell or "" for cell in cells)
    return float(text[:-1]) if AMPS_TEXT.fullmatch(text) else None


def classify(frames: np.ndarray, templates: Templates) -> list:
    """Per frame: amps, DISARMED, TURTLE, STATIC or None."""
    readings: list = [parse_amps(cells) for cells in read_glyphs(frames, templates)]

    layout = templates.layout
    jumps = np.abs(np.diff(cropped(frames, layout).astype(np.int16), axis=2))
    jumps = jumps.mean((1, 2))
    for index in np.flatnonzero(jumps > STATIC_DIFF):
        if readings[index] is None:
            readings[index] = STATIC

    # TURTLE goes last, since ARMED can flash at the same time.
    for word, (box, reading) in sorted(layout.words.items(), key=lambda w: w[1][1]):
        mask = text_mask(frames, box, layout.word_slack)
        for index in np.flatnonzero(best_dice(mask, templates.words[word]) >= MATCH):
            readings[index] = reading
    return readings


def read_crafts(frames: np.ndarray, templates: Templates) -> list[str | None]:
    """Per frame: the craft name, if it matches one we know."""
    best: list[str | None] = [None] * len(frames)
    scores = np.full(len(frames), MATCH)
    layout = templates.layout
    for name, template in templates.crafts.items():
        box = craft_box(layout, name)
        dice = best_dice(text_mask(frames, box, layout.word_slack), template)
        for index in np.flatnonzero(dice >= scores):
            best[index], scores[index] = name, dice[index]
    return best


def decode(
    path: Path,
    profile: Profile,
    fps: float = FPS,
    # Bytes per read, whatever the frame size.
    chunk_bytes: int = 80_000_000,
    seek: float = 0,
    limit: int = 0,
    threads: int = 1,
    keyframes: bool = False,
):
    command = ["ffmpeg", "-nostdin", "-v", "error", "-threads", str(threads)]
    # Much faster for HEVC; MJPEG just falls back to the CPU.
    if HAS_CUDA:
        command += ["-hwaccel", "cuda"]
    if keyframes:
        command += ["-skip_frame", "nokey"]
    command += ["-ss", str(seek), "-i", str(path)]
    if limit:
        command += ["-frames:v", str(limit)]
    command += [
        "-an",
        "-vf",
        f"fps={fps},{profile.to_frame},format=gray",
        "-f",
        "rawvideo",
        "-",
    ]
    proc = Popen(command, stdin=DEVNULL, stdout=PIPE, stderr=DEVNULL)
    assert proc.stdout is not None
    width, height = profile.layout.width, profile.layout.height
    size = width * height
    chunk = max(1, chunk_bytes // size)
    try:
        while True:
            data = proc.stdout.read(size * chunk)
            if not data:
                break
            frames = len(data) // size
            yield np.frombuffer(data[: frames * size], np.uint8).reshape(
                frames, height, width
            )
    finally:
        proc.stdout.close()
        proc.wait()
    if proc.returncode != 0:
        raise RuntimeError(f"ffmpeg exited {proc.returncode} reading '{path.name}'")


def cache_key(path: Path, profile: Profile, templates: Templates) -> dict:
    stat = path.stat()
    return {
        "size": stat.st_size,
        # The goggles reuse file names.
        "mtime": stat.st_mtime,
        "profile": profile.to_frame,
        "templates": templates.digest,
        "version": OSD_VERSION,
        "tunables": [FPS, repr(profile.layout)]
        + [WHITE, OUTLINE, CONTRAST, BLANK_PIXELS, MATCH, STATIC_DIFF],
    }


def read_recording(path: Path, threads: int = 1) -> tuple[list, list, list]:
    """Readings, motion (NaN for the first sample) and craft per sample."""
    profile = profile_of(path)
    templates = Templates.load(profile)
    cache = CACHE_DIR / f"{path.name}.json"
    # Round-trip through JSON so it compares equal to the cached one.
    key = json.loads(json.dumps(cache_key(path, profile, templates)))
    if cache.exists():
        try:
            cached = json.loads(cache.read_text())
            if cached.get("key") == key:
                return cached["readings"], cached["motion"], cached["crafts"]
        except (ValueError, KeyError):
            pass

    readings: list = []
    motion: list = []
    crafts: list = []
    previous = None
    for frames in decode(path, profile, threads=threads):
        readings += classify(frames, templates)
        crafts += read_crafts(frames, templates)
        small = cropped(frames, profile.layout)[:, ::4, ::4].astype(np.int16)
        if previous is not None:
            small = np.concatenate([previous, small])
        diffs = np.abs(np.diff(small, axis=0)).mean((1, 2)).tolist()
        motion += diffs if previous is not None else [float("nan")] + diffs
        previous = small[-1:]

    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache.write_text(
        json.dumps(
            {"key": key, "readings": readings, "motion": motion, "crafts": crafts}
        )
    )
    return readings, motion, crafts


@dataclass
class Session:
    files: list[str]
    lengths: list[float]
    readings: list[list]
    motion: list[list] | None = None
    crafts: list[list] | None = None
    # Recording end times, if the goggles have a clock.
    ends: list[float] | None = None
    chunked: list[bool] | None = None

    @property
    def offsets(self) -> list[float]:
        """Recording start times, with real gaps if we have a clock."""
        if self.ends is None:
            return list(np.cumsum([0.0] + self.lengths[:-1]))
        first = self.ends[0] - self.lengths[0]
        return [end - length - first for end, length in zip(self.ends, self.lengths)]

    @property
    def seams(self) -> list[float]:
        """Starts of recordings that come after a gap."""
        offsets = self.offsets
        chunked = self.chunked or [True] * len(offsets)
        return [
            offsets[i + 1]
            for i in range(len(offsets) - 1)
            if offsets[i + 1] - (offsets[i] + self.lengths[i]) > MAX_SEAM
            or not (chunked[i] and chunked[i + 1])
        ]


def recording_ends(paths: list[Path], lengths: list[float]) -> list[float] | None:
    """mtimes as end times, if they make sense (the analog goggles have no
    clock and write dates like 2090)."""
    ends = [path.stat().st_mtime for path in paths]
    if max(ends) > time.time():
        return None
    for i in range(len(ends) - 1):
        if ends[i + 1] - lengths[i + 1] < ends[i] - MAX_SEAM:
            return None
    return ends


def read_session(paths: list[Path]) -> Session:
    cores = os.cpu_count() or 4
    threads = max(1, cores // max(len(paths), 1))

    def work(path: Path) -> tuple[float, tuple[list, list, list]]:
        length = float(probe(path).get("format", {}).get("duration", 0))
        return length, read_recording(path, threads)

    with ThreadPoolExecutor(max_workers=cores) as pool:
        results = list(pool.map(work, paths))
    lengths = [length for length, _ in results]
    return Session(
        files=[path.name for path in paths],
        lengths=lengths,
        readings=[readings for _, (readings, _, _) in results],
        motion=[motion for _, (_, motion, _) in results],
        crafts=[crafts for _, (_, _, crafts) in results],
        ends=recording_ends(paths, lengths),
        chunked=[profile_of(path).chunked for path in paths],
    )


def state(reading) -> str:
    if isinstance(reading, float):
        return "F" if reading >= FLY_AMPS else "I"
    return {DISARMED: "I", TURTLE: "T", STATIC: "?", None: "?"}[reading]


def is_break(states: str, times: np.ndarray) -> bool:
    """Whether a gap between flying samples splits two flights."""
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
    times: np.ndarray,
    readings: list,
    seams: list[float] = (),
    motion: list | None = None,
) -> tuple[list, int, int]:
    """Flight (start, end)s, plus how many were too short and held still."""
    step = 1 / FPS
    states = list(state(reading) for reading in readings)
    # A single flying sample is a misread.
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
    short = still = 0
    for first, last in runs:
        end = times[last] + step
        # Count time flown, not the span, which crash-flips can drag out.
        if states[first : last + 1].count("F") * step < MIN_FLIGHT:
            short += 1
            continue
        if motion is not None:
            flying = [motion[i] for i in range(first, last + 1) if states[i] == "F"]
            if np.nanmedian(flying) < MIN_MOTION:
                still += 1
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
    return [tuple(f) for f in flights], short, still


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
    # The craft name read most often in each clip, if any.
    crafts: list[str | None]
    short: int
    still: int
    unread: list[str]
    discard: list[str]


def detect_flights(paths: list[Path]) -> Detection:
    session = read_session(paths)
    times, readings, motion, crafts = [], [], [], []
    for offset, file_readings, file_motion, file_crafts in zip(
        session.offsets, session.readings, session.motion, session.crafts
    ):
        times += [offset + i / FPS for i in range(len(file_readings))]
        readings += file_readings
        motion += file_motion
        crafts += file_crafts
    spans, short, still = split_flights(
        np.array(times), readings, session.seams, motion
    )
    clips = [to_cuts(session, start, end) for start, end in spans]
    times = np.array(times)
    span_crafts = []
    for start, end in spans:
        seen = Counter(
            crafts[i] for i in np.flatnonzero((times >= start) & (times < end))
        )
        seen.pop(None, None)
        span_crafts.append(seen.most_common(1)[0][0] if seen else None)

    used = {file for cuts in clips for file, _, _ in cuts}
    unread, discard = [], []
    for file, file_readings in zip(session.files, session.readings):
        if file in used:
            continue
        static = file_readings.count(STATIC) / max(len(file_readings), 1)
        read = any(r not in (None, STATIC) for r in file_readings)
        (discard if read or static >= MOSTLY_STATIC else unread).append(file)

    return Detection(clips, spans, span_crafts, short, still, unread, discard)


# --- Learning the templates ---


def cluster(
    masks: list[np.ndarray], slack: int, threshold: float = 0.9
) -> list[list[int]]:
    reps: list[np.ndarray] = []
    members: list[list[int]] = []
    for index, mask in enumerate(masks):
        core = mask[slack:-slack, slack:-slack]
        if reps:
            scores = best_dice(np.stack(reps), shifted(core, slack))
            best = int(scores.argmax())
            if scores[best] >= threshold:
                members[best].append(index)
                continue
        reps.append(mask)
        members.append([index])
    return sorted(members, key=len, reverse=True)


def learn_masks(paths: list[Path], profile: Profile) -> list[np.ndarray]:
    layout = profile.layout

    def work(path: Path) -> list[np.ndarray]:
        found = []
        for frames in decode(path, profile, fps=1):
            for cell in layout.amps_cells:
                box = cell_box(layout, cell)
                for mask in text_mask(frames, box, layout.cell_slack):
                    if mask.sum() >= layout.blank_pixels:
                        found.append(mask)
        return found

    with ThreadPoolExecutor(max_workers=os.cpu_count() or 4) as pool:
        return [mask for masks in pool.map(work, paths) for mask in masks]


def grab_word(specs: list[str], box: tuple[int, int, int, int], sources: Path):
    return np.mean([grab_frame_box(spec, box, sources) for spec in specs], 0) >= 0.5


def grab_frame_box(spec: str, box: tuple[int, int, int, int], sources: Path):
    file, _, seconds = spec.partition("@")
    path = sources / file
    frames = next(decode(path, profile_of(path), seek=float(seconds), limit=1))
    return text_mask(frames, box, 0)[0]


def cmd_learn(args):
    paths = sorted(args.recordings)
    profiles = {profile_of(path) for path in paths}
    if len(profiles) != 1:
        sys.exit(f"learn from one kind of recording at a time, not {profiles}")
    profile = profiles.pop()
    layout = profile.layout
    templates = profile.templates
    masks = learn_masks(paths, profile)
    clusters = [
        c for c in cluster(masks, layout.cell_slack) if len(c) >= args.min_count
    ]
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

    missing = [
        word for word in layout.words if not getattr(args, word.replace("-", "_"))
    ]
    if missing:
        sys.exit(f"--labels needs {' '.join('--' + w for w in missing)} too")
    labels: dict[str, list[int]] = {}
    for pair in args.labels.split(","):
        index, _, glyph = pair.strip().partition("=")
        if glyph not in GLYPHS:
            sys.exit(f"'{glyph}' is not one of {GLYPHS}")
        labels.setdefault(glyph, []).append(int(index))
    missing = [g for g in GLYPHS if g not in labels]
    if missing:
        sys.exit(f"no cluster labelled {' '.join(missing)}")

    size = layout.glyph_size
    inked = {}
    for glyph in GLYPHS:
        # Clusters are sorted by size, so this aligns to the largest.
        group = [masks[i] for index in sorted(labels[glyph]) for i in clusters[index]]
        inked[glyph] = aligned_mean(group, layout.cell_slack) >= 0.5
    # Digits are centred, and the rest sit on their baseline.
    glyphs = {g: centered(inked[g], *size) for g in "0123456789"}
    baseline = max(np.nonzero(glyphs["0"])[0])
    glyphs |= {g: centered(inked[g], *size, baseline) for g in ".A"}
    glyphs = np.stack([glyphs[g] for g in GLYPHS])
    sources = paths[0].parent
    np.savez_compressed(
        templates,
        **saved_crafts(templates),
        glyphs=glyphs,
        **{
            word: grab_word(getattr(args, word.replace("-", "_")), box, sources)
            for word, (box, _) in layout.words.items()
        },
    )
    print(f"Saved {templates.relative_to(HUGO_ROOT)}.")


def aligned_mean(masks: list[np.ndarray], slack: int) -> np.ndarray:
    """The mean of masks, each moved by up to slack px onto the first."""
    reference = masks[0]
    moves = [
        (dy, dx) for dy in range(-slack, slack + 1) for dx in range(-slack, slack + 1)
    ]
    moved = []
    for mask in masks:
        candidates = [np.roll(mask, move, (0, 1)) for move in moves]
        moved.append(max(candidates, key=lambda c: (c & reference).sum()))
    return np.mean(moved, 0)


def centered(
    mask: np.ndarray, height: int, width: int, baseline: int | None = None
) -> np.ndarray:
    """A height x width window of the mask, centred on its ink (or with its
    bottom on the baseline row)."""
    rows, cols = np.nonzero(mask)
    if baseline is None:
        y = (rows.min() + rows.max() + 1 - height) // 2
    else:
        y = rows.max() - baseline
    x = (cols.min() + cols.max() + 1 - width) // 2
    padded = np.pad(mask, ((height, height), (width, width)))
    return padded[y + height : y + 2 * height, x + width : x + 2 * width]


def saved_crafts(templates: Path) -> dict[str, np.ndarray]:
    if not templates.exists():
        return {}
    data = np.load(templates)
    return {key: data[key] for key in data.files if key.startswith("craft-")}


def cmd_learn_craft(args):
    name = args.name.lower()
    paths = [Path(spec.partition("@")[0]) for spec in args.frames]
    profiles = {profile_of(path) for path in paths}
    if len(profiles) != 1:
        sys.exit(f"learn from one kind of recording at a time, not {profiles}")
    profile = profiles.pop()
    templates = profile.templates
    if not templates.exists():
        sys.exit(f"no {templates.relative_to(HUGO_ROOT)} yet; run `learn` first")
    data = dict(np.load(templates))
    box = craft_box(profile.layout, name)
    data[f"craft-{name}"] = grab_word(args.frames, box, Path())
    np.savez_compressed(templates, **data)
    print(f"Saved {name.upper()} to {templates.relative_to(HUGO_ROOT)}.")


def cmd_read(args):
    session = read_session(sorted(args.recordings))
    for file, readings, crafts in zip(session.files, session.readings, session.crafts):
        known = sum(r is not None for r in readings)
        seen = Counter(c for c in crafts if c is not None)
        print(
            f"{file}: {known}/{len(readings)} read, crafts "
            + (", ".join(f"{c} {n}" for c, n in seen.most_common()) or "none")
        )
        if args.verbose:
            for index, (reading, craft) in enumerate(zip(readings, crafts)):
                print(f"  {index / FPS:7.1f}  {reading}  {craft or ''}")


def main():
    parser = argparse.ArgumentParser(description="Read the drone OSD")
    subparsers = parser.add_subparsers(dest="command", required=True)

    learn = subparsers.add_parser("learn", help="(Re)build the OSD templates")
    learn.add_argument("recordings", nargs="+", type=Path)
    learn.add_argument("--labels", help="cluster=glyph pairs, comma-separated")
    for word in dict.fromkeys(w for p in PROFILES.values() for w in p.layout.words):
        learn.add_argument(
            f"--{word}",
            action="append",
            metavar="FILE@SECONDS",
            help=f"a frame showing {word.upper()} (repeat to average a few)",
        )
    learn.add_argument("--min-count", type=int, default=20)
    learn.add_argument("--montage", default="osd-clusters.png")
    learn.set_defaults(func=cmd_learn)

    learn_craft = subparsers.add_parser(
        "learn-craft", help="Add or replace the template of a craft name"
    )
    learn_craft.add_argument("name", help="as on the OSD, e.g. syl")
    learn_craft.add_argument(
        "frames",
        nargs="+",
        metavar="FILE@SECONDS",
        help="frames showing the name (several to average a few)",
    )
    learn_craft.set_defaults(func=cmd_learn_craft)

    read = subparsers.add_parser("read", help="Print the readings of recordings")
    read.add_argument("recordings", nargs="+", type=Path)
    read.add_argument("-v", "--verbose", action="store_true")
    read.set_defaults(func=cmd_read)

    for command in (learn, learn_craft, read):
        command.add_argument(
            "--profile",
            choices=PROFILES,
            help="instead of telling it from the recordings",
        )

    args = parser.parse_args()
    if getattr(args, "profile", None):
        global FORCED_PROFILE
        FORCED_PROFILE = PROFILES[args.profile]
    args.func(args)


if __name__ == "__main__":
    main()
