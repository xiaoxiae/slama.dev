#!/usr/bin/env python3

import os
import hashlib
from PIL import Image
from typing import *
from subprocess import Popen, PIPE

import yaml

os.chdir(os.path.dirname(os.path.realpath(__file__)))

CACHE_FOLDER = "../.jekyll-cache/compress_images"

full_size = 0  # total size of images before compression
reduced_size = 0  # total size of images before compression
something_changed = False


def get_file_hashsum(file_name: str):
    """Generate a SHA-256 hashsum of the given file."""
    hash_sha256 = hashlib.sha256()

    with open(file_name, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha256.update(chunk)

    return hash_sha256.hexdigest()


def execute_shell_command(command: List[str]):
    result = Popen(command, stdout=PIPE, stderr=PIPE).communicate()


def format_to_mb(size: int) -> str:
    """Format to megabytes."""
    return round(size / (1024 ** 2), 2)


config = {}
new_config = {}
if os.path.exists(CACHE_FOLDER):
    with open(CACHE_FOLDER, "r") as f:
        config = yaml.safe_load(f.read())


for root, dirs, files in os.walk("../photos/"):
    for name in files:
        # use cwebp to convert raw images to webp
        if name.endswith(("jpg", "jpeg")) and "raw" in root:
            path = os.path.join(root, name)

            reduced_path = os.path.join(root, "..")
            reduced_name = os.path.join(
                reduced_path, os.path.splitext(name)[0] + ".webp"
            )

            if path not in config or config[path] != get_file_hashsum(path):
                print(f"converting '{path}'... ", flush=True, end="")

                im = Image.open(path)
                width, height = im.size
                new_width = 1000
                new_height = int(height * (new_width / width))

                execute_shell_command(
                    [
                        "cwebp",
                        "-q",
                        "50",
                        "-resize",
                        str(new_width),
                        str(new_height),
                        path,
                        "-o",
                        reduced_name,
                    ]
                )
                print("done.", flush=True)

                new_config[path] = get_file_hashsum(path)

                something_changed = True
            else:
                new_config[path] = config[path]

            full_size += os.path.getsize(path)
            reduced_size += os.path.getsize(reduced_name)

with open(CACHE_FOLDER, "w") as f:
    f.write(yaml.dump(new_config))

if something_changed:
    print(f"size before: {format_to_mb(full_size)} MB", flush=True)
    print(f"size after: {format_to_mb(reduced_size)} MB", flush=True)
else:
    print("no changes.", flush=True)
