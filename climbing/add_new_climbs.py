#!/usr/bin/env python3

import os
import shutil
from subprocess import Popen, PIPE
from datetime import date

import yaml


os.chdir(os.path.dirname(os.path.realpath(__file__)))

CLIMBING_FOLDER = "."
CLIMBING_VIDEOS_FOLDER = os.path.join(CLIMBING_FOLDER, "videos")
CLIMBING_INFO = os.path.join(CLIMBING_FOLDER, "videos.yaml")

config = {}
if os.path.exists(CLIMBING_INFO):
    with open(CLIMBING_INFO, "r") as f:
        config = yaml.safe_load(f.read())

files = os.listdir(CLIMBING_VIDEOS_FOLDER)
for file in files:
    if file.lower().endswith(".mp4") and file not in config:
        config[file] = {
            "color": "TODO",
            "date": date.today(),
            "new": None,
            "rotate": "left",
            "encode": None,
            "trim": "TODO",
            "wall": "Boulderhaus",
        }

        kilter = file.lower().startswith("kilter")

        # hacky since the DJI camera is usually turned upside down this way
        if "dji" not in file.lower():
            del config[file]["rotate"]

        # a little hacky but very functional
        if kilter:
            del config[file]["wall"]
            config[file]["kilter"] = True

        print(f"adding new {'' if not kilter else 'Kilter '}file {file}.")

with open(CLIMBING_INFO, "w") as f:
    f.write(yaml.dump(config))
