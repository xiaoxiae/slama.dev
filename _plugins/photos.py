#!/usr/bin/env python3
import os
from pathlib import Path
from datetime import datetime

os.chdir(os.path.dirname(os.path.realpath(__file__)))


OUTPUT = "../_includes/photos.md"

# Define the list of image information
images = [
    {
        "date": datetime(2024, 7, 29),
        "path": Path('DSC6709.jpg'),
        "instagram_url": "https://www.instagram.com/p/C-DNxsUN-di/"
    },
    {
        "date": datetime(2024, 7, 26),
        "path": Path('tatry-1.jpg'),
        "instagram_url": "https://www.instagram.com/p/C9m__DOtQt-/?img_index=3"
    },
    {
        "date": datetime(2024, 7, 26),
        "path": Path('tatry-3.jpg'),
        "instagram_url": "https://www.instagram.com/p/C9m__DOtQt-/?img_index=2"
    },
    {
        "date": datetime(2024, 7, 26),
        "path": Path('tatry-4.jpg'),
        "instagram_url": "https://www.instagram.com/p/C9m__DOtQt-/?img_index=1"
    },
    {
        "date": datetime(2024, 7, 22),
        "path": Path('DSC9529.jpg'),
        "instagram_url": "https://www.instagram.com/p/C9kXxFKN3-s/"
    },
    {
        "date": datetime(2024, 7, 18),
        "path": Path('DSC7572.jpg'),
        "instagram_url": "https://www.instagram.com/p/C9uq4K5tiBR/?img_index=2"
    },
    {
        "date": datetime(2024, 7, 14),
        "path": Path('DSC8604.jpg'),
        "instagram_url": "https://www.instagram.com/p/C97fajytWD1/"
    },
    {
        "date": datetime(2024, 7, 9),
        "path": Path('austria-1.jpg'),
        "instagram_url": "https://www.instagram.com/p/C9NV0xKNI1s/?img_index=1"
    },
    {
        "date": datetime(2021, 10, 31),
        "path": Path('prague-4.jpg'),
        "instagram_url": "https://www.instagram.com/p/CVq_Gw3N-Y_/?img_index=4"
    },
    {
        "date": datetime(2021, 10, 31),
        "path": Path('prague-3.jpg'),
        "instagram_url": "https://www.instagram.com/p/CVq_Gw3N-Y_/?img_index=3"
    },
    {
        "date": datetime(2021, 10, 31),
        "path": Path('prague-2.jpg'),
        "instagram_url": "https://www.instagram.com/p/CVq_Gw3N-Y_/?img_index=2"
    },
    {
        "date": datetime(2021, 10, 31),
        "path": Path('prague-1.jpg'),
        "instagram_url": "https://www.instagram.com/p/CVq_Gw3N-Y_/?img_index=1"
    },
    {
        "date": datetime(2020, 10, 2),
        "path": Path('p2.jpeg'),
    },
    {
        "date": datetime(2020, 10, 2),
        "path": Path('p1.jpeg'),
    },
    {
        "date": datetime(2020, 10, 2),
        "path": Path('winter-5.jpg'),
    },
    {
        "date": datetime(2018, 6, 27),
        "path": Path('fire-1.jpg'),
        "instagram_url": "https://www.instagram.com/p/Bkg1_sKFDB4/"
    },
    {
        "date": datetime(2017, 12, 25),
        "path": Path('christmas-2018-1.jpg'),
        "instagram_url": "https://www.instagram.com/p/BdI2KnOH_If/?img_index=4"
    },
    {
        "date": datetime(2017, 12, 25),
        "path": Path('winter-4.jpg'),
        "instagram_url": "https://www.instagram.com/p/BcgD6DYlo57/"
    },
    {
        "date": datetime(2017, 7, 3),
        "path": Path('other-1.jpg'),
        "instagram_url": "https://www.instagram.com/p/BWFzjsglya6/"
    },
    {
        "date": datetime(2017, 2, 26),
        "path": Path('winter-1.jpg'),
        "instagram_url": "https://www.instagram.com/p/BH7PSl9AS5a/"
    },
    {
        "date": datetime(2016, 7, 16),
        "path": Path('sunset-2.jpg'),
        "instagram_url": "https://www.instagram.com/p/BH7PSl9AS5a/"
    },
    {
        "date": datetime(2016, 6, 30),
        "path": Path('sunset-1.jpg'),
        "instagram_url": "https://www.instagram.com/p/BHRgCv1AAVY/"
    },
    {
        "date": datetime(2015, 6, 8),
        "path": Path('flower-1.jpg'),
        "instagram_url": "https://www.instagram.com/p/3rpA4whHD7/"
    },
    {
        "date": datetime(2015, 6, 8),
        "path": Path('flower-2.jpg'),
        "instagram_url": "https://www.instagram.com/p/3rWUaeBHMQ/"
    },
    {
        "date": datetime(2015, 6, 6),
        "path": Path('bee-2.jpg'),
        "instagram_url": "https://www.instagram.com/p/3k9LqVBHM5/"
    },
]

results = "<div class='grid'>"

for image in images:
    icons = ""

    date = image['date'].strftime('%Y/%m/%d')
    path = image['path']
    photo_url = f"/photos/{path.with_suffix('.webp').name}"
    download_url = f"/photos/raw/{path}"

    icons += f"""
            <a href="{download_url}" download class="icon download">
                <i class="fas fa-download"></i>
            </a>
    """

    if 'instagram_url' in image:
        icons += f"""
                <a href="{image['instagram_url']}" target="_blank" class="icon instagram">
                    <i class="fab fa-instagram"></i>
                </a>
        """

    results += f"""
        <div>
            <div class="date">{date}</div>
            <img src="{photo_url}" alt="Image">
            <div class="icons">{icons}</div>
        </div>
"""

results += "</div>"

# Save the HTML content to a file
with open(OUTPUT, 'w') as file:
    file.write(results)

print("generated.", flush=True)

