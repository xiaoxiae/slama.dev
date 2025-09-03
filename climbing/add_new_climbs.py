#!/usr/bin/env python3

import os
import shutil
from subprocess import Popen, PIPE
from datetime import date

import sys

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
    if file.lower().endswith((".mp4", ".avi")) and file not in config:
        full_path = os.path.join(CLIMBING_VIDEOS_FOLDER, file)

        if sys.argv[-1].lower() == "crimp":
            config[file] = {
                "date": date.fromtimestamp(os.path.getmtime(full_path)),
                "new": None,
                "encode": None,
                "trim": "TODO",
                "wall": "Crimp",
            }

        else:
            config[file] = {
                "color": "TODO",
                "date": date.fromtimestamp(os.path.getmtime(full_path)),
                "new": None,
                "encode": None,
                "trim": "TODO",
                "deface": None,
                "wall": "Boulderhaus",
            }

        kilter = file.lower().startswith("kilter")
        moon = file.lower().startswith("moon")

        # a little hacky but very functional
        if kilter:
            del config[file]["wall"]

            try:
                del config[file]["deface"]
            except Exception:
                pass

            config[file]["kilter"] = True
            print(f"adding new {'' if not kilter else 'Kilter '}file {file}.")
        # a little hacky but very functional
        elif moon:
            del config[file]["wall"]

            try:
                del config[file]["deface"]
            except Exception:
                pass

            config[file]["moon"] = True
            print(f"adding new {'' if not moon else 'Moon '}file {file}.")
        else:
            print(f"adding new file {file}.")

with open(CLIMBING_INFO, "w") as f:
    f.write(yaml.dump(config))
