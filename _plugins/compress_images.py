#!/usr/bin/env python3

import os
import re
import sys
import hashlib
from PIL import Image, ImageFilter
from typing import *
from subprocess import Popen, PIPE
from pathlib import Path

import yaml


os.chdir(os.path.dirname(os.path.realpath(__file__)))
CACHE_FOLDER = Path("../.jekyll-cache/compress_images")
PHOTOS_FOLDER = Path("../photos/")
POSTS_FOLDER = Path("../_posts/")
LEFTOVER_FOLDER = Path("../ignored/automatically-removed-photos/")
THUMBNAIL_WEBP_PATH = PHOTOS_FOLDER / "thumbnail.webp"

full_size = 0  # total size of images before compression
thumbnail_size = 0  # total size of images before compression
something_changed = False

full = False
if len(sys.argv) == 2 and sys.argv[1] in ("-f", "--full"):
    full = True

def get_file_hashsum(file_name: str | Path):
    """Generate a SHA-256 hashsum of the given file."""
    hash_sha256 = hashlib.sha256()
    with open(file_name, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()

def execute_shell_command(command: list[str]):
    result = Popen(command, stdout=PIPE, stderr=PIPE).communicate()

def format_to_mb(size: int) -> str:
    """Format to megabytes."""
    return round(size / (1024**2), 2)

def extract_image_paths_from_markdown(markdown_content) -> list[Path]:
    """Extracts image paths from Markdown content containing Liquid tags."""
    liquid_tag_pattern = r'{%\s*photos\s*(.+)\s*%}'
    liquid_tags = re.findall(liquid_tag_pattern, markdown_content)
    image_paths = []
    for tag in liquid_tags:
        paths = tag.split('|')
        for path in paths:
            image_path = path.split('&')[0].strip()
            image_paths.append(PHOTOS_FOLDER / image_path)
    return image_paths

def find_markdown_files(directory) -> list[Path]:
    """Finds all Markdown files in a directory and its subdirectories."""
    markdown_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".md"):
                markdown_files.append(Path(root) / file)
    return markdown_files

def extract_image_paths_from_directory(directories) -> set[Path]:
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
if CACHE_FOLDER.exists():
    with open(CACHE_FOLDER, "r") as f:
        config = yaml.safe_load(f.read()) or {}

config = {Path(k): v for k, v in config.items()}

thumbnails = set()
webp_files = set()
thumbnail_images = {}

for root, dirs, files in os.walk(PHOTOS_FOLDER, followlinks=True):
    for name in files:
        path = Path(root) / name
        name = Path(name)

        if name.suffix == ".webp":
            thumbnails.add(path.absolute())
            continue

        if name.suffix in (".jpg", ".jpeg", ".png") and path.parent.name == "raw":
            thumbnail_directory = path.parent.parent
            thumbnail_path = (thumbnail_directory / name.with_suffix(".webp")).absolute()

            if path not in config or (full and config[path] != get_file_hashsum(path)):
                print(f"thumbnailing '{path}'... ", flush=True, end="")
                with Image.open(path) as im:
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
                new_config[path] = config[path]

            webp_files.add(thumbnail_path.absolute())
            full_size += os.path.getsize(path)
            thumbnail_size += os.path.getsize(thumbnail_path)

            if thumbnail_directory not in thumbnail_images:
                thumbnail_images[thumbnail_directory] = []

            thumbnail_images[thumbnail_directory].append(thumbnail_path)

leftover_webps = thumbnails - webp_files
leftover_webps = [p for p in leftover_webps if p.name != "thumbnail.webp"]

if len(leftover_webps) != 0:
    print(f"removing {len(leftover_webps)} leftover thumbnails", flush=True)
    for l in leftover_webps:
        l.unlink()

if not LEFTOVER_FOLDER.exists():
    LEFTOVER_FOLDER.mkdir()

used_image_paths = extract_image_paths_from_directory([PHOTOS_FOLDER, POSTS_FOLDER])
to_remove_images = []
for path in new_config:
    if path not in used_image_paths:
        to_remove_images.append(path)

if len(to_remove_images) != 0:
    print(f"removing {len(to_remove_images)} unreferenced images (moving to {LEFTOVER_FOLDER})", flush=True)
    for image in to_remove_images:
        image.rename(image, LEFTOVER_FOLDER / image.name)

with open(CACHE_FOLDER, "w") as f:
    new_config = {str(k): v for k, v in new_config.items()}
    f.write(yaml.dump(new_config))

if something_changed:
    print(f"size before: {format_to_mb(full_size)} MB", flush=True)
    print(f"size after: {format_to_mb(thumbnail_size)} MB", flush=True)
else:
    print("no changes.", flush=True)

# Create a concatenated thumbnail image
if something_changed:
    print(f"generating concatenated thumbnails.")
    for path, imgs in thumbnail_images.items():
        tiny_size = 128
        gap_size = 10

        thumbnail_images = [Image.open(img) for img in imgs]

        for t in thumbnail_images:
            t.thumbnail((tiny_size, t.height / t.width * tiny_size))

        total_width = sum(img.width for img in thumbnail_images) + gap_size * (len(thumbnail_images) - 1)
        max_height = max(img.height for img in thumbnail_images)

        new_im = Image.new('RGBA', (total_width, max_height), (255, 255, 255, 0))
        x_offset = 0
        for img in thumbnail_images:
            new_im.paste(img, (x_offset, 0), img.convert('RGBA'))
            x_offset += img.width + gap_size

        new_im.filter(ImageFilter.BLUR)

        new_im.save(path / "thumbnail.webp", "WEBP")
