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
CLIMBING_INFO = os.path.join(CLIMBING_FOLDER, "information.yaml")

config = {}
if os.path.exists(CLIMBING_INFO):
    with open(CLIMBING_INFO, "r") as f:
        config = yaml.safe_load(f.read())

zones = [1, 2, 3, 4, 5, 6, 7, 8, 9, "all"]
colors = ["red", "salmon", "blue", "yellow"]

# rename new files
for name in list(config):
    if "new" in config[name]:
        print(f"parsing new climb '{name}'.")

        # assign a new name
        random_string = get_random_string(8)
        new_name = "smichoff-" + config[name]["color"] + "-" + config[name]["date"].strftime("%Y-%m-%d") + "-" + random_string + ".mp4"
        del config[name]["new"]
        config[new_name] = config[name]
        del config[name]

        # useful paths
        old_path = os.path.join(CLIMBING_FOLDER, name)
        tmp_path = os.path.join(CLIMBING_FOLDER, "tmp_" + name)
        new_path = os.path.join(CLIMBING_FOLDER, new_name)

        # create the poster
        _ = Popen(["ffmpeg", "-i", old_path, "-vf", "select=eq(n\,0)", "-vframes", "1", "-y", new_path + ".jpeg"], stdout=PIPE, stderr=PIPE).communicate()

        # trim the video
        if "trim" in config[new_name]:
            start, end = config[new_name]["trim"].split(",")
            command = ["ffmpeg", "-y", "-i", old_path, "-ss", start, "-to", end, tmp_path]

            _ = Popen(command, stdout=PIPE, stderr=PIPE).communicate()
            os.remove(old_path)
            os.rename(tmp_path, old_path)
            del config[new_name]["trim"]

        # encode/rotate the video
        if "encode" in config[new_name] or "rotate" in config[new_name]:
            encode_config = [] if "encode" not in config[new_name] else ["-vcodec", "libx264", "-crf", "28"]
            rotate_config = [] if "rotate" not in config[new_name] else ["-vf", f'transpose={"2" if config[new_name]["rotate"] == "left" else "1"}']
            command = ["ffmpeg", "-y", "-i", old_path] + encode_config + rotate_config + [tmp_path]

            _ = Popen(command, stdout=PIPE, stderr=PIPE).communicate()
            os.remove(old_path)
            os.rename(tmp_path, old_path)

            if "encode" in config[new_name]:
                del config[new_name]["encode"]
            if "rotate" in config[new_name]:
                del config[new_name]["rotate"]

        os.rename(old_path, new_path)

# sort -- gets sorted by date, due to the name of the climbing files
config_list = [(file, config[file]) for file in config]

# clear old zones
zones_folder = os.path.join(CLIMBING_FOLDER, "zones")
if os.path.exists(zones_folder):
    shutil.rmtree(zones_folder)
os.mkdir(zones_folder)

print("generating zones.")

for zone in zones:
    zone_file_name = os.path.join(CLIMBING_FOLDER, "zones", str(zone) + ".md")
    zone_file_content = f"""---
title: Climbing
layout: default
---
"""
    added = False

    for color in colors:
        videos_in_color = []

        for name in config:
            if config[name]["color"] == color and (config[name]["zone"] == zone or zone == "all"):
                videos_in_color.append(name)

        videos_in_color = list(reversed(sorted(videos_in_color)))

        if len(videos_in_color) != 0:
            zone_file_content += "\n\n{: .center}\n### " + color.capitalize()

        for i, name in enumerate(videos_in_color):
            style_class = "climbing-"

            # either an odd number of videos, or even and not the last -- no center
            if len(videos_in_color) % 2 == 0 or (len(videos_in_color) % 2 == 1 and i != len(videos_in_color) - 1):
                style_class += 'left' if i % 2 == 0 else 'right'
            else:
                style_class += "center"

            zone_file_content += f"""
<figure class='climbing-video climbing-{color} {style_class}'>
<video poster="/climbing/{name}.jpeg" controls><source src='/climbing/{name}' type='video/mp4'></video>
<figcaption class='figcaption-margin'>{config[name]["date"].strftime("%d / %m / %Y")}</figcaption>
</figure>"""

            added = True

    # if there are no videos of the climb, add a text about it
    if not added:
        zone_file_content += "{: .center}\nI haven't recorded any climbs in this zone yet, sorry!"

    with open(zone_file_name, "w") as f:
        f.write(zone_file_content)

with open(CLIMBING_INFO, "w") as f:
    f.write(yaml.dump(config))

# remove videos that are not on the list, for good measure
for file in os.listdir(CLIMBING_FOLDER):
    if (file.endswith(".mp4") and file not in config) or (file.endswith(".jpeg") and file[:-5] not in config):
        os.remove(os.path.join(CLIMBING_FOLDER, file))
