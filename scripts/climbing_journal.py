#!/usr/bin/env python3

import os
import re
from collections import OrderedDict

import markdown
import yaml
from unidecode import unidecode


class UniqueKeyLoader(yaml.SafeLoader):
    def construct_mapping(self, node, deep=False):
        mapping = []
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            assert key not in mapping, (
                f"Duplicate key {key} in journal.yaml/videos.yaml."
            )
            mapping.append(key)
        return super().construct_mapping(node, deep)


os.chdir(os.path.dirname(os.path.realpath(__file__)))

# Hugo paths
CLIMBING_INFO = "../data/climbing/videos.yaml"
CLIMBING_JOURNAL = "../data/climbing/journal.yaml"
CLIMBING_STATIC = "../static/climbing"

OUTPUT_PATH = "../content/climbing/diary.txt"
LAST_CLIMB_PATH = "../content/climbing/last-climb.txt"
CLIMBING_VIDEOS_PATH = "../content/climbing/videos/climbing-videos.html"

videos = {}
if os.path.exists(CLIMBING_INFO):
    with open(CLIMBING_INFO, "r") as f:
        videos = yaml.load(f.read(), Loader=UniqueKeyLoader)

journal = {}
if os.path.exists(CLIMBING_JOURNAL):
    with open(CLIMBING_JOURNAL, "r") as f:
        journal = yaml.load(f.read(), Loader=UniqueKeyLoader)

KILTER_NAME = "Kilter Board"
MOONBOARD_NAME = "MoonBoard"

result = """
<div class="climbing-journal">
"""

videos_result = {KILTER_NAME: OrderedDict(), MOONBOARD_NAME: OrderedDict()}

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
            line += f"</ul></details> <details class='climbing-year-details'><summary><h3>{entry.year}</h3></summary> <ul>"

        current_year = entry.year

    if current_month != entry.month:
        send_of_the_month = None

        for video in videos:
            if (
                videos[video]["date"].month == entry.month
                and videos[video]["date"].year == entry.year
            ):
                if "sotm" in videos[video] and videos[video]["sotm"]:
                    send_of_the_month = video

        if send_of_the_month is not None:
            line += f"</ul><h4>{month_mapping[entry.month - 1]} (<a href='/climbing/videos/{send_of_the_month}'>best send</a>)</h4><ul>"
        else:
            line += f"</ul><h4>{month_mapping[entry.month - 1]}</h4><ul>"

        current_month = entry.month

    if "note" in journal[entry]:
        if isinstance(journal[entry]["note"], list):
            note = "</p><p class='climbing-note'>".join(journal[entry]["note"])
        else:
            note = journal[entry]["note"]

        note = (
            note.replace("--", "–")
            .replace(":)", "<span class='emoji'>🙂</span>")
            .replace(":P", "<span class='emoji'>😛</span>")
            .replace(":D", "<span class='emoji'>😀</span>")
            .replace(":|", "<span class='emoji'>😐</span>")
            .replace(":/", "<span class='emoji'>🫤</span>")
            .replace("<3", "<span class='emoji'>❤️</span>")
            .replace(":(", "<span class='emoji'>☹️</span>")
        )

    if "placeholder" in journal[entry] and journal[entry]["placeholder"]:
        result += (
            line + f"<div class='half-visible'><p>⋮<br>{note}<br>⋮</p></div>" + "\n"
        )
        continue

    if "image" in journal[entry]:
        line += f"<div class='climbing-bg-div' style='background-image: url(/climbing/images/{journal[entry]['image']})'>"

    line += f"\n<li id='{str(entry)}'><ul class='climbing-entry-header'><li><strong>{entry.strftime('%-d. %-m. %Y')}</strong>"

    v_colors = [f"V{i}" for i in range(2, 11)]
    v_grading_gyms_stubs = {"trinactka"}

    f_colors = sorted(
        [f"{i}{c}{p}".strip() for i in range(6, 9) for c in "abc" for p in " +"]
    )
    f_grading_gyms_stubs = {"boulder-point"}

    number_colors = sorted([str(i) for i in range(1, 10)])
    number_grading_gyms_stubs = {"boulderwelt-karlsruhe", "climbhouse-brasov"}

    # keep sorted by difficulty! (left easiest, right hardest)
    wall_stubs_colors = {
        "smichoff": ["red", "salmon", "blue", "yellow"],
        "jungle": ["green", "blue", "red"],
        "boulderhaus": ["christmas", "blue", "red", "black", "purple"],
        "crimp": ["blue", "red", "black", "purple"],
        "boulderhaus-darmstadt": ["christmas", "blue", "red", "black"],
        "boulder-bar": ["green", "blue", "red"],
        "trinactka": v_colors,
        "boulder-point": f_colors,
        "climbhouse-brasov": number_colors,
        "boulderwelt-karlsruhe": number_colors,
        "steil-karlsruhe": number_colors,
    }

    wall_urls = {
        "beest": "https://beestboulders.com/",
        "bigwall": "https://www.big-wall.cz/",
        "boulder-bar": "https://www.boulder.cz/",
        "boulderhaus": "https://www.boulderhaus.net/boulderhaus-heidelberg/",
        "boulderhaus-darmstadt": "https://www.boulderhaus.net/boulderhaus-darmstadt/",
        "boulder-point": "http://www.boulderpoint.cz/",
        "boulderwelt-karlsruhe": "https://www.boulderwelt-karlsruhe.de/",
        "climbhouse-brasov": "https://climbhouse.ro/",
        "crimp": "https://www.crimp-heidelberg.com/",
        "jungle-letnany": "https://www.jungleletnany.cz/",
        "lokalblok": "http://www.lokalblok.cz/lezecka-stena/",
        "mandala": "https://boulderhalle-dresden.de/",
        "smichoff": "https://www.lezeckecentrum.cz/cs/",
        "steil-karlsruhe": "https://boulderhalle-steil.com/en/",
        "studiobloc": "http://studiobloc.de/",
        "trinactka": "http://stenastodulky.cz/",
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
                line += (
                    f" [<a href='/climbing/guides/{journal[entry]['guide']}'>guide</a>]"
                )

        line += "</li> <li>"

        colors = []
    else:
        if wall == "":
            wall = "Smíchoff"
            wall_stub = "smichoff"

        colors = (
            {} if wall_stub not in wall_stubs_colors else wall_stubs_colors[wall_stub]
        )

        if not os.path.exists(f"{CLIMBING_STATIC}/wall-logos/{wall_stub}.svg"):
            a = f"<strong>{wall}</strong>"
        else:
            a = f"<img class='climbing-wall-logo' src='/climbing/wall-logos/{wall_stub}.svg' alt='Logo of the {wall} climbing wall.'/>"

        if wall_stub in wall_urls:
            a = f"<a href='{wall_urls[wall_stub]}'>{a}</a>"

        line += f" (at {a}"

        if "rebuilt" in journal[entry]:
            line += ", <strong>new boulders</strong>"

        line += ")</li> <li>"

    if wall not in videos_result:
        videos_result[wall] = OrderedDict()

    def _format_color(color, oc, nc, vs, kilter, moon):
        if oc == 0 and nc == 0:
            # if there are no videos and no sends for the color, don't add it
            if len(vs) == 0:
                return ""

            count = ""

        elif oc == 0:
            count = f"<span class='underline'>{nc}</span>"
        elif nc == 0:
            count = f"{oc}"
        else:
            count = f"{oc}/<span class='underline'>{nc}</span>"

        if count != "":
            count = "<strong>" + count + "</strong>"

        line = ""

        if color == "other":
            line += f"<mark class='climbing-diary-record climbing-other climbing-other-text'>other: {count}"
        elif color is None:
            line += f"<mark class='climbing-diary-record climbing-other climbing-other-text'>{count}"
        elif color == "christmas":
            line += f"<mark class='climbing-diary-record climbing-christmas climbing-christmas-text'>🎄 {count}"
        elif wall_stub in v_grading_gyms_stubs:
            line += f"<mark class='climbing-diary-record climbing-{color} climbing-v'><strong>{color}:</strong> {count}"
        elif wall_stub in f_grading_gyms_stubs:
            line += f"<mark class='climbing-diary-record climbing-{color.replace('+', 'p')} climbing-f'><strong>{color}:</strong> {count}"
        elif wall_stub in number_grading_gyms_stubs:
            line += f"<mark class='climbing-diary-record climbing-{color} climbing-number'><strong>{color}:</strong> {count}"
        elif kilter or moon:
            line += f"<mark class='climbing-diary-record climbing-{color.replace('+', 'p')} climbing-f'><strong>{color}:</strong> {count}"
        else:
            line += f"<mark class='climbing-diary-record climbing-{color} climbing-{color}-text'>{count}"

        if len(vs) != 0:
            line += (
                " ["
                + "".join(
                    [
                        f"<a class='climbing-link' href='/climbing/videos/{name}'>{'F' if 'attempts' in videos[name] and videos[name]['attempts'] == 1 else 'A'}</a>"
                        for i, name in enumerate(vs)
                    ]
                )
                + "]"
            )

        return line + "</mark> "

    def format_color(color, kilter=False, moon=False):
        entry_videos = []
        for video in videos:
            if "ignored" in videos[video] and videos[video]["ignored"]:
                continue

            # Check if video type matches the context (kilter/moon/regular)
            video_type = videos[video].get("type", "indoor")
            type_matches = False

            if kilter and video_type == "kilter":
                type_matches = True
            elif moon and video_type == "moon":
                type_matches = True
            elif not kilter and not moon and video_type in ["indoor", "outdoor"]:
                type_matches = True

            # Check if date and color match
            if (
                type_matches
                and videos[video]["date"] == entry
                and (
                    ("color" in videos[video] and videos[video]["color"]) == color
                    or (color is None and "color" not in videos[video])
                )
            ):
                entry_videos.append(video)

        # for adding fail videos
        if kilter:
            color_dict = journal[entry]["kilter"][color]
        elif moon:
            color_dict = journal[entry]["moon"][color]
        else:
            color_dict = {} if color not in journal[entry] else journal[entry][color]

        old_count = 0 if "old" not in color_dict else color_dict["old"]
        new_count = 0 if "new" not in color_dict else color_dict["new"]

        w = KILTER_NAME if kilter else MOONBOARD_NAME if moon else wall
        if color not in videos_result[w]:
            videos_result[w][color] = [0, 0, []]

        videos_result[w][color][0] += int(old_count)
        videos_result[w][color][1] += int(new_count)
        videos_result[w][color][2] += entry_videos

        return _format_color(
            color, old_count, new_count, entry_videos, kilter=kilter, moon=moon
        )

    some_color_added = False
    if "location" not in journal[entry]:
        for color in list(colors) + ["other"] + [None]:
            formatted_color = format_color(color)

            line += formatted_color

            if formatted_color.strip() != "":
                some_color_added = True

    if "kilter" in journal[entry]:
        if some_color_added:
            line += "/ "

        angle = journal[entry]["kilter"]["angle"]
        line += f"<strong>Kilter Board ({angle}°): </strong>"
        for color in journal[entry]["kilter"]:
            if color == "angle":
                continue

            line += format_color(color, kilter=True)

    if "moon" in journal[entry]:
        if some_color_added:
            line += "/ "

        line += f"<strong>MoonBoard ({journal[entry]['moon']['setup']}): </strong>"

        for color in journal[entry]["moon"]:
            if color == "setup":
                continue

            line += format_color(color, moon=True)

    if line.endswith("<li>"):
        line = line[: -len("<li>")] + "</ul>"
    else:
        line += "</li></ul>"

    if "routes" in journal[entry]:
        line += "<ul class='climbing-routes-list'>"
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

        line += "</ul>"

    if "hangboard" in journal[entry]:
        reps, hang_time, break_time, long_break_time = list(
            map(int, journal[entry]["hangboard"]["parameters"].split("/"))
        )

        exercises = journal[entry]["hangboard"]["exercises"]
        board = journal[entry]["hangboard"]["type"]

        line += (
            f"<p class='climbing-training'><strong>Hangboard:</strong> <strong>{len(exercises)}x{reps}</strong> reps of hang <strong>{hang_time}s</strong> / break <strong>{break_time}s</strong> with <strong>{long_break_time}s</strong> in between"
            "</p>"
            "<ul>"
            f"<li><a href='/climbing/boards/{board}.svg'><strong>exercises:</strong></a> {'  |  '.join(['<em>' + e + '</em>' for e in exercises])}</li>"
            "</ul>"
        )

    if "training" in journal[entry]:
        line += f"<p class='climbing-training'><strong>Training:</strong> {journal[entry]['training']}</p>"

    if "note" in journal[entry]:
        line += "<p class='climbing-note'>" + markdown.markdown(note)[3:]

    line += "</li>"

    if "image" in journal[entry]:
        line += "</div>"

    result += line + "\n"

result += "</ul></details>"

# Handle orphaned videos (videos without corresponding journal entries)
orphaned_videos = {}
for video in videos:
    if "ignored" in videos[video] and videos[video]["ignored"]:
        continue

    if videos[video]["date"] not in journal:
        # Determine the wall/board name based on type
        video_type = videos[video].get("type", "indoor")
        if video_type == "kilter":
            video_wall = KILTER_NAME
        elif video_type == "moon":
            video_wall = MOONBOARD_NAME
        else:
            video_wall = videos[video].get("wall", "Smíchoff")

        if video_wall not in orphaned_videos:
            orphaned_videos[video_wall] = {}

        video_color = videos[video].get("color", None)
        if video_color not in orphaned_videos[video_wall]:
            orphaned_videos[video_wall][video_color] = []

        orphaned_videos[video_wall][video_color].append(video)

# Add orphaned videos section if there are any
if orphaned_videos:
    result += "<h3>Unlinked Videos</h3>"
    result += "<p>These are videos that were added to this website before the journal was created (before 2020), so they can't be linked to any particular journal entry. They are all from Smíchoff, since that's where I was climbing at the time.</p>"

    for wall_name in sorted(orphaned_videos.keys()):
        colors = orphaned_videos[wall_name]
        wall_stub = unidecode(wall_name).lower().replace(" ", "-")

        # Determine if this is a board (kilter/moon)
        is_kilter = wall_name == KILTER_NAME
        is_moon = wall_name == MOONBOARD_NAME

        # Get colors for this wall
        if is_kilter or is_moon:
            # For boards, iterate through the grades that exist in sorted order
            wall_colors = sorted(colors.keys())
        else:
            wall_colors = (
                {}
                if wall_stub not in wall_stubs_colors
                else wall_stubs_colors[wall_stub]
            )

        # Format each color's videos
        colors_to_iterate = (
            wall_colors
            if (is_kilter or is_moon)
            else list(wall_colors) + ["other"] + [None]
        )
        for color in colors_to_iterate:
            if color not in colors:
                continue

            vs = colors[color]
            if len(vs) == 0:
                continue

            # Format the color with video links
            result += _format_color(
                color, 0, len(vs), vs, kilter=is_kilter, moon=is_moon
            )

    result += "<p></p>"  # it was 2 AM and I wanted a spacer

result += "</div>"

with open(OUTPUT_PATH, "w") as f:
    f.write(result)

with open(LAST_CLIMB_PATH, "w") as f:
    # iterating cause some entries might be at home
    for entry in reversed(sorted(list(journal))):
        if "wall" in journal[entry]:
            where = journal[entry]["wall"]

            if where == "home":
                continue

        elif "location" in journal[entry]:
            where = journal[entry]["location"]

        elif "placeholder" in journal[entry]:
            continue

        # strip tags (links) from locations
        where = re.sub("<[^<]+?>", "", where)

        f.write(
            f"Last climbing session: **{entry.strftime('%-d. %-m. %Y')}** at <a href='#{str(entry)}'>{where} ↩</a>."
        )
        break

with open(CLIMBING_VIDEOS_PATH, "w") as f:
    f.write("<div class='climbing-journal-vids-only'>")

    for key in sorted(videos_result):
        # skip no videos
        if not any([len(videos_result[key][c][2]) for c in videos_result[key]]):
            continue

        f.write(f"<h3>{key}</h3><ul>")

        colors = videos_result[key]

        if key == KILTER_NAME or key == MOONBOARD_NAME:
            colors = sorted(colors)

        for color in colors:
            oc, nc, vs = videos_result[key][color]

            if len(vs) == 0:
                continue

            line = _format_color(
                color,
                len(vs),
                0,
                vs,
                kilter=False if key != KILTER_NAME else True,
                moon=False if key != MOONBOARD_NAME else True,
            )

            f.write(f"<li>{line}</li>")

        f.write("</ul>")

    f.write("</div>")

print("journal generated (and reformatted).", flush=True)
