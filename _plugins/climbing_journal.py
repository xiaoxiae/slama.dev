#!/usr/bin/env python3

import os
import shutil
from random import choice
from string import ascii_lowercase, digits
from typing import *
from subprocess import Popen, PIPE
from datetime import date

import yaml


os.chdir(os.path.dirname(os.path.realpath(__file__)))

CLIMBING_FOLDER = "../climbing/"
CLIMBING_VIDEOS_FOLDER = os.path.join(CLIMBING_FOLDER, "videos")
CLIMBING_INFO = os.path.join(CLIMBING_FOLDER, "videos.yaml")
CLIMBING_JOURNAL = os.path.join(CLIMBING_FOLDER, "journal.yaml")
OUTPUT_PATH = os.path.join("..", "_includes", "diary.md")

videos = {}
if os.path.exists(CLIMBING_INFO):
    with open(CLIMBING_INFO, "r") as f:
        videos = yaml.safe_load(f.read())

journal = {}
if os.path.exists(CLIMBING_JOURNAL):
    with open(CLIMBING_JOURNAL, "r") as f:
        journal = yaml.safe_load(f.read())

result = """
<div markdown="1" class="climbing-journal">
"""

for entry in reversed(sorted(list(journal))):
    line = f"- **{entry.strftime('%-d. %-m. %Y')}:** "

    for color in ["red", "salmon", "blue", "yellow"]:
        entry_videos = []
        for video in videos:
            if videos[video]["date"] == entry and videos[video]["color"] == color:
                entry_videos.append(video)

        if color in journal[entry]:
            line += f"<mark class='climbing-diary-record climbing-{color} climbing-{color}-text'>{journal[entry][color]}"

            if len(entry_videos) != 0:
                line += (
                    " ["
                    + ", ".join(
                        [
                            f"<a href='/climbing/videos/{name}'>{i + 1}</a>"
                            for i, name in enumerate(entry_videos)
                        ]
                    )
                    + "]"
                )

            line += "</mark> "

    if "note" in journal[entry]:
        line += "-- " + journal[entry]["note"]

    result += line + "\n"

result += "</div>"

with open(OUTPUT_PATH, "w") as f:
    f.write(result)

print("journal generated.", flush=True)
