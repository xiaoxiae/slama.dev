#!/usr/bin/env python3

import os
import shutil
from subprocess import Popen, PIPE
from datetime import date

import yaml






os.chdir(os.path.dirname(os.path.realpath(__file__)))

CLIMBING_FOLDER = "../climbing/"
CLIMBING_VIDEOS_FOLDER = os.path.join(CLIMBING_FOLDER, "videos")
CLIMBING_INFO = os.path.join(CLIMBING_FOLDER, "information.yaml")

config = {}
if os.path.exists(CLIMBING_INFO):
    with open(CLIMBING_INFO, "r") as f:
        config = yaml.safe_load(f.read())

files = os.listdir(CLIMBING_VIDEOS_FOLDER)
for file in files:
    if file.lower().endswith(".mp4") and file not in config:
        print(f"adding new file {file}.")
        config[file] = {
            "color": "TODO",
            "date": date.today(),
            "zone": "TODO",
            "new": None,
            "rotate": "left",
            "encode": None,
            "trim": "TODO",
        }

with open(CLIMBING_INFO, "w") as f:
    f.write(yaml.dump(config))
