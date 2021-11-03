#!/usr/bin/env python3

import os
import shutil
from random import choice
from string import ascii_lowercase, digits
from typing import *
from subprocess import Popen, PIPE

import yaml


def get_random_string(length: int):
    """Generate a random string."""
    result = ""
    for _ in range(length):
        result += choice(ascii_lowercase)
    return result


os.chdir(os.path.dirname(os.path.realpath(__file__)))

CLIMBING_FOLDER = "../climbing/"
CLIMBING_VIDEOS_FOLDER = os.path.join(CLIMBING_FOLDER, "videos")
CLIMBING_INFO = os.path.join(CLIMBING_FOLDER, "videos.yaml")

config = {}
if os.path.exists(CLIMBING_INFO):
    with open(CLIMBING_INFO, "r") as f:
        config = yaml.safe_load(f.read())

zones = [1, 2, 3, 4, 5, 6, 7, 8, 9, "all"]
colors = list(reversed(["red", "salmon", "blue", "yellow"]))

# rename new files
for name in list(config):
    old_path = os.path.join(CLIMBING_VIDEOS_FOLDER, name)

    if "new" in config[name]:
        print(f"parsing new climb '{name}'.", flush=True)

        # assign a new (random) name
        random_string = get_random_string(8)
        new_name = (
            "smichoff-"
            + ("" if "color" not in config[name] else (config[name]["color"] + "-"))
            + (
                ""
                if "date" not in config[name]
                else config[name]["date"].strftime("%Y-%m-%d") + "-"
            )
            + random_string
            + ".mp4"
        )

        # not new anymore
        del config[name]["new"]
        config[new_name] = config[name]
        del config[name]

        name = new_name

        tmp_path = os.path.join(CLIMBING_VIDEOS_FOLDER, "tmp_" + name)

        # trim the video
        if "trim" in config[name]:
            start, end = config[name]["trim"].split(",")
            command = [
                "ffmpeg",
                "-y",
                "-i",
                old_path,
                "-ss",
                start,
                "-to",
                end,
                tmp_path,
            ]

            _ = Popen(command, stdout=PIPE, stderr=PIPE).communicate()
            os.remove(old_path)
            os.rename(tmp_path, old_path)
            del config[name]["trim"]

        # encode/rotate the video
        if "encode" in config[name] or "rotate" in config[name]:
            encode_config = (
                []
                if "encode" not in config[name]
                else ["-vcodec", "libx264", "-crf", "28"]
            )
            rotate_config = (
                []
                if "rotate" not in config[name]
                else [
                    "-vf",
                    f'transpose={"2" if config[name]["rotate"] == "left" else "1"}',
                ]
            )
            command = (
                ["ffmpeg", "-y", "-i", old_path]
                + encode_config
                + rotate_config
                + [tmp_path]
            )

            _ = Popen(command, stdout=PIPE, stderr=PIPE).communicate()
            os.remove(old_path)
            os.rename(tmp_path, old_path)

            if "encode" in config[name]:
                del config[name]["encode"]
            if "rotate" in config[name]:
                del config[name]["rotate"]

        new_path = os.path.join(CLIMBING_VIDEOS_FOLDER, name)
        os.rename(old_path, new_path)

    # generate a poster, if it doesn't exist
    poster_jpeg = os.path.join(
        CLIMBING_VIDEOS_FOLDER, os.path.splitext(name)[0] + ".jpeg"
    )
    poster_webp = os.path.join(
        CLIMBING_VIDEOS_FOLDER, os.path.splitext(name)[0] + ".webp"
    )

    if not os.path.exists(poster_webp):
        print(f"generating a poster for '{name}'.", flush=True)

        _ = Popen(
            [
                "ffmpeg",
                "-i",
                old_path,
                "-vf",
                "select=eq(n\,0)",
                "-vframes",
                "1",
                "-y",
                poster_jpeg,
            ],
            stdout=PIPE,
            stderr=PIPE,
        ).communicate()

        _ = Popen(
            ["cwebp", "-q", "10", poster_jpeg, "-o", poster_webp],
            stdout=PIPE,
            stderr=PIPE,
        ).communicate()

        _ = Popen(["rm", poster_jpeg], stdout=PIPE, stderr=PIPE).communicate()

# sort -- gets sorted by date, due to the name of the climbing files
config_list = [(file, config[file]) for file in config]

# clear old zones
zones_folder = os.path.join(CLIMBING_FOLDER, "zones")
if os.path.exists(zones_folder):
    shutil.rmtree(zones_folder)
os.mkdir(zones_folder)

for zone in zones:
    zone_file_name = os.path.join(CLIMBING_FOLDER, "zones", str(zone) + ".md")
    zone_file_content = f"""---
title: Climbing
layout: default
css: climbing
no-heading: True
---
"""
    added = False
    total = 0

    for color in colors:
        videos_in_color = []

        for name in config:
            if config[name]["color"] == color and (
                config[name]["zone"] == zone or zone == "all"
            ):
                videos_in_color.append(name)

        videos_in_color = list(reversed(sorted(videos_in_color)))

        if len(videos_in_color) != 0:
            zone_file_content += "\n\n{: .center}\n### " + color.capitalize()

        for i, name in enumerate(videos_in_color):
            style_class = "climbing-"

            # either an odd number of videos, or even and not the last -- no center
            if len(videos_in_color) % 2 == 0 or (
                len(videos_in_color) % 2 == 1 and i != len(videos_in_color) - 1
            ):
                style_class += "left" if i % 2 == 0 else "right"
            else:
                style_class += "center"

            zone_file_content += f"""
<figure class='climbing-video climbing-{color} {style_class}'>
<video alt="Me climbing a {color} boulder at Smíchoff, {config[name]["date"].strftime("%d/%m/%Y")}." poster="/climbing/videos/{os.path.splitext(name)[0] + '.webp'}" controls preload="none"><source src='/climbing/videos/{name}' type='video/mp4'></video>
<figcaption class='figcaption-margin'>{config[name]["date"].strftime("%d / %m / %Y")}</figcaption>
</figure>"""

            added = True
            total += 1

        # THIS IS SUPER IMPORTANT!
        # I don't know how to make it so that floats don't intersect the footer,
        # but putting anything below fixes it
        if len(videos_in_color) != 0:
            zone_file_content += f"<p class='right'>Total climbs: {total}</p>"

    # if there are no videos of the climb, add a text about it
    if not added:
        zone_file_content += (
            "{: .center}\nI haven't recorded any climbs in this zone yet, sorry!"
        )

    with open(zone_file_name, "w") as f:
        f.write(zone_file_content)

print("zones generated.", flush=True)

with open(CLIMBING_INFO, "w") as f:
    f.write(yaml.dump(config))

# remove videos that are not on the list, for good measure
files = os.listdir(CLIMBING_VIDEOS_FOLDER)
for file in files:
    if file.lower().endswith(".mp4") and file not in config:
        print(f"WARNING: leftover file {file}.", flush=True)
    if file.lower().endswith(".jpeg") and file[:-5] not in config:
        print(f"WARNING: leftover poster {file}.", flush=True)

for file in config:
    if file not in files:
        print(f"WARNING: file {file} not found.", flush=True)
