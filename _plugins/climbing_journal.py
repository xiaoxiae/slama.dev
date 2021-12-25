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
<div class="climbing-journal">
<ul>
"""

for entry in reversed(sorted(list(journal))):
    line = f"\n<li><p><strong>{entry.strftime('%-d. %-m. %Y')}:</strong> "

    colors = ["red", "salmon", "blue", "yellow"]

    location_colors = {
        "jungle": ["green", "blue", "red"],
        "boulder-bar": [],
        "bigwall": [],
    }

    # location is Smíchoff by default, which has no postfix
    location = ""

    if "location" in journal[entry]:
        location_stub = journal[entry]["location"].lower().replace(" ", "-")
        location = "-" + location_stub

        colors = location_colors[location_stub]

    for color in colors:
        entry_videos = []
        for video in videos:
            if videos[video]["date"] == entry and videos[video]["color"] == color:
                entry_videos.append(video)

        if color in journal[entry]:
            color_dict = journal[entry][color]

            old_count = 0 if "old" not in color_dict else color_dict["old"]
            new_count = 0 if "new" not in color_dict else color_dict["new"]

            if old_count == 0:
                count = f"<span class='underline'>{new_count}</span>"
            elif new_count == 0:
                count = f"{old_count}"
            else:
                count = f"{old_count}/<span class='underline'>{new_count}</span>"

            line += f"<mark class='climbing-diary-record climbing-{color}{location} climbing-{color}{location}-text'>{count}"

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

    if location == "":
        location_stub = "smichoff"

    line += f"(at <img class='climbing-location-logo' src='/climbing/location-logos/{location_stub}.svg'/>)"

    line += "</p>"

    if "note" in journal[entry]:
        line += "<p>" + journal[entry]["note"] + "</p>"

    line += "</li>"

    if "rebuilt" in journal[entry]:
        line += "</ul><hr class='hr-text' data-content='new boulders'><ul>"

    result += line + "\n"

result += "</ul></div>"

with open(OUTPUT_PATH, "w") as f:
    f.write(result)

print("journal generated.", flush=True)
