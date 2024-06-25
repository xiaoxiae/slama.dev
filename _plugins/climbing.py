#!/usr/bin/env python3

import os
import shutil
from PIL import Image
from random import choice
from string import ascii_lowercase
from subprocess import Popen, PIPE
from unidecode import unidecode

import yaml


def stubify(string: str) -> str:
    return unidecode(string).lower().replace(" ", "-")

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

for name in list(config):
    for attribute in config[name]:
        if config[name][attribute] == "TODO":
            print("ERROR: the videos.yaml file contains TODOs, not generating.")
            quit()

    if not os.path.exists(os.path.join(CLIMBING_VIDEOS_FOLDER, name)):
        print(f"ERROR: nonexistent video '{name}', not generating.")
        quit()

# rename new files
for name in list(config):
    path = os.path.join(CLIMBING_VIDEOS_FOLDER, name)

    if "new" in config[name]:
        print(f"parsing new climb '{name}'.", flush=True)

        if "wall" in config[name]:
            location_stub = stubify(config[name]["wall"]) 
        elif "kilter" in config[name] and config[name]["kilter"]:
            location_stub = "kilter"
        elif "moon" in config[name] and config[name]["moon"]:
            location_stub = "moon"
        elif "location" in config[name]:
            location_stub = stubify(config[name]["location"])
        else:
            location_stub = "smichoff"

        # assign a new (random) name
        random_string = get_random_string(8)

        if "color" in config[name]:
            identifier_stub = config[name]["color"].replace("+", "p") + "-"
        elif "name" in config[name]:
            identifier_stub = stubify(config[name]["name"]) + "-"
        else:
            # NOTE: this can happen when a wall doesn't have colors
            #  and we want to support it
            identifier_stub = ""

        new_name = (
            f"{location_stub}-"
            + identifier_stub
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

        new_path = os.path.join(CLIMBING_VIDEOS_FOLDER, name)
        os.rename(path, new_path)

        path = new_path

    tmp_path = os.path.join(CLIMBING_VIDEOS_FOLDER, "tmp_" + name)

    # trim the video
    if "trim" in config[name]:

        start, end = config[name]["trim"].split(",")
        command = [
            "ffmpeg",
            "-y",
            "-i",
            path,
            "-ss",
            start,
            "-to",
            end,
            tmp_path,
        ]

        _ = Popen(command, stdout=PIPE, stderr=PIPE).communicate()
        os.remove(path)
        os.rename(tmp_path, path)
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
            ["ffmpeg", "-y", "-i", path]
            + encode_config
            + rotate_config
            + [tmp_path]
        )

        _ = Popen(command, stdout=PIPE, stderr=PIPE).communicate()
        os.remove(path)
        os.rename(tmp_path, path)

        if "encode" in config[name]:
            del config[name]["encode"]
        if "rotate" in config[name]:
            del config[name]["rotate"]

    if "deface" in config[name]:
        command = [
            "deface",
            path,
            "-t",
            "0.5",
            "-o",
            tmp_path,
        ]

        _ = Popen(command, stdout=PIPE, stderr=PIPE).communicate()

        old_folder = os.path.join(CLIMBING_VIDEOS_FOLDER, "unblurred")

        if not os.path.exists(old_folder):
            os.mkdir(old_folder)

        os.rename(path, os.path.join(old_folder, name))
        os.rename(tmp_path, path)
        del config[name]["deface"]


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
                path,
                "-vf",
                r"select=eq(n\,0)",
                "-vframes",
                "1",
                "-y",
                poster_jpeg,
            ],
            stdout=PIPE,
            stderr=PIPE,
        ).communicate()

        im = Image.open(poster_jpeg)
        width, height = im.size
        new_width = 720
        new_height = int(height * (new_width / width))

        _ = Popen(
            [
                "cwebp",
                "-q",
                "5",
                "-resize",
                str(new_width),
                str(new_height),
                poster_jpeg,
                "-o",
                poster_webp,
            ],
            stdout=PIPE,
            stderr=PIPE,
        ).communicate()

        _ = Popen(["rm", poster_jpeg], stdout=PIPE, stderr=PIPE).communicate()


with open(CLIMBING_INFO, "w") as f:
    f.write(yaml.dump(config))

print("climbing videos generated (and reformatted).", flush=True)

# warn about videos that are not on the list, for good measure
files = os.listdir(CLIMBING_VIDEOS_FOLDER)
for file in files:
    if file.lower().endswith(".mp4") and file not in config:
        print(f"WARNING: leftover file {file}.", flush=True)
    if file.lower().endswith(".jpeg") and file[:-5] not in config:
        print(f"WARNING: leftover poster {file}.", flush=True)

# warn about videos that were not found
for file in config:
    if file not in files:
        print(f"WARNING: file {file} not found.", flush=True)
