#!/usr/bin/env python3
"""
Build the site's Font Awesome from the stock copy plus custom SVG icons.

Stock FA lives in assets/fontawesome/; the result goes to static/assets/fa/
(gitignored), which is what the site links. Every assets/fa-custom/NAME.svg
becomes the glyph of `fa-NAME`: an icon FA has is overridden in place, an
unknown name is added to the solid font as a new icon (use it with `fa-solid`).
subset_fonts.py later subsets this patched copy.

SVGs follow FA's own convention (an FA SVG download is a valid template): the
viewBox height maps to the 512-unit em, with the baseline 64 units up. Only
fills count -- convert strokes to paths -- and fonts fill with the nonzero rule.

Usage:
    uv run scripts/fontawesome.py             # build static/assets/fa/
    uv run scripts/fontawesome.py dump NAME…  # stock fa-NAME → fa-custom/NAME.svg

A dumped SVG is in font units, so it builds back into the identical glyph.
"""

import hashlib
import math
import re
import shutil
import sys
from pathlib import Path

from fontTools.misc.transform import Transform
from fontTools.pens.cu2quPen import Cu2QuPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.svgLib.path.parser import parse_path
from fontTools.svgLib.path.shapes import PathBuilder
from fontTools.ttLib import TTFont
from lxml import etree

ROOT = Path(__file__).parent.parent
STOCK = ROOT / "assets" / "fontawesome"
CUSTOM = ROOT / "assets" / "fa-custom"
OUTPUT = ROOT / "static" / "assets" / "fa"
# Same place subset_fonts.py caches; gitignored, safe to delete. Not in static/,
# which Hugo would publish.
STAMP = ROOT / ".cache" / "fontawesome.stamp"

# Fonts an override may land in, in order of preference; new icons go to the
# first. Solid and brands share some codepoints (digits, punctuation), and
# regular is a subset of solid, so each icon is patched in exactly one font.
FONTS = ["fa-solid-900", "fa-brands-400", "fa-regular-400", "fa-v4compatibility"]

# FA's em: 512 units, baseline 64 units above the bottom of the viewBox
EM, ASCENT = 512, 448

SKIPPED_ELEMENTS = {"defs", "clipPath", "mask", "symbol", "metadata", "title", "desc"}
SHAPES = {"path", "rect", "circle", "ellipse", "polygon", "polyline"}
NAME = re.compile(r"[a-z][-a-z0-9]*")


def warn(message: str) -> None:
    print(f"  WARNING: {message}")


def fa_codepoint(css: str, name: str) -> int | None:
    """The codepoint of icon `fa-NAME` in FA's CSS, handling alias lists like
    `.fa-bolt:before,.fa-zap:before{content:"\\f0e7"}`."""
    match = re.search(
        rf'\.fa-{re.escape(name)}:before[^{{]*\{{content:"\\([0-9a-fA-F]+)"\}}', css
    )
    return int(match.group(1), 16) if match else None


def parse_transform(value: str) -> Transform:
    """An SVG transform list as one Transform (applied right to left)."""
    result = Transform()
    for function, raw in re.findall(r"(\w+)\s*\(([^)]*)\)", value):
        args = [float(a) for a in re.split(r"[\s,]+", raw.strip()) if a]
        match function, args:
            case "matrix", [a, b, c, d, e, f]:
                t = Transform(a, b, c, d, e, f)
            case "translate", [x, *y]:
                t = Transform().translate(x, y[0] if y else 0)
            case "scale", [x, *y]:
                t = Transform().scale(x, y[0] if y else x)
            case "rotate", [angle]:
                t = Transform().rotate(math.radians(angle))
            case "rotate", [angle, cx, cy]:
                t = (
                    Transform()
                    .translate(cx, cy)
                    .rotate(math.radians(angle))
                    .translate(-cx, -cy)
                )
            case "skewX", [angle]:
                t = Transform(1, 0, math.tan(math.radians(angle)), 1, 0, 0)
            case "skewY", [angle]:
                t = Transform(1, math.tan(math.radians(angle)), 0, 1, 0, 0)
            case _:
                raise ValueError(f"unsupported transform {function}({raw})")
        result = result.transform(t)
    return result


def presentation(el, inherited: dict[str, str]) -> dict[str, str]:
    """The fill/stroke properties of an element, inheriting from its parents."""
    props = dict(inherited)
    for key in ("fill", "stroke", "fill-rule", "display"):
        if key in el.attrib:
            props[key] = el.attrib[key].strip()
    for declaration in el.attrib.get("style", "").split(";"):
        key, _, value = declaration.partition(":")
        if key.strip() in ("fill", "stroke", "fill-rule", "display"):
            props[key.strip()] = value.strip()
    return props


def draw_svg(path: Path, pen) -> int:
    """Draw an SVG's filled shapes onto a pen in FA's glyph space.

    Returns the advance width. Raises ValueError on SVGs that can't be used.
    """
    root = etree.parse(str(path)).getroot()
    if "viewBox" not in root.attrib:
        raise ValueError("no viewBox")
    vx, vy, vw, vh = (float(v) for v in re.split(r"[\s,]+", root.attrib["viewBox"]))
    scale = EM / vh
    viewport = Transform(scale, 0, 0, -scale, -vx * scale, ASCENT + vy * scale)

    shapes = 0

    def walk(el, transform: Transform, inherited: dict[str, str]):
        nonlocal shapes
        if not isinstance(el.tag, str):  # comments, processing instructions
            return
        tag = etree.QName(el).localname
        if tag in SKIPPED_ELEMENTS:
            return
        props = presentation(el, inherited)
        if props.get("display") == "none":
            return
        if "transform" in el.attrib:
            transform = transform.transform(parse_transform(el.attrib["transform"]))

        if tag in SHAPES:
            label = el.attrib.get("id", tag)
            if props.get("fill") == "none":
                if props.get("stroke", "none") != "none":
                    warn(f"{path.name}: {label} is stroke-only and is skipped")
                return
            if props.get("fill-rule") == "evenodd":
                warn(f"{path.name}: {label} uses evenodd, fonts fill nonzero")
            builder = PathBuilder()
            # Not add_path_from_element: it chokes on non-matrix transforms,
            # which are handled above instead.
            getattr(builder, f"_parse_{tag}")(el)
            for d in builder.paths:
                parse_path(d, TransformPen(pen, viewport.transform(transform)))
                shapes += 1

        for child in el:
            walk(child, transform, props)

    walk(root, Transform(), {})
    if not shapes:
        raise ValueError("no filled shapes")
    return round(vw * scale)


def make_glyph(path: Path, font: TTFont, glyph_name: str):
    """Draw an SVG into a new glyph `glyph_name` of a font."""
    glyph_pen = TTGlyphPen(None)
    advance = draw_svg(path, Cu2QuPen(glyph_pen, 1.0, reverse_direction=True))
    glyph = glyph_pen.glyph()
    glyf = font["glyf"]
    glyf[glyph_name] = glyph  # appends to the glyph order if new
    glyph.recalcBounds(glyf)
    font["hmtx"][glyph_name] = (advance, glyph.xMin)


def add_codepoint(font: TTFont, codepoint: int, glyph_name: str):
    for table in font["cmap"].tables:
        if table.isUnicode():
            table.cmap[codepoint] = glyph_name


def stamp_of(svgs: list[Path]) -> str:
    h = hashlib.sha256(Path(__file__).read_bytes())
    for file in [*sorted(STOCK.rglob("*")), *svgs]:
        if file.is_file():
            h.update(str(file.relative_to(ROOT)).encode() + b"\0")
            h.update(file.read_bytes())
    return h.hexdigest()


def load_stock() -> tuple[str, dict[str, TTFont], dict[str, dict[int, str]]]:
    css = (STOCK / "fa.min.css").read_text(encoding="utf-8")
    fonts = {
        name: TTFont(STOCK / "fonts" / f"{name}.ttf", recalcTimestamp=False)
        for name in FONTS
    }
    cmaps = {name: font.getBestCmap() or {} for name, font in fonts.items()}
    return css, fonts, cmaps


def find_icon(css: str, cmaps, name: str) -> tuple[int, str] | None:
    """The codepoint and font of a stock icon, or None if FA doesn't have it."""
    codepoint = fa_codepoint(css, name)
    if codepoint is None:
        return None
    font_name = next((f for f in FONTS if codepoint in cmaps[f]), None)
    if font_name is None:
        raise ValueError(f"U+{codepoint:04X} is in no FA font")
    return codepoint, font_name


def dump(names: list[str]):
    css, fonts, cmaps = load_stock()
    CUSTOM.mkdir(parents=True, exist_ok=True)
    for name in names:
        name = name.removeprefix("fa-")
        target = CUSTOM / f"{name}.svg"
        found = find_icon(css, cmaps, name)
        if found is None:
            sys.exit(f"  ERROR: fa-{name} is not in FA")
        if target.exists():
            sys.exit(f"  ERROR: {target.relative_to(ROOT)} already exists")
        codepoint, font_name = found
        font = fonts[font_name]
        glyph_name = cmaps[font_name][codepoint]
        pen = SVGPathPen(font.getGlyphSet(), ntos=lambda v: f"{v:g}")
        # Font units, y flipped: the build maps this viewBox back 1:1
        font.getGlyphSet()[glyph_name].draw(
            TransformPen(pen, Transform(1, 0, 0, -1, 0, ASCENT))
        )
        advance = font["hmtx"][glyph_name][0]
        target.write_text(
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {advance} {EM}">'
            f'<path d="{pen.getCommands()}"/></svg>\n'
        )
        print(f"  fa-{name} ({font_name}) → {target.relative_to(ROOT)}")


def build():
    svgs = sorted(CUSTOM.glob("*.svg"))
    stamp = stamp_of(svgs)
    if (
        STAMP.exists()
        and STAMP.read_text() == stamp
        and (OUTPUT / "fa.min.css").exists()
    ):
        print("  up to date")
        return

    css, fonts, cmaps = load_stock()
    taken = set().union(*cmaps.values())
    patched, new_rules, errors = set(), [], 0

    for svg in svgs:
        name = svg.stem
        try:
            if not NAME.fullmatch(name):
                raise ValueError("file name must be a lowercase icon name")
            if found := find_icon(css, cmaps, name):
                codepoint, font_name = found
                glyph_name = cmaps[font_name][codepoint]
                make_glyph(svg, fonts[font_name], glyph_name)
                print(f"  fa-{name}: overrides U+{codepoint:04X} in {font_name}")
            else:
                if re.search(rf"\.fa-{re.escape(name)}(?![-a-z0-9])", css):
                    raise ValueError(f"fa-{name} is an FA utility class")
                codepoint = max(c for c in range(0xE000, 0xF900) if c not in taken)
                taken.add(codepoint)
                font_name, glyph_name = FONTS[0], f"custom-{name}"
                make_glyph(svg, fonts[font_name], glyph_name)
                add_codepoint(fonts[font_name], codepoint, glyph_name)
                new_rules.append(f'.fa-{name}:before{{content:"\\{codepoint:x}"}}')
                print(f"  fa-{name}: new icon at U+{codepoint:04X} in {font_name}")
            patched.add(font_name)
        except ValueError as e:
            print(f"  ERROR: {svg.relative_to(ROOT)}: {e}")
            errors += 1
    if errors:
        sys.exit(1)

    shutil.rmtree(OUTPUT, ignore_errors=True)
    shutil.copytree(STOCK / "fonts", OUTPUT / "fonts")
    for name in sorted(patched):
        fonts[name].save(OUTPUT / "fonts" / f"{name}.ttf")
        fonts[name].flavor = "woff2"
        fonts[name].save(OUTPUT / "fonts" / f"{name}.woff2")
        # Cache-bust: browsers (and Hugo's CSS-only live reload) keep a font
        # whose URL hasn't changed
        version = hashlib.sha256(
            (OUTPUT / "fonts" / f"{name}.woff2").read_bytes()
        ).hexdigest()[:10]
        for ext in ("woff2", "ttf"):
            css = css.replace(
                f"url(fonts/{name}.{ext})", f"url(fonts/{name}.{ext}?v={version})"
            )
    (OUTPUT / "fa.min.css").write_text(css + "".join(new_rules), encoding="utf-8")

    STAMP.parent.mkdir(parents=True, exist_ok=True)
    STAMP.write_text(stamp)
    print(f"  {len(svgs)} custom icon(s) → {OUTPUT.relative_to(ROOT)}/")


if __name__ == "__main__":
    if sys.argv[1:2] == ["dump"]:
        dump(sys.argv[2:])
    else:
        build()
