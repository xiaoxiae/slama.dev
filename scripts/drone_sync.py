#!/usr/bin/env python3
"""Sync goggle recordings to action camera recordings by their picture motion.

Both cameras sit on the same frame, so how fast their pictures move (dense
optical flow) rises and falls together. Matching that beat matching the OSD
amps to the camera's audio (0.2 s late from OSD lag, missed short overlaps),
brightness, and the camera's own gyro: in 40 s windows it agrees within 10 ms.

The goggles' clock runs but is off (by years), and the camera's isn't, so every
recording from one goggle session shares one clock error. We take it from the
confident matches and use it to place and check the rest.
"""

import argparse
import datetime
import hashlib
import json
import os
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from pathlib import Path
from subprocess import DEVNULL, PIPE, Popen

import cv2
import numpy as np

from drone_osd import CACHE_DIR
from video_common import HAS_CUDA, probe

# Bump to invalidate the cache.
SYNC_VERSION = 1

RATE = 30
# Frames are tiny: flow only has to see the picture move.
WIDTH = 128
# The goggles' 4:3 picture, without the goggles' icons on the sides.
DVR_CROP = "crop=ih*4/3:ih,"
TREND = 10.0  # s of running median we subtract

MIN_OVERLAP = 20.0  # s, to match without the clock
# Best match against the best one more than EXCLUDE away, and its r.
MIN_RATIO, MIN_R, EXCLUDE = 1.4, 0.4, 2.0
CLOCK_TOLERANCE = 2.0  # s; the camera timestamps whole seconds
# With the clock: how far around its prediction to look, and in how much.
REFINE, MIN_REFINE_OVERLAP = 2.0, 5.0
MIN_COVER = 1.0  # s of overlap worth a camera entry


def duration(path: Path) -> float:
    return float(probe(path).get("format", {}).get("duration", 0))


def camera_start(path: Path) -> float:
    """Unix time of the first frame, from the camera's (UTC) creation_time."""
    tags = probe(path).get("format", {}).get("tags", {})
    text = tags.get("creation_time")
    if not text:
        raise RuntimeError(f"'{path.name}' has no creation_time")
    return datetime.datetime.fromisoformat(text.replace("Z", "+00:00")).timestamp()


def goggle_start(path: Path) -> float:
    """By the goggles' clock: they write the file's mtime as it ends."""
    return path.stat().st_mtime - duration(path)


def frames(path: Path, crop: str) -> np.ndarray:
    stream = next(s for s in probe(path)["streams"] if s.get("codec_type") == "video")
    width, height = int(stream["width"]), int(stream["height"])
    if crop:
        width = height * 4 // 3
    height = round(WIDTH * height / width / 2) * 2
    command = ["ffmpeg", "-nostdin", "-v", "error"]
    if HAS_CUDA:
        command += ["-hwaccel", "cuda"]
    command += ["-i", str(path), "-map", "0:v:0", "-an"]
    command += ["-vf", f"{crop}fps={RATE},scale={WIDTH}:{height},format=gray"]
    command += ["-f", "rawvideo", "-"]
    proc = Popen(command, stdin=DEVNULL, stdout=PIPE, stderr=DEVNULL)
    data, _ = proc.communicate()
    if proc.returncode != 0:
        raise RuntimeError(f"ffmpeg exited {proc.returncode} reading '{path.name}'")
    return np.frombuffer(data, np.uint8).reshape(-1, height, WIDTH)


def flow_speed(frames: np.ndarray) -> np.ndarray:
    """Per frame: log speed of the picture (pan, tilt and roll together)."""
    height, width = frames.shape[1:]
    ys, xs = np.mgrid[0:height, 0:width].astype(np.float32)
    xs -= width / 2
    ys -= height / 2
    radius = xs**2 + ys**2 + 1
    speed = np.full(len(frames), np.nan)
    for i in range(1, len(frames)):
        flow = cv2.calcOpticalFlowFarneback(
            frames[i - 1], frames[i], None, 0.5, 3, 11, 3, 5, 1.1, 0
        )
        dx, dy = flow[..., 0], flow[..., 1]
        # Roll in radians per frame, weighted like a shift of half the width.
        roll = ((xs * dy - ys * dx) / radius).mean() * width / 2
        speed[i] = np.log1p(np.sqrt(dx.mean() ** 2 + dy.mean() ** 2 + roll**2))
    return speed


def detrend(x: np.ndarray) -> np.ndarray:
    """Minus a running median, z-scored, so only the changes count."""
    window = int(TREND * RATE)
    step = window // 10
    centers = np.arange(0, len(x), step)
    medians = np.array(
        [np.nanmedian(x[max(0, c - window // 2) : c + window // 2]) for c in centers]
    )
    x = x - np.interp(np.arange(len(x)), centers, medians)
    return (x - np.nanmean(x)) / np.nanstd(x)


def motion(path: Path, crop: str) -> np.ndarray:
    """The detrended motion signal of a recording at RATE, cached."""
    stat = path.stat()
    key = json.dumps([stat.st_size, stat.st_mtime, crop, SYNC_VERSION, RATE, WIDTH])
    digest = hashlib.sha1(key.encode()).hexdigest()[:12]
    cache = CACHE_DIR / f"{path.name}.motion-{digest}.npy"
    if cache.exists():
        return np.load(cache)
    signal = detrend(flow_speed(frames(path, crop)))
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    np.save(cache, signal)
    return signal


def ncc(a: np.ndarray, b: np.ndarray, min_overlap: int):
    """Normalised cross-correlation of b against a by lag (b[i + lag] ~ a[i]),
    ignoring NaNs; NaN where fewer than min_overlap samples overlap."""
    size = 1 << (len(a) + len(b) - 2).bit_length()

    def correlate(x, y):
        out = np.fft.irfft(np.conj(np.fft.rfft(x, size)) * np.fft.rfft(y, size), size)
        return np.r_[out[size - len(a) + 1 :], out[: len(b)]]

    ma, mb = np.isfinite(a).astype(float), np.isfinite(b).astype(float)
    a0, b0 = np.nan_to_num(a), np.nan_to_num(b)
    count = np.rint(correlate(ma, mb))
    sa, sb = correlate(a0, mb), correlate(ma, b0)
    with np.errstate(invalid="ignore", divide="ignore"):
        cov = correlate(a0, b0) - sa * sb / count
        var_a = correlate(a0**2, mb) - sa**2 / count
        var_b = correlate(ma, b0**2) - sb**2 / count
        r = cov / np.sqrt(var_a * var_b)
    r[(count < min_overlap) | ~np.isfinite(r)] = np.nan
    return np.arange(-len(a) + 1, len(b)), r


def best_lag(lags: np.ndarray, r: np.ndarray) -> tuple[float, float, float]:
    """Sub-sample lag of the peak, its r, and the best r away from it."""
    if np.isnan(r).all():
        return np.nan, np.nan, np.nan
    k = int(np.nanargmax(r))
    lag = float(lags[k])
    if 0 < k < len(r) - 1 and np.isfinite(r[k - 1 : k + 2]).all():
        y0, y1, y2 = r[k - 1 : k + 2]
        if (curve := y0 - 2 * y1 + y2) < 0:
            lag += 0.5 * (y0 - y2) / curve
    rest = r.copy()
    exclude = int(EXCLUDE * RATE)
    rest[max(0, k - exclude) : k + exclude + 1] = np.nan
    second = float(np.nanmax(rest)) if np.isfinite(rest).any() else 0.0
    return lag / RATE, float(r[k]), second


@dataclass
class Match:
    dvr: str
    camera: str
    offset: float  # camera time = DVR time + offset
    r: float
    ratio: float
    clock: float  # the goggle clock error it implies
    anchor: bool = False


@dataclass
class Sync:
    # Goggle clock + clock = real time; None without a confident match.
    clock: float | None = None
    # DVR file -> camera file -> offset (camera time = DVR time + offset).
    offsets: dict[str, dict[str, float]] = field(default_factory=dict)
    matches: list[Match] = field(default_factory=list)
    # Camera files that overlap none of the DVR files.
    unused: list[str] = field(default_factory=list)


def sync(dvrs: list[Path], cameras: list[Path]) -> Sync:
    if not dvrs or not cameras:
        return Sync(unused=[path.name for path in cameras])
    lengths = {p: duration(p) for p in [*dvrs, *cameras]}
    jobs = [(p, DVR_CROP) for p in dvrs] + [(p, "") for p in cameras]
    # OpenCV and ffmpeg release the GIL.
    with ThreadPoolExecutor(max_workers=max(1, (os.cpu_count() or 4) // 2)) as pool:
        signals = dict(zip([p for p, _ in jobs], pool.map(lambda j: motion(*j), jobs)))
    goggle = {p: p.stat().st_mtime - lengths[p] for p in dvrs}
    camera = {p: camera_start(p) for p in cameras}

    matches = []
    for d in dvrs:
        for c in cameras:
            lags, r = ncc(signals[d], signals[c], int(MIN_OVERLAP * RATE))
            offset, best, second = best_lag(lags, r)
            if not np.isfinite(offset):
                continue
            clock = camera[c] + offset - goggle[d]
            ratio = best / second if second > 0 else np.inf
            matches.append(Match(d.name, c.name, offset, best, ratio, clock))

    confident = [m for m in matches if m.ratio >= MIN_RATIO and m.r >= MIN_R]
    if not confident:
        return Sync(matches=matches, unused=[c.name for c in cameras])
    # The clock most confident matches agree on.
    votes = [
        [n for n in confident if abs(n.clock - m.clock) <= CLOCK_TOLERANCE]
        for m in confident
    ]
    agreeing = max(votes, key=len)
    clock = float(np.median([m.clock for m in agreeing]))
    for m in agreeing:
        m.anchor = True

    result = Sync(clock=clock, matches=matches)
    for d in dvrs:
        for c in cameras:
            offset = goggle[d] + clock - camera[c]
            low, high = max(0.0, -offset), min(lengths[d], lengths[c] - offset)
            if high - low < MIN_COVER:
                continue
            anchor = next(
                (m for m in agreeing if m.dvr == d.name and m.camera == c.name), None
            )
            if anchor is not None:
                offset = anchor.offset
            else:
                offset = refine(signals[d], signals[c], offset)
            result.offsets.setdefault(d.name, {})[c.name] = round(float(offset), 3)
    used = {c for cameras in result.offsets.values() for c in cameras}
    result.unused = [c.name for c in cameras if c.name not in used]
    return result


def refine(a: np.ndarray, b: np.ndarray, predicted: float) -> float:
    """The best lag within REFINE of the clock's prediction, or the prediction."""
    lags, r = ncc(a, b, int(MIN_REFINE_OVERLAP * RATE))
    near = np.abs(lags / RATE - predicted) <= REFINE
    offset, best, _ = best_lag(lags[near], r[near])
    return offset if np.isfinite(offset) and best >= MIN_R else predicted


def describe(result: Sync) -> list[str]:
    lines = []
    if result.clock is None:
        lines.append("no confident camera match; the camera stays unused")
    else:
        anchors = [m for m in result.matches if m.anchor]
        spread = max(m.clock for m in anchors) - min(m.clock for m in anchors)
        # Whole days (the date) plus or minus the time of day.
        days, rest = divmod(round(result.clock), 86400)
        if rest > 43200:
            days, rest = days + 1, rest - 86400
        sign = "-" if rest < 0 else "+"
        time = datetime.timedelta(seconds=abs(rest))
        lines.append(
            f"goggle clock behind by {days} days {sign}{time} "
            f"({len(anchors)} match(es) agree within {spread:.1f}s)"
        )
    for dvr, cameras in result.offsets.items():
        for camera, offset in cameras.items():
            match = next(
                (m for m in result.matches if (m.dvr, m.camera) == (dvr, camera)), None
            )
            how = (
                f"matched, r {match.r:.2f}, ratio {match.ratio:.1f}"
                if match and match.anchor
                else "placed by the clock"
            )
            lines.append(f"{dvr} -> {camera}: {offset:+.3f}s ({how})")
    return lines


def main():
    parser = argparse.ArgumentParser(description="Sync goggle and camera recordings")
    parser.add_argument("--dvr", nargs="+", type=Path, required=True)
    parser.add_argument("--camera", nargs="+", type=Path, required=True)
    args = parser.parse_args()
    result = sync(sorted(args.dvr), sorted(args.camera))
    print("\n".join(describe(result)))
    if result.unused:
        print(f"unused: {', '.join(result.unused)}")


if __name__ == "__main__":
    main()
