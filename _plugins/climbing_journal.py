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
"""

current_year = None

for entry in reversed(sorted(list(journal))):
    line = ""

    if current_year != entry.year:
        if current_year is None:
            line += f"<details open class='climbing-year-details'><summary><h3>{entry.year}</h3></summary> <ul>"
        else:
            line += f"</ul></details> <details open class='climbing-year-details'><summary><h3>{entry.year}</h3></summary> <ul>"

        current_year = entry.year

    line += f"\n<li><p><strong>{entry.strftime('%-d. %-m. %Y')}</strong>"

    colors = ["red", "salmon", "blue", "yellow"]

    wall_colors = {
        "jungle": ["green", "blue", "red"],
        "boulder-bar": ["green", "blue", "red"],
        "třináctka": [f"V{i}" for i in range(4, 11)],
    }

    # v-graded climbing gyms will have the same color
    v_grading = set(["třináctka"])

    wall = ""
    wall_stub = ""

    if "wall" in journal[entry]:
        wall_stub = journal[entry]["wall"].lower().replace(" ", "-")
        wall = "-" + wall_stub

        colors = (
            {}
            if wall_stub not in wall_colors
            else wall_colors[wall_stub]
        )

    # locations have no colors since they are not walls; they get treated differently
    if "location" in journal[entry]:
        location = journal[entry]["location"]

        line += f" ({location})"

        if "guide" in journal[entry]:
            line += f" [<a href='/climbing/guides/{journal[entry]['guide']}'>guide</a>]"

        line += f": "

    else:
        if wall == "":
            wall_stub = "smíchoff"

        line += f" (at <img class='climbing-wall-logo' src='/climbing/wall-logos/{wall_stub}.svg'/>): "

    for color in list(colors) + ["other"]:
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

            if color == "other":
                line += f"<mark class='climbing-diary-record climbing-{color} climbing-{color}-text'>other: {count}"
            elif wall_stub in v_grading:
                line += f"<mark class='climbing-diary-record climbing-{color}{wall.replace(' ', '-')}'><strong>{color}:</strong> {count}"
            else:
                line += f"<mark class='climbing-diary-record climbing-{color}{wall.replace(' ', '-')} climbing-{color}{wall.replace(' ', '-')}-text'>{count}"

            if len(entry_videos) != 0:
                line += (
                    " ["
                    + ", ".join(
                        [
                            f"<a href='/climbing/videos/{name}'>{i + 1}{'↯' if 'flash' in videos[name] and videos[name]['flash'] else ''}</a>"
                            for i, name in enumerate(entry_videos)
                        ]
                    )
                    + "]"
                )

            line += "</mark> "

    line += "</p>"

    if "routes" in journal[entry]:
        line += f"<ul class='climbing-routes-list'>"
        for name, (difficulty, status) in journal[entry]["routes"]:
            line += f"<li><mark class='climbing-diary-record climbing-other climbing-other-text'>{name} ({difficulty}, {status})</mark></li>"
        line += f"</ul>"

    if "note" in journal[entry]:
        # the replace is a bit of a hack.
        # I should probably do proper conversion, but I don't really use anything special
        line += "<p>" + journal[entry]["note"].replace("--", "–").replace(":)", "🙂") + "</p>"

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
