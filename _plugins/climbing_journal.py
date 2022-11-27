#!/usr/bin/env python3

import os
import yaml
from unidecode import unidecode


class UniqueKeyLoader(yaml.SafeLoader):
    def construct_mapping(self, node, deep=False):
        mapping = []
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            assert key not in mapping, f"Duplicate key {key} in journal.yaml/videos.yaml."
            mapping.append(key)
        return super().construct_mapping(node, deep)


os.chdir(os.path.dirname(os.path.realpath(__file__)))

CLIMBING_FOLDER = "../climbing/"
CLIMBING_VIDEOS_FOLDER = os.path.join(CLIMBING_FOLDER, "videos")
CLIMBING_INFO = os.path.join(CLIMBING_FOLDER, "videos.yaml")
CLIMBING_JOURNAL = os.path.join(CLIMBING_FOLDER, "journal.yaml")
OUTPUT_PATH = os.path.join("..", "_includes", "diary.md")

videos = {}
if os.path.exists(CLIMBING_INFO):
    with open(CLIMBING_INFO, "r") as f:
        videos = yaml.load(f.read(), Loader=UniqueKeyLoader)

journal = {}
if os.path.exists(CLIMBING_JOURNAL):
    with open(CLIMBING_JOURNAL, "r") as f:
        journal = yaml.load(f.read(), Loader=UniqueKeyLoader)

result = """
<div class="climbing-journal">
"""

current_year = None
current_month = None

month_mapping = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]

for entry in reversed(sorted(list(journal))):
    line = ""

    if current_year != entry.year:
        if current_year is None:
            line += f"<details open class='climbing-year-details'><summary><h3>{entry.year}</h3></summary> <ul>"
        else:
            line += f"</ul></details> <details open class='climbing-year-details'><summary><h3>{entry.year}</h3></summary> <ul>"

        current_year = entry.year

    if current_month != entry.month:
        line += f"</ul><h4>{month_mapping[entry.month - 1]}</h4><ul>"

        current_month = entry.month

    line += f"\n<li><ul class='hfill'><li><strong>{entry.strftime('%-d. %-m. %Y')}</strong>"

    v_colors = [f"V{i}" for i in range(2, 11)]
    v_grading_gyms = set(["třináctka"])

    # keep sorted by difficulty! (left easiest, right hardest)
    wall_colors = {
        "smichoff": ["red", "salmon", "blue", "yellow"],
        "jungle": ["green", "blue", "red"],
        "boulderhaus": ["green", "blue", "red", "black"],
        "boulder-bar": ["green", "blue", "red"],
        "trinactka": v_colors,
    }

    wall = ""
    wall_stub = ""

    if "wall" in journal[entry]:
        wall = journal[entry]["wall"]
        wall_stub = unidecode(wall).lower().replace(" ", "-")

    # locations have no colors since they are not walls; they get treated differently
    if "location" in journal[entry]:
        location = journal[entry]["location"]

        line += f" ({location})"

        if "guide" in journal[entry]:
            line += f" [<a href='/climbing/guides/{journal[entry]['guide']}'>guide</a>]"

        line += f"</li> <li>"

    else:
        if wall == "":
            wall = "Smíchoff"
            wall_stub = "smichoff"

        colors = (
            {}
            if wall_stub not in wall_colors
            else wall_colors[wall_stub]
        )

        line += f" (at <img class='climbing-wall-logo' src='/climbing/wall-logos/{wall_stub}.svg' alt='Logo of the {wall} climbing wall.'/>"

        if "rebuilt" in journal[entry]:
            line += f", <strong>new boulders</strong>"

        line += ")</li> <li>"

    def format_color(color, kilter=False):
        line = ""

        entry_videos = []
        for video in videos:
            if videos[video]["date"] == entry and videos[video]["color"] == color:
                entry_videos.append(video)

        # for adding fail videos
        if kilter:
            color_dict = journal[entry]["kilter"][color]
        else:
            color_dict = {} if color not in journal[entry] else journal[entry][color]

        old_count = 0 if "old" not in color_dict else color_dict["old"]
        new_count = 0 if "new" not in color_dict else color_dict["new"]

        if old_count == 0 and new_count == 0:
            # if there are no videos and no sends for the color, don't add it
            if len(entry_videos) == 0:
                return ""

            count = ""
        elif old_count == 0:
            count = f"<span class='underline'>{new_count}</span>"
        elif new_count == 0:
            count = f"{old_count}"
        else:
            count = f"{old_count}/<span class='underline'>{new_count}</span>"

        if count != "":
            count = "<strong>" + count + "</strong>"

        if color == "other":
            line += f"<mark class='climbing-diary-record climbing-other climbing-other-text'>other: {count}"
        elif (wall_stub in v_grading_gyms) or kilter:
            line += f"<mark class='climbing-diary-record climbing-{color}'><strong>{color}:</strong> {count}"
        else:
            line += f"<mark class='climbing-diary-record climbing-{color} climbing-{color}-text'>{count}"

        if len(entry_videos) != 0:
            line += (
                " ["
                + ", ".join(
                    [
                        f"<a class='climbing-link' href='/climbing/videos/{name}'>{videos[name]['label'] if 'label' in videos[name] else 'F' if 'flash' in videos[name] and videos[name]['flash'] else 'A'}</a>"
                        for i, name in enumerate(entry_videos)
                    ]
                )
                + "]"
            )

        return line + "</mark> "

    some_color_added = False
    for color in list(colors) + ["other"]:
        formatted_color = format_color(color)

        line += formatted_color

        if formatted_color.strip() != "":
            some_color_added = True

    if "kilter" in journal[entry]:
        if some_color_added:
            line += "/ "

        line += "<strong>Kilter: </strong>"
        for color in journal[entry]["kilter"]:
            line += format_color(color, kilter=True)


    line += "</li></ul>"

    if "routes" in journal[entry]:
        line += f"<ul class='climbing-routes-list'>"
        for name, (difficulty, status) in journal[entry]["routes"]:
            line += f"<li><mark class='climbing-diary-record climbing-other climbing-other-text'>{name} ({difficulty}, {status})</mark></li>"
        line += f"</ul>"

    if "note" in journal[entry]:
        # the replace is a bit of a hack.
        # I should probably do proper conversion, but I don't really use anything special
        line += "<p class='climbing-note'>" + journal[entry]["note"].replace("--", "–").replace(":)", "<span class='emoji'>🙂</span>").replace(":(", "<span class='emoji'>☹️</span>") + "</p>"

    line += "</li>"

    result += line + "\n"

result += "</ul>"

with open(OUTPUT_PATH, "w") as f:
    f.write(result)

with open(CLIMBING_JOURNAL, "w") as f:
    f.write(yaml.dump(journal))

print("journal generated (and reformatted).", flush=True)
