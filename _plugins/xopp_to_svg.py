#!/usr/bin/python3

import argparse
import glob
import os
import sys
from re import search, sub
from subprocess import DEVNULL, PIPE, Popen
from tempfile import NamedTemporaryFile  # for reading Xournal++ output
from typing import *


def crop_svg(contents: str) -> None:
    """Crop the specified .svg file."""
    # I wanted to match anything, including the newline, but was lazy to do it properly
    # this is extremely brittle but I'm to lazy to do it properly
    contents = sub("<clipPath([^á]*?)</clipPath>", "", contents)
    contents = sub("<path([^á]*?)\/>", "", contents, count=4)

    return contents


def get_argument_parser() -> argparse.ArgumentParser:
    """Returns the ArgumentParser object for the script."""
    parser = argparse.ArgumentParser(
        description="Convert Xournal++ files to SVGs.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    # svg margins
    parser.add_argument(
        "-m",
        "--margins",
        dest="margins",
        metavar="M",
        type=int,
        default=15,
        help="the margins around the cropped Xournal++ files (in points, default 15)",
    )

    # compress
    parser.add_argument(
        "-c",
        "--compress",
        dest="compress",
        action="store_true",
        default=True,
        help="whether not to compress the SVG (on by default)",
    )

    # either convert all files or only specific files
    group = parser.add_mutually_exclusive_group(required=True)

    # all files
    group.add_argument(
        "-a",
        "--all-files",
        dest="files",
        default=[],
        action="store_const",
        const=glob.glob("*.xopp"),
        help="convert all .xopp files in the working directory",
    )

    # only specific files
    group.add_argument(
        "-i",
        "-f",
        "--files",
        dest="files",
        default=[],
        metavar="F",
        nargs="+",
        help="the name(s) of the .xopp file(s) to convert to SVG",
    )

    return parser


# get the parser and parse the commands
parser = get_argument_parser()
arguments = parser.parse_args()


# go through the specified markdown files
for i, name in enumerate(arguments.files):
    # check if the file exists
    if not os.path.exists(name):
        print(f"'{name}' not found, skipping.", flush=True)
        continue

    # get the svg from Xournal++, storing it in a temporary file
    tmp = NamedTemporaryFile(mode="w+", suffix=".pdf")
    Popen(["xournalpp", f"--create-pdf={tmp.name}", name], stderr=DEVNULL).communicate()

    tmp2 = NamedTemporaryFile(mode="w+", suffix=".svg")
    Popen(["inkscape", f"--export-filename={tmp2.name}", tmp.name], stderr=DEVNULL).communicate()

    # crop the SVG
    cropped_svg = crop_svg(tmp2.read())

    out_name = name[:-4] + "svg"
    with open(out_name, "w") as f:
        f.write(cropped_svg)

    Popen(["inkscape", f"--export-filename={out_name}", "--export-area-drawing", out_name], stderr=DEVNULL).communicate()

    if arguments.compress:
        Popen(["_plugins/svgcleaner/svgcleaner", out_name, out_name], stdin=PIPE, stdout=PIPE, stderr=PIPE).communicate()

    print(f"{name} -> {out_name}", flush=True)

