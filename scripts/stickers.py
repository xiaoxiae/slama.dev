#!/usr/bin/env python3
"""
Build the interactive sticker sheet from content/stickers/stickers.svg.

A sticker is a <g> holding exactly two things: the artwork and a <text> with the
commentary (first line the title, blank line a new paragraph). The drawing is
emitted inline, the commentary as HTML captions below it. Every interaction is
CSS. Inkscape is optional. CLAUDE.md explains the arrangement.

Usage:
    uv run scripts/stickers.py
"""

import hashlib
import html
import json
import re
import shutil
import subprocess
import sys
import tempfile
from base64 import b64decode
from pathlib import Path

import markdown
import numpy as np
from PIL import Image
from lxml import etree
from unidecode import unidecode

ROOT = Path(__file__).parent.parent
SOURCE = ROOT / "content" / "stickers" / "stickers.svg"
OUTPUT = ROOT / "assets" / "stickers" / "stickers.html"
IMAGE_DIR = ROOT / "static" / "stickers-img"
IMAGE_URL = "/stickers-img"
# Same place subset_fonts.py caches; gitignored, safe to delete.
HULL_CACHE = ROOT / ".cache" / "sticker-hulls.json"

SVG = "http://www.w3.org/2000/svg"
INKSCAPE = "http://www.inkscape.org/namespaces/inkscape"
SODIPODI = "http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
XLINK = "http://www.w3.org/1999/xlink"

DATA_URI = re.compile(r"^data:image/(png|jpe?g|webp);base64,(.*)$", re.DOTALL)

# Inkscape reports px; the drawing's user unit is the millimetre.
PX_PER_USER_UNIT = 96 / 25.4

HOVER_SCALE = 1.15
FOCUS_COVERAGE = 0.5

HULL_RENDER_SIZE = 320
HULL_ALPHA_FLOOR = 8


def q(namespace: str, tag: str) -> str:
    return f"{{{namespace}}}{tag}"


def warn(message: str) -> None:
    print(f"  warning: {message}", file=sys.stderr)


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", unidecode(text).lower()).strip("-")
    return slug[:60].strip("-") or "sticker"


def commentary_of(group) -> tuple[object, object] | None:
    """The group's (commentary, artwork), if it is shaped like a sticker."""
    children = [child for child in group if isinstance(child.tag, str)]

    if len(children) != 2:
        return None

    texts = [child for child in children if child.tag == q(SVG, "text")]

    if len(texts) != 1:
        return None

    return texts[0], next(c for c in children if c is not texts[0])


def read_lines(text_element) -> list[str]:
    """One string per line. Direct <tspan> children only, so styled runs
    inside a line aren't read twice."""
    spans = [child for child in text_element if child.tag == q(SVG, "tspan")]
    sources = spans or [text_element]

    return ["".join(source.itertext()).strip() for source in sources]


def to_paragraphs(lines: list[str]) -> list[str]:
    """Join consecutive lines into paragraphs, splitting on blank lines."""
    paragraphs = []
    current = []

    for line in lines:
        if line:
            current.append(line)
        elif current:
            paragraphs.append(" ".join(current))
            current = []

    if current:
        paragraphs.append(" ".join(current))

    return paragraphs


def find_stickers(svg) -> list[dict]:
    found = []

    for group in svg.iter(q(SVG, "g")):
        if group.get(q(INKSCAPE, "groupmode")) == "layer":
            continue

        parts = commentary_of(group)
        if parts is not None:
            found.append((group, *parts))

    groups = {id(group) for group, _, _ in found}
    stickers = []

    for group, text, artwork in found:
        # Nested means artwork paired with the drawing's own lettering.
        if any(id(a) in groups for a in group.iterancestors()):
            warn(
                f"group {group.get('id')!r} sits inside another sticker; ignored "
                "(its text is probably part of the drawing, not a description)"
            )
            continue

        lines = read_lines(text)
        title = lines[0] if lines else ""

        # Never painted, even when unusable.
        group.remove(text)

        if not title:
            warn(f"group {group.get('id')!r} has an empty commentary; ignored")
            continue

        stickers.append(
            {
                "group": group,
                "artwork": artwork,
                "title": title,
                "paragraphs": to_paragraphs(lines[1:]),
            }
        )

    return stickers


def canvas_size(svg) -> tuple[float, float]:
    view_box = (svg.get("viewBox") or "").split()

    if len(view_box) == 4:
        try:
            return float(view_box[2]), float(view_box[3])
        except ValueError:
            pass

    return 1920.0, 1080.0


def extract_images(svg) -> int:
    """Link the embedded images from static/ instead of inlining their bytes."""
    count = 0

    for image in svg.iter(q(SVG, "image")):
        for attribute in (q(XLINK, "href"), "href"):
            match = DATA_URI.match(image.get(attribute) or "")
            if not match:
                continue

            suffix, payload = match.group(1), match.group(2)
            data = b64decode(payload)
            name = f"{hashlib.sha1(data).hexdigest()[:16]}.{suffix}"

            IMAGE_DIR.mkdir(parents=True, exist_ok=True)
            target = IMAGE_DIR / name
            if not target.exists():
                target.write_bytes(data)

            image.set(attribute, f"{IMAGE_URL}/{name}")
            count += 1

    return count


def query_boxes() -> dict[str, tuple[float, float, float, float]]:
    """Every object's bounding box, in user units."""
    if shutil.which("inkscape") is None:
        warn("inkscape not found; stickers will not enlarge, and hovering is fiddlier")
        return {}

    try:
        result = subprocess.run(
            ["inkscape", "--query-all", str(SOURCE)],
            capture_output=True,
            text=True,
            timeout=120,
            check=True,
        )
    except (subprocess.SubprocessError, OSError) as error:
        warn(f"inkscape --query-all failed ({error}); stickers will not enlarge")
        return {}

    boxes = {}

    for line in result.stdout.splitlines():
        fields = line.rsplit(",", 4)
        if len(fields) != 5:
            continue
        try:
            boxes[fields[0]] = tuple(
                float(field) / PX_PER_USER_UNIT for field in fields[1:]
            )
        except ValueError:
            continue

    return boxes


def convex_hull(points: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """Andrew's monotone chain. Returns the hull counter-clockwise."""
    pts = sorted(set(points))

    if len(pts) < 3:
        return pts

    def half(sequence):
        out = []
        for p in sequence:
            while len(out) >= 2:
                (ox, oy), (ax, ay) = out[-2], out[-1]
                if (ax - ox) * (p[1] - oy) - (ay - oy) * (p[0] - ox) <= 0:
                    out.pop()
                else:
                    break
            out.append(p)
        return out

    return half(pts)[:-1] + half(pts[::-1])[:-1]


def trace_hull(element_id: str, box, work: Path) -> list[tuple[float, float]] | None:
    """Trace a sticker's outline by rendering it and hulling its pixels.

    Hovering the artwork alone drops through the gaps between logos.
    """
    png = work / f"{element_id}.png"
    x, y, width, height = box

    longest = (
        f"--export-width={HULL_RENDER_SIZE}"
        if width >= height
        else f"--export-height={HULL_RENDER_SIZE}"
    )

    try:
        subprocess.run(
            [
                "inkscape",
                f"--export-id={element_id}",
                "--export-id-only",
                "--export-type=png",
                f"--export-filename={png}",
                longest,
                str(SOURCE),
            ],
            capture_output=True,
            timeout=120,
            check=True,
        )
    except (subprocess.SubprocessError, OSError):
        return None

    if not png.exists():
        return None

    alpha = np.array(Image.open(png).convert("RGBA"))[..., 3]
    rows, columns = np.where(alpha > HULL_ALPHA_FLOOR)

    if len(rows) < 3:
        return None

    # Only each column's topmost and bottommost pixel can be on the hull.
    extremes = {}
    for column, row in zip(columns.tolist(), rows.tolist()):
        low, high = extremes.get(column, (row, row))
        extremes[column] = (min(low, row), max(high, row))

    cloud = [(c, lo) for c, (lo, _) in extremes.items()]
    cloud += [(c, hi) for c, (_, hi) in extremes.items()]

    png_height, png_width = alpha.shape

    return [
        (x + px * width / png_width, y + py * height / png_height)
        for px, py in convex_hull(cloud)
    ]


def hull_cache_key(artwork, box) -> str:
    digest = hashlib.sha256()
    digest.update(etree.tostring(artwork))
    digest.update(",".join(f"{v:.2f}" for v in box).encode())
    digest.update(f"{HULL_RENDER_SIZE}:{HULL_ALPHA_FLOOR}".encode())
    return digest.hexdigest()


def read_hull_cache() -> dict[str, list]:
    try:
        return json.loads(HULL_CACHE.read_text())
    except (OSError, json.JSONDecodeError):
        return {}


def trace_outlines(stickers: list[dict]) -> tuple[int, int]:
    """Outline every measured sticker; returns (traced, reused).

    Serial on purpose: concurrent Inkscape exports abort on a random subset.
    """
    measured = [s for s in stickers if s["box"] and s["artwork"].get("id")]

    if not measured or shutil.which("inkscape") is None:
        return 0, 0

    remembered = read_hull_cache()
    keep = {}
    traced = reused = 0

    with tempfile.TemporaryDirectory() as work:
        for sticker in measured:
            key = sticker["key"]
            outline = remembered.get(key)

            if outline is None:
                traced += 1
                outline = trace_hull(
                    sticker["artwork"].get("id"), sticker["box"], Path(work)
                )
                if outline is None:
                    # An abort is transient; a real failure happens twice.
                    outline = trace_hull(
                        sticker["artwork"].get("id"), sticker["box"], Path(work)
                    )
            else:
                reused += 1

            if outline:
                sticker["outline"] = outline
                keep[key] = outline

    # Only what this run used, so the file cannot grow without bound.
    try:
        HULL_CACHE.parent.mkdir(parents=True, exist_ok=True)
        HULL_CACHE.write_text(json.dumps(keep))
    except OSError as error:
        warn(f"could not save the traced outlines ({error}); they will be redone")

    return traced, reused


def transforms_for(box, canvas) -> tuple[str, str]:
    x, y, width, height = box
    cx, cy = x + width / 2, y + height / 2
    canvas_width, canvas_height = canvas

    k = HOVER_SCALE
    hover = f"translate({cx * (1 - k):.3f}px, {cy * (1 - k):.3f}px) scale({k})"

    # min() rather than max() so a wide sticker doesn't overflow top and bottom.
    scale = FOCUS_COVERAGE * min(canvas_width / width, canvas_height / height)
    focus = (
        f"translate({canvas_width / 2 - scale * cx:.3f}px, "
        f"{canvas_height / 2 - scale * cy:.3f}px) scale({scale:.4f})"
    )

    return hover, focus


def ancestor_transform(node, root) -> str:
    """Transforms inherited from above, outermost first: a <use> drops them."""
    transforms = []
    node = node.getparent()

    while node is not None and node is not root:
        transform = node.get("transform")
        if transform:
            transforms.append(transform)
        node = node.getparent()

    return " ".join(reversed(transforms))


def build_front(sticker: dict, svg) -> object:
    group = sticker["group"]

    if group.get("id") is None:
        group.set("id", f"sticker-{sticker['slug']}")

    front = etree.Element(q(SVG, "g"))
    front.set("class", "sticker-front")
    front.set("data-front", sticker["slug"])
    front.set("pointer-events", "none")
    front.set("aria-hidden", "true")

    inherited = ancestor_transform(group, svg)
    if inherited:
        carrier = etree.SubElement(front, q(SVG, "g"))
        carrier.set("transform", inherited)
    else:
        carrier = front

    etree.SubElement(carrier, q(SVG, "use")).set("href", f"#{group.get('id')}")

    return front


def append_hit_area(sticker: dict, svg) -> None:
    """Append the shape that takes the pointer; nothing else in the sheet does."""
    slug = sticker["slug"]

    if sticker.get("outline"):
        shape = etree.SubElement(svg, q(SVG, "polygon"))
        shape.set("points", " ".join(f"{x:.2f},{y:.2f}" for x, y in sticker["outline"]))
    elif sticker["box"]:
        shape = etree.SubElement(svg, q(SVG, "rect"))
        x, y, width, height = sticker["box"]
        shape.set("x", f"{x:.2f}")
        shape.set("y", f"{y:.2f}")
        shape.set("width", f"{width:.2f}")
        shape.set("height", f"{height:.2f}")
        warn(f"{slug!r}: could not trace an outline; using its bounding box")
    else:
        # Unmeasured: the artwork becomes its own hit target. Wrap rather than
        # tag -- the copy <use>s it and would inherit `pointer-events: all`.
        artwork = sticker["group"]
        shape = etree.Element(q(SVG, "g"))
        parent = artwork.getparent()
        shape.tail, artwork.tail = artwork.tail, None
        parent.replace(artwork, shape)
        shape.append(artwork)
        warn(f"{slug!r}: not measured; hovering will only catch its artwork")

    shape.set("class", f"{shape.get('class', '')} sticker".strip())
    shape.set("data-sticker", slug)
    shape.set("tabindex", "0")
    shape.set("role", "img")
    shape.set("aria-label", sticker["title"])
    shape.set("aria-describedby", f"cap-{slug}")


def append_scrim(svg, canvas) -> None:
    scrim = etree.SubElement(svg, q(SVG, "rect"))
    scrim.set("class", "stickers-scrim")
    scrim.set("x", "0")
    scrim.set("y", "0")
    scrim.set("width", f"{canvas[0]:g}")
    scrim.set("height", f"{canvas[1]:g}")
    scrim.set("pointer-events", "none")


def rules_for(sticker: dict) -> str:
    slug = sticker["slug"]

    # Covers the caption too: pressing the mouse on a link blurs the sticker.
    engaged = (
        f'.stickers:has([data-sticker="{slug}"]:focus, '
        f'[data-caption="{slug}"]:hover, [data-caption="{slug}"]:focus-within)'
    )
    idle = (
        ".stickers:not(:has(.sticker:focus, .stickers-caption-item:hover, "
        ".stickers-caption-item:focus-within))"
    )

    grow = f" transform: {sticker['hover']};" if sticker["hover"] else ""
    fly = f" transform: {sticker['focus']};" if sticker["focus"] else ""

    return "\n".join(
        [
            f'{idle}:has([data-sticker="{slug}"]:hover) [data-caption="{slug}"],\n'
            f'{engaged} [data-caption="{slug}"] '
            "{ opacity: 1; visibility: visible; }",
            f'{idle}:has([data-sticker="{slug}"]:hover) [data-front="{slug}"] '
            f"{{ opacity: 1;{grow} }}",
            f'{engaged} [data-front="{slug}"] {{ opacity: 1;{fly} }}',
            f'{idle}:has([data-sticker="{slug}"]:hover) [data-art="{slug}"],\n'
            f'{engaged} [data-art="{slug}"] '
            "{ opacity: 0; }",
        ]
    )


def render(stickers: list[dict], sheet: str) -> str:
    captions = "\n".join(
        f'    <div class="stickers-caption-item" tabindex="-1" '
        f'id="cap-{s["slug"]}" data-caption="{s["slug"]}">'
        f"<strong>{html.escape(s['title'])}</strong>"
        f"{markdown.markdown('\n\n'.join(s['paragraphs']))}</div>"
        for s in stickers
    )

    return (
        "<style>\n" + "\n".join(rules_for(s) for s in stickers) + "\n</style>\n"
        f"{sheet}\n"
        '<div class="stickers-captions">\n'
        '    <div class="stickers-caption-placeholder">'
        "Hover a sticker to read about it.</div>\n"
        f"{captions}\n"
        "</div>\n"
    )


def main() -> int:
    if not SOURCE.exists():
        print(f"ERROR: {SOURCE.relative_to(ROOT)} not found.", file=sys.stderr)
        return 1

    boxes = query_boxes()

    tree = etree.parse(str(SOURCE))
    svg = tree.getroot()

    # Editor state, several KB of it.
    for namedview in svg.findall(q(SODIPODI, "namedview")):
        svg.remove(namedview)

    images = extract_images(svg)
    canvas = canvas_size(svg)
    stickers = find_stickers(svg)
    used_slugs = {}

    for sticker in stickers:
        slug = slugify(sticker["title"])

        used_slugs[slug] = used_slugs.get(slug, 0) + 1
        if used_slugs[slug] > 1:
            slug = f"{slug}-{used_slugs[slug]}"

        sticker["slug"] = slug
        # Stays under the scrim, so it dims with the rest of the drawing.
        sticker["group"].set("data-art", slug)

        box = boxes.get(sticker["artwork"].get("id") or "")
        sticker["box"] = box if box and box[2] > 0 and box[3] > 0 else None
        sticker["key"] = (
            hull_cache_key(sticker["artwork"], box) if sticker["box"] else None
        )
        sticker["hover"], sticker["focus"] = (
            transforms_for(sticker["box"], canvas) if sticker["box"] else ("", "")
        )

        if not sticker["box"] and boxes:
            warn(f"{slug!r}: no bounding box; it will not enlarge on click")

    traced, reused = trace_outlines(stickers)

    if stickers:
        fronts = [build_front(sticker, svg) for sticker in stickers]

        append_scrim(svg, canvas)
        for sticker in stickers:
            append_hit_area(sticker, svg)
        for front in fronts:
            svg.append(front)

    # Otherwise it renders at its physical size instead of scaling.
    for attribute in ("width", "height"):
        svg.attrib.pop(attribute, None)
    svg.set("class", "stickers-sheet")

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(render(stickers, etree.tostring(svg, encoding="unicode")))

    print(
        f"Generated {OUTPUT.relative_to(ROOT)}: {len(stickers)} sticker(s), "
        f"{traced + reused} outlined ({traced} traced, {reused} cached), "
        f"{images} image(s) extracted, {OUTPUT.stat().st_size / 1024 / 1024:.2f} MiB"
    )

    return 0


if __name__ == "__main__":
    sys.exit(main())
