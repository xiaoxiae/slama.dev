#!/usr/bin/env python3

import os
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

previous_date = None

for entry in reversed(sorted(list(journal))):
    line = f"\n<li><p><strong>{entry.strftime('%-d. %-m. %Y')}</strong>"

    colors = ["red", "salmon", "blue", "yellow"]

    location_colors = {
        "jungle": ["green", "blue", "red"],
        "třináctka": [f"V{i}" for i in range(4, 11)],
    }

    # v-graded climbing gyms will have the same color
    v_grading = set(["třináctka"])

    location = ""
    location_stub = ""

    if "location" in journal[entry]:
        location_stub = journal[entry]["location"].lower().replace(" ", "-")
        location = "-" + location_stub

        colors = (
            {}
            if location_stub not in location_colors
            else location_colors[location_stub]
        )

    if location == "":
        location_stub = "smíchoff"

    line += f" (at <img class='climbing-location-logo' src='/climbing/location-logos/{location_stub}.svg'/>): "

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

            if location_stub in v_grading:
                line += f"<mark class='climbing-diary-record climbing-{color}{location}'><strong>{color}:</strong> {count}"
            else:
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

    line += "</p>"

    if "note" in journal[entry]:
        # the replace is a bit of a hack.
        # I should probably do proper conversion, but I don't really use anything else
        line += "<p>" + journal[entry]["note"].replace("--", "–") + "</p>"

    line += "</li>"

    if "rebuilt" in journal[entry]:
        line += f"</ul><hr class='hr-text' data-content='new boulders (zone {journal[entry]['rebuilt']})'><ul>\n"

    result += line + "\n"

result += "</ul></div>"

with open(OUTPUT_PATH, "w") as f:
    f.write(result)

with open(CLIMBING_JOURNAL, "w") as f:
    f.write(yaml.dump(journal))

print("journal generated (and reformatted).", flush=True)
