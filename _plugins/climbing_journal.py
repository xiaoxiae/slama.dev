#!/usr/bin/env python3

import markdown
import os
import re
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
LAST_CLIMB_PATH = os.path.join("..", "_includes", "last-climb.md")

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
        send_of_the_month = None

        for video in videos:
            if videos[video]["date"].month == entry.month and videos[video]["date"].year == entry.year:
                if "sotm" in videos[video] and videos[video]["sotm"]:
                    send_of_the_month = video

        if send_of_the_month is not None:
            line += f"</ul><h4>{month_mapping[entry.month - 1]} (<a href='/climbing/videos/{send_of_the_month}'>best send</a>)</h4><ul>"
        else:
            line += f"</ul><h4>{month_mapping[entry.month - 1]}</h4><ul>"

        current_month = entry.month

    if "image" in journal[entry]:
        line += f"<div class='climbing-bg-div' style='background-image: url(/climbing/images/{journal[entry]['image']})'>"

    line += f"\n<li id='{str(entry)}'><ul class='hfill'><li><strong>{entry.strftime('%-d. %-m. %Y')}</strong>"

    v_colors = [f"V{i}" for i in range(2, 11)]
    v_grading_gyms_stubs = {"trinactka"}

    f_colors = sorted([f"{i}{c}{p}".strip() for i in range(6, 9) for c in "abc" for p in " +"])
    f_grading_gyms_stubs = {"boulder-point"}

    # keep sorted by difficulty! (left easiest, right hardest)
    wall_stubs_colors = {
        "smichoff": ["red", "salmon", "blue", "yellow"],
        "jungle": ["green", "blue", "red"],
        "boulderhaus": ["christmas", "blue", "red", "black"],
        "boulder-bar": ["green", "blue", "red"],
        "trinactka": v_colors,
        "boulder-point": f_colors,
    }

    wall = ""
    wall_stub = ""

    if "wall" in journal[entry]:
        wall = journal[entry]["wall"]
        wall_stub = unidecode(wall).lower().replace(" ", "-")

    # locations have no colors since they are not walls; they get treated differently
    if "location" in journal[entry]:
        location = journal[entry]["location"]

        line += f" (at {location})"

        if "guide" in journal[entry]:
            g = journal[entry]["guide"]
            # a bit hacky but w/e
            if "http" in g:
                line += f" [<a href='{g}'>guide</a>]"
            else:
                line += f" [<a href='/climbing/guides/{journal[entry]['guide']}'>guide</a>]"

        line += f"</li> <li>"

        colors = []
    else:
        if wall == "":
            wall = "Smíchoff"
            wall_stub = "smichoff"

        colors = (
            {}
            if wall_stub not in wall_stubs_colors
            else wall_stubs_colors[wall_stub]
        )

        if not os.path.exists(f"../climbing/wall-logos/{wall_stub}.svg"):
            line += f" (at <strong>{wall}</strong>"
        else:
            line += f" (at <img class='climbing-wall-logo' src='/climbing/wall-logos/{wall_stub}.svg' alt='Logo of the {wall} climbing wall.'/>"

        if "rebuilt" in journal[entry]:
            line += f", <strong>new boulders</strong>"

        line += ")</li> <li>"

    def format_color(color, kilter=False):
        line = ""

        entry_videos = []
        for video in videos:
            if 'ignored' in videos[video] and videos[video]['ignored']:
                continue

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
        elif color == "christmas":
            line += f"<mark class='climbing-diary-record climbing-christmas climbing-christmas-text'>🎄 {count}"
        elif wall_stub in v_grading_gyms_stubs:
            line += f"<mark class='climbing-diary-record climbing-{color} climbing-v'><strong>{color}:</strong> {count}"
        elif wall_stub in f_grading_gyms_stubs:
            line += f"<mark class='climbing-diary-record climbing-{color.replace('+', 'p')} climbing-f'><strong>{color}:</strong> {count}"
        elif kilter:
            line += f"<mark class='climbing-diary-record climbing-{color.replace('+', 'p')} climbing-f'><strong>{color}:</strong> {count}"
        else:
            line += f"<mark class='climbing-diary-record climbing-{color} climbing-{color}-text'>{count}"

        if len(entry_videos) != 0:
            line += (
                " ["
                + "".join(
                    [
                        f"<a class='climbing-link' href='/climbing/videos/{name}'>{'F' if 'attempts' in videos[name] and videos[name]['attempts'] == 1 else 'A'}</a>"
                        for i, name in enumerate(entry_videos)
                    ]
                )
                + "]"
            )

        return line + "</mark> "

    some_color_added = False
    if "location" not in journal[entry]:
        for color in list(colors) + ["other"]:
            formatted_color = format_color(color)

            line += formatted_color

            if formatted_color.strip() != "":
                some_color_added = True

    if "kilter" in journal[entry]:
        if some_color_added:
            line += "/ "

        angle = journal[entry]["kilter"]["angle"]
        line += f"<strong>Kilter ({angle}°): </strong>"
        for color in journal[entry]["kilter"]:
            if color == "angle":
                continue

            line += format_color(color, kilter=True)

    if line.endswith("<li>"):
        line = line[:-len("<li>")] + "</ul>"
    else:
        line += "</li></ul>"

    if "routes" in journal[entry]:
        line += f"<ul class='climbing-routes-list'>"
        for name, attributes in journal[entry]["routes"]:
            # ugly but I tired
            if len(attributes) == 2:
                difficulty, status = attributes
                line += f"<li><mark class='climbing-diary-record climbing-other climbing-other-text'>{name} ({difficulty}, {status})"
            else:
                difficulty = attributes[0]
                line += f"<li><mark class='climbing-diary-record climbing-other climbing-other-text'>{name} ({difficulty})"

            for video in videos:
                if videos[video]["date"] == entry and videos[video]["name"] == name:
                    line += f" [<a class='climbing-link' href='/climbing/videos/{video}'>video</a>]"

            line += "</mark></li>"

        line += f"</ul>"

    if "hangboard" in journal[entry]:
        reps, hang_time, break_time, long_break_time = list(map(int, journal[entry]["hangboard"]["parameters"].split("/")))

        exercises = journal[entry]["hangboard"]["exercises"]
        board = journal[entry]["hangboard"]["type"]

        line += f"<p class='climbing-hangboard'><strong>Hangboard:</strong> <strong>{len(exercises)}x{reps}</strong> reps of hang <strong>{hang_time}s</strong> / break <strong>{break_time}s</strong> with <strong>{long_break_time}s</strong> in between" \
                 "</p>" \
                 "<ul>" \
                 f"<li><a href='/climbing/boards/{board}.svg'><strong>exercises:</strong></a> {'  |  '.join(['<em>' + e + '</em>' for e in exercises])}</li>" \
                 "</ul>"

    if "note" in journal[entry]:
        note = journal[entry]["note"]\
                .replace("--", "–")\
                .replace(":)", "<span class='emoji'>🙂</span>")\
                .replace(":D", "<span class='emoji'>😀</span>")\
                .replace(":|", "<span class='emoji'>😐</span>")\
                .replace(":/", "<span class='emoji'>🫤</span>")\
                .replace("<3", "<span class='emoji'>❤️</span>")\
                .replace(":(", "<span class='emoji'>☹️</span>")

        line += "<p class='climbing-note'>" + markdown.markdown(note)[3:]

    line += "</li>"

    if "image" in journal[entry]:
        line += "</div>"

    result += line + "\n"

result += "</ul>"

with open(OUTPUT_PATH, "w") as f:
    f.write(result)

with open(LAST_CLIMB_PATH, "w") as f:
    entry = sorted(list(journal))[-1]

    if "wall" in journal[entry]:
        where = journal[entry]["wall"]

        if "kilter" in journal[entry]:
            where += " / Kilter"

    elif "location" in journal[entry]:
        where = journal[entry]["location"]

    # strip tags (links) from locations
    where = re.sub('<[^<]+?>', '', where)

    f.write(f"Last climbing session: **{entry.strftime('%-d. %-m. %Y')}** at <a href='#{str(entry)}'>{where} ↩</a>.")

with open(CLIMBING_JOURNAL, "w") as f:
    f.write(yaml.dump(journal))

print("journal generated (and reformatted).", flush=True)
