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

zones = [1, 2, 3, 4, 5, 6, 7, 8, 9]
colors = ["red", "salmon", "blue", "yellow"]

print(config)

# rename new files
for name in list(config):
    if "new" in config[name]:
        print(config[name])

        random_string = get_random_string(8)
        new_name = "smichoff-" + config[name]["color"] + "-" + config[name]["date"].strftime("%Y-%m-%d") + "-" + random_string + ".mp4"
        del config[name]["new"]
        config[new_name] = config[name]
        del config[name]

        os.rename(os.path.join(CLIMBING_FOLDER, name), os.path.join(CLIMBING_FOLDER, new_name))

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
---
"""

    added = False

    for color in colors:
        videos_in_color = []

        for name in config:
            if config[name]["color"] == color and config[name]["zone"] == zone:
                videos_in_color.append(name)

        videos_in_color = list(reversed(sorted(videos_in_color)))
        print(videos_in_color)

        if len(videos_in_color) != 0:
            zone_file_content += "#### " + color.capitalize()

        for i, name in enumerate(videos_in_color):
            style = f"width:{'48' if (i != len(videos_in_color) - 1 or len(videos_in_color) % 2 == 0) else '100'}%;float:{'left' if i % 2 == 0 else 'right'};"

            zone_file_content += f"""
<figure class='video' style='{style}'>
<video controls><source src='/climbing/{name}' type='video/mp4'></video>
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
