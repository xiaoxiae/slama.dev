#!/usr/bin/env python3

import os
import shutil
import random
import string

from pathlib import Path
from PIL import Image


os.chdir(os.path.dirname(os.path.realpath(__file__)))


def generate_random_id(length=8):
    characters = string.ascii_letters + string.digits
    random_id = ''.join(random.choice(characters) for _ in range(length))
    return random_id


def downscale_image(image_path, output_folder, max_dimension=2500):
    """Downscale image if either width or height is greater than max_dimension."""
    img = Image.open(image_path)
    width, height = img.size

    output_folder.mkdir(parents=True, exist_ok=True)

    # If either width or height is greater than max_dimension, downscale the image
    if width > max_dimension or height > max_dimension:
        # Calculate the downscaling factor

        new_width = width
        new_height = height

        while new_width > max_dimension or new_height > max_dimension:
            new_width //= 2
            new_height //= 2

        img = img.resize((new_width, new_height), Image.ANTIALIAS)

        shutil.copy(image_path, output_folder / (image_path.name + "." + generate_random_id(4)))
        img.save(image_path)
        print(f"downscaled image '{image_path}' ({width}x{height} -> {new_width}x{new_height})")

def find_and_downscale_webp_images(directory, output_folder):
    """Recursively find and downscale .webp images in the given directory."""
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(".webp"):
                downscale_image(Path(root) / file, output_folder)


print("checking image sizes.")

find_and_downscale_webp_images(Path("../assets/"), Path("../ignored/original-webp"))

