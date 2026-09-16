#!/usr/bin/env python3
"""
Show what an upload would publish or unpublish, so nothing is released by accident.

`./site upload` is a plain `rsync --delete` of public/, so dropping `draft: true`
from a post, a future `date` arriving, or a `date` going missing publishes or
unpublishes an article with no warning -- and RSS readers pick new items up the
moment they land. This script compares the feed and sitemap of the fresh build
against copies of the ones last uploaded and lists the articles and pages that
differ; `./site upload` asks for confirmation when the list is not empty.

The baseline is a copy taken after the previous successful upload (`record`),
kept in .cache/ next to the mtime manifest. It is not git (public/ isn't in it)
and not the live site (the check should work offline and not depend on what
another deploy path may have put there).

Usage:
    release_diff.py check    exit 0 = no changes, 1 = changes printed,
                             2 = nothing to compare (no build, or no baseline yet)
    release_diff.py record   copy the built feed and sitemap into the baseline
"""

import shutil
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).parent.parent
PUBLIC = ROOT / "public"
BASELINE = ROOT / ".cache" / "release"
FILES = ("feed.xml", "sitemap.xml")

SITEMAP_NS = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}


def normalize(url: str) -> str:
    """Comparison key: scheme and host case-insensitive, trailing slash ignored."""
    parts = urlsplit(url.strip())
    return f"{parts.scheme.lower()}://{parts.netloc.lower()}{parts.path.rstrip('/')}"


def parse_feed(data: bytes) -> dict[str, tuple[str, str]]:
    """Map normalized link -> (title, link) for every item in an RSS feed.

    Items are found under channel/ deliberately: the channel has a <link> of its
    own that a bare search would sweep up.
    """
    items = {}
    for item in ET.fromstring(data).findall("./channel/item"):
        link = item.findtext("link", "")
        items[normalize(link)] = (item.findtext("title", ""), link)
    return items


def parse_sitemap(data: bytes) -> dict[str, str]:
    """Map normalized loc -> loc for every URL in a sitemap."""
    locs = {}
    for loc in ET.fromstring(data).findall("sm:url/sm:loc", SITEMAP_NS):
        locs[normalize(loc.text or "")] = loc.text or ""
    return locs


def missing(directory: Path, hint: str) -> bool:
    absent = [name for name in FILES if not (directory / name).is_file()]
    if absent:
        where = directory.relative_to(ROOT)
        print(
            f"ERROR: {', '.join(absent)} missing in {where}/: {hint}", file=sys.stderr
        )
    return bool(absent)


def section(heading: str, lines: list[str]) -> None:
    if lines:
        print(f"{heading} ({len(lines)}):")
        for line in lines:
            print(f"  {line}")


def check() -> int:
    if missing(PUBLIC, "run ./site build first."):
        return 2
    if missing(BASELINE, "no baseline yet, the first upload records one."):
        return 2

    try:
        feed_now = parse_feed((PUBLIC / "feed.xml").read_bytes())
        feed_then = parse_feed((BASELINE / "feed.xml").read_bytes())
        sitemap_now = parse_sitemap((PUBLIC / "sitemap.xml").read_bytes())
        sitemap_then = parse_sitemap((BASELINE / "sitemap.xml").read_bytes())
    except ET.ParseError as e:
        print(f"ERROR: could not parse feed or sitemap: {e}", file=sys.stderr)
        return 2

    feed_added = sorted(feed_now.keys() - feed_then.keys())
    feed_removed = sorted(feed_then.keys() - feed_now.keys())
    # Every new post is also a new sitemap URL; report it once, with its title.
    feed_urls = set(feed_added) | set(feed_removed)
    pages_added = sorted(sitemap_now.keys() - sitemap_then.keys() - feed_urls)
    pages_removed = sorted(sitemap_then.keys() - sitemap_now.keys() - feed_urls)

    if not (feed_added or feed_removed or pages_added or pages_removed):
        print("No feed or sitemap changes since the last upload.")
        return 0

    section(
        "Feed articles to be published",
        [f"+ {feed_now[k][0]}  {feed_now[k][1]}" for k in feed_added],
    )
    section(
        "Feed articles to be removed",
        [f"- {feed_then[k][0]}  {feed_then[k][1]}" for k in feed_removed],
    )
    section("Other sitemap pages added", [f"+ {sitemap_now[k]}" for k in pages_added])
    section(
        "Other sitemap pages removed", [f"- {sitemap_then[k]}" for k in pages_removed]
    )
    return 1


def record() -> int:
    if missing(PUBLIC, "run ./site build first."):
        return 2
    BASELINE.mkdir(parents=True, exist_ok=True)
    for name in FILES:
        shutil.copyfile(PUBLIC / name, BASELINE / name)
    print(f"Recorded feed and sitemap baseline in {BASELINE.relative_to(ROOT)}/.")
    return 0


def main() -> int:
    command = sys.argv[1] if len(sys.argv) == 2 else None
    if command == "check":
        return check()
    if command == "record":
        return record()
    print(f"Usage: {Path(sys.argv[0]).name} check|record", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
