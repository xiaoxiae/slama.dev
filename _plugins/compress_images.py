#!/usr/bin/env python3

import os
import re
import sys
import hashlib
from PIL import Image
from typing import *
from subprocess import Popen, PIPE

import yaml

os.chdir(os.path.dirname(os.path.realpath(__file__)))
CACHE_FOLDER = "../.jekyll-cache/compress_images"
PHOTOS_FOLDER = "../photos/"
POSTS_FOLDER = "../_posts/"
LEFTOVER_FOLDER = "../ignored/automatically-removed-photos/"

full_size = 0  # total size of images before compression
thumbnail_size = 0  # total size of images before compression
something_changed = False


full = False
if len(sys.argv) == 2 and sys.argv[1] in ("-f", "--full"):
    full = True


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
    return round(size / (1024**2), 2)

def extract_image_paths_from_markdown(markdown_content):
    """Extracts image paths from Markdown content containing Liquid tags."""

    # Regular expression to find image paths within Liquid tags
    liquid_tag_pattern = r'{%\s*photos\s*(.+)\s*%}'

    # Find all matches of liquid tags in the markdown content
    liquid_tags = re.findall(liquid_tag_pattern, markdown_content)

    # Extract image paths from liquid tags
    image_paths = []
    for tag in liquid_tags:
        paths = tag.split('|')
        for path in paths:
            image_path = path.split('&')[0].strip()
            image_paths.append(os.path.join(PHOTOS_FOLDER, image_path))

    return image_paths

def find_markdown_files(directory):
    """Finds all Markdown files in a directory and its subdirectories."""
    markdown_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".md"):
                markdown_files.append(os.path.join(root, file))
    return markdown_files

def extract_image_paths_from_directory(directories):
    """Extracts image paths from all Markdown files in a directory and its subdirectories."""

    markdown_files = []

    for directory in directories:
        markdown_files += find_markdown_files(directory)

    image_paths_set = set()
    for markdown_file in markdown_files:
        with open(markdown_file, 'r') as file:
            markdown_content = file.read()
        image_paths = extract_image_paths_from_markdown(markdown_content)
        image_paths_set.update(image_paths)

    return image_paths_set


config = {}
new_config = {}
if os.path.exists(CACHE_FOLDER):
    with open(CACHE_FOLDER, "r") as f:
        config = yaml.safe_load(f.read()) or {}


thumbnails = set()
webp_files = set()

for root, dirs, files in os.walk(PHOTOS_FOLDER, followlinks=True):
    for name in files:
        path = os.path.join(root, name)

        if name.endswith("webp"):
            thumbnails.add(os.path.abspath(path))
            continue

        # use cwebp to convert raw images to webp
        if name.endswith(("jpg", "jpeg", "png")) and "raw" in root:

            thumbnail_directory = os.path.join(root, "..")
            thumbnail_path = os.path.abspath(os.path.join(
                thumbnail_directory, os.path.splitext(name)[0] + ".webp"
            ))

            if path not in config or (full and config[path] != get_file_hashsum(path)):
                # Generate a thumbnail
                print(f"thumbnailing '{path}'... ", flush=True, end="")

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
                        thumbnail_path,
                    ]
                )
                print("done.", flush=True)

                new_config[path] = get_file_hashsum(path)

                something_changed = True
            else:
                # Just copy over
                new_config[path] = config[path]

            webp_files.add(os.path.abspath(thumbnail_path))

            full_size += os.path.getsize(path)
            thumbnail_size += os.path.getsize(thumbnail_path)

leftover_webps = thumbnails - webp_files

if len(leftover_webps) != 0:
    print(f"removing {len(leftover_webps)} leftover thumbnails", flush=True)

    for l in leftover_webps:
        os.remove(l)


if not os.path.exists(LEFTOVER_FOLDER):
    os.mkdir(LEFTOVER_FOLDER)

used_image_paths = extract_image_paths_from_directory([PHOTOS_FOLDER, POSTS_FOLDER])
to_remove_images = []
for path in new_config:
    if path not in used_image_paths:
        to_remove_images.append(path)

if len(to_remove_images) != 0:
    print(f"removing {len(to_remove_images)} unreferenced images (moving to {LEFTOVER_FOLDER})", flush=True)
    for image in to_remove_images:
        os.rename(image, os.path.join(LEFTOVER_FOLDER, os.path.basename(image)))

with open(CACHE_FOLDER, "w") as f:
    f.write(yaml.dump(new_config))

if something_changed:
    print(f"size before: {format_to_mb(full_size)} MB", flush=True)
    print(f"size after: {format_to_mb(thumbnail_size)} MB", flush=True)
else:
    print("no changes.", flush=True)
