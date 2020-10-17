#!/usr/bin/env python3

import argparse
import os
import hashlib
from typing import *
from subprocess import Popen, PIPE

import yaml

os.chdir(os.path.dirname(os.path.realpath(__file__)))

MAX = 10  # out of 100
CACHE_FOLDER = ".compress_images_cache"
SUB = "Images"

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
    print([f for f in result if f != b""][0].decode().strip())


def format_to_mb(size: int) -> str:
    """Format to megabytes."""
    return round(size / (1024 ** 2), 2)


config = {}
new_config = {}
if os.path.exists(CACHE_FOLDER):
    with open(CACHE_FOLDER, "r") as f:
        config = yaml.safe_load(f.read())


for root, dirs, files in os.walk("../photography/"):
    for name in files:
        # use jpegoptim to optimize raw images
        if name.endswith(("jpg", "jpeg")) and "raw" in root:
            path = os.path.join(root, name)
            reduced_path = os.path.join(root, "..")
            reduced_name = os.path.join(reduced_path, name)

            # first command is to create a low-res version of the default image
            # second command is to strip the metadata from the pictures
            commands = [
                ["jpegoptim", "-s", path],
                ["jpegoptim", "-s", f"-m{MAX}", path, "-d", reduced_path, "-o"],
            ]

            # strip metadata
            force_low_res = False  # to possibly force-create a new low-res version
            if path not in config or config[path][1] != get_file_hashsum(path):
                execute_shell_command(commands[0])
                new_config[path] = [100, get_file_hashsum(path)]
                force_low_res = True
                something_changed = True
            else:
                new_config[path] = config[path]

            # create low-res image
            if (
                not os.path.exists(reduced_name)
                or reduced_name not in config
                or config[reduced_name] != [MAX, get_file_hashsum(reduced_name)]
                or force_low_res
            ):
                execute_shell_command(commands[1])
                new_config[reduced_name] = [MAX, get_file_hashsum(reduced_name)]
                something_changed = True
            else:
                new_config[reduced_name] = config[reduced_name]

            full_size += os.path.getsize(path)
            reduced_size += os.path.getsize(reduced_name)

with open(CACHE_FOLDER, "w") as f:
    f.write(yaml.dump(new_config))

if something_changed:
    print(f"size before: {format_to_mb(full_size)} MB")
    print(f"size after: {format_to_mb(reduced_size)} MB")
else:
    print("no changes.")
