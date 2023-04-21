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
            # NOTE: this probably shouldn't happen, but if it does let's not crash ok?
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
                "select=eq(n\,0)",
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


# Kilter routes by difficulty
kilter_folder = os.path.join(CLIMBING_FOLDER, "kilter")
if os.path.exists(kilter_folder):
    shutil.rmtree(kilter_folder)
os.mkdir(kilter_folder)

kilter_stats_path = os.path.join("..", "_includes", "kilter.md")

kilter_stats = {}


for grade in sorted([f"{i}{c}{p}".strip() for i in range(6, 9) for c in "abc" for p in " +"]):
    grade_file_name = os.path.join(kilter_folder, grade.lower().replace("+", "p") + ".md")

    grade_file_content = f"""---
title: Kilter {grade}
layout: default
css: climbing
no-heading: True
---
"""
    total = 0

    videos_in_color = []
    for name in config:
        if (
            "kilter" in config[name]
            and config[name]["kilter"]
            and config[name]["color"] == grade
        ):
            videos_in_color.append(name)
    videos_in_color = list(reversed(sorted(videos_in_color)))

    for i, name in enumerate(videos_in_color):
        style_class = "climbing-"

        if i % 2 == 0:
            style_class += "left"
        else:
            style_class += "right"

        if len(videos_in_color) % 2 == 1 and i == len(videos_in_color) - 1:
            style_class = "climbing-center"

        grade_file_content += f"""
<figure class='climbing-video {style_class}'>
<video poster="/climbing/videos/{os.path.splitext(name)[0] + '.webp'}" controls preload="none"><source src='/climbing/videos/{name}' type='video/mp4'></video>
<figcaption class='figcaption-margin'>{config[name]["date"].strftime("%d / %m / %Y")}</figcaption>
</figure>"""
        total += 1

    # THIS IS SUPER IMPORTANT!
    # I don't know how to make it so that floats don't intersect the footer,
    # but putting anything below fixes it
    if len(videos_in_color) != 0:
        grade_file_content += f"<p>Total sends: {total}</p>"

    if total != 0:
        with open(grade_file_name, "w") as f:
            f.write(grade_file_content)

        kilter_stats[grade] = total

with open(CLIMBING_INFO, "w") as f:
    f.write(yaml.dump(config))

with open(kilter_stats_path, "w") as f:
    f.write("| " + "|".join([f"[{k}](/climbing/kilter/{k.lower().replace('+', 'p')}/) ({v})" for k, v in kilter_stats.items()]) + "|\n")

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
