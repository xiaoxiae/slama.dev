#!/usr/bin/env python3

import os
import shutil
from PIL import Image
from random import choice
from string import ascii_lowercase
from subprocess import Popen, PIPE
from unidecode import unidecode

import yaml
from climbing_types import VideoMetadata


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

HAS_CUDA = shutil.which('nvidia-smi') is not None


config: dict[str, VideoMetadata] = {}
if os.path.exists(CLIMBING_INFO):
    with open(CLIMBING_INFO, "r") as f:
        raw_config = yaml.safe_load(f.read())
        if raw_config:
            # Parse each video entry through Pydantic for validation
            for video_name, video_data in raw_config.items():
                # Skip default names
                if 'name' in video_data and video_data['name'] == video_name:
                    video_data['name'] = None

                config[video_name] = VideoMetadata(**video_data)

for name in list(config):
    video_dict = config[name].model_dump()
    for attribute, value in video_dict.items():
        if value == "TODO":
            print("ERROR: the videos.yaml file contains TODOs, not generating.")
            quit()

    if not os.path.exists(os.path.join(CLIMBING_VIDEOS_FOLDER, name)):
        print(f"ERROR: nonexistent video '{name}', not generating.")
        quit()

# rename new files
for name in list(config):
    path = os.path.join(CLIMBING_VIDEOS_FOLDER, name)
    video = config[name]

    if video.new:
        print(f"parsing new climb '{name}'.", flush=True)

        if video.wall:
            location_stub = stubify(video.wall)
        elif video.type == "kilter":
            location_stub = "kilter"
        elif video.type == "moon":
            location_stub = "moon"
        elif video.location:
            location_stub = stubify(video.location)
        else:
            location_stub = "smichoff"

        # assign a new (random) name
        random_string = get_random_string(8)

        if video.color is not None:
            color_str = str(video.color).replace("+", "p")
            identifier_stub = color_str + "-"
        elif video.name:
            identifier_stub = stubify(video.name) + "-"
        else:
            # NOTE: this can happen when a wall doesn't have colors
            #  and we want to support it
            identifier_stub = ""

        new_name = (
            f"{location_stub}-"
            + identifier_stub
            + (
                ""
                if video.date is None
                else video.date.strftime("%Y-%m-%d") + "-"
            )
            + random_string
            + ".mp4"
        )

        # not new anymore - create a new instance without the 'new' flag
        video.new = None
        config[new_name] = video
        del config[name]

        name = new_name

        new_path = os.path.join(CLIMBING_VIDEOS_FOLDER, name)
        os.rename(path, new_path)

        path = new_path

    tmp_path = os.path.join(CLIMBING_VIDEOS_FOLDER, "tmp_" + name)
    video = config[name]

    # trim the video
    if video.trim:
        start, end = video.trim.split(",")
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

        _ = Popen(command).communicate()
        os.remove(path)
        os.rename(tmp_path, path)
        video.trim = None

    # encode/rotate the video
    if video.encode or video.rotate:
        encode_config = (
            []
            if not video.encode
            else ["-c:v", "h264_nvenc" if HAS_CUDA else "h264", "-preset", "slow"]
        )
        rotate_config = (
            []
            if not video.rotate
            else [
                "-vf",
                f'transpose={"2" if video.rotate == "left" else "1"}',
            ]
        )
        command = (
            ["ffmpeg", "-y", "-i", path]
            + encode_config
            + rotate_config
            + [tmp_path]
        )

        _ = Popen(command).communicate()
        os.remove(path)
        os.rename(tmp_path, path)

        if video.encode:
            video.encode = None
        if video.rotate:
            video.rotate = None

    if video.deface:
        command = [
            "deface",
            path,
            "-t",
            "0.5",
            "-o",
            tmp_path,
        ]

        _ = Popen(command).communicate()

        old_folder = os.path.join(CLIMBING_VIDEOS_FOLDER, "unblurred")

        if not os.path.exists(old_folder):
            os.mkdir(old_folder)

        os.rename(path, os.path.join(old_folder, name))
        os.rename(tmp_path, path)
        video.deface = None


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
        ).communicate()

        _ = Popen(["rm", poster_jpeg]).communicate()


# Convert Pydantic models back to dicts for YAML serialization
# Exclude None values, defaults, and temporary processing fields
config_dict = {
    video_name: video.model_dump(
        exclude_none=True,
        exclude_defaults=True,
        exclude={'new', 'trim', 'encode', 'rotate', 'deface'}
    )
    for video_name, video in config.items()
}

with open(CLIMBING_INFO, "w") as f:
    f.write(yaml.dump(config_dict))

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
