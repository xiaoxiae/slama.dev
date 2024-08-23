#!/usr/bin/env python3
import os
from pathlib import Path
from datetime import datetime

os.chdir(os.path.dirname(os.path.realpath(__file__)))


OUTPUT = "../_includes/photos.md"

# Define the list of image information
images = [
    {
        "date": datetime(2024, 8, 22),
        "path": Path('2024-08-22-duck.jpg'),
        "instagram_url": "https://www.instagram.com/p/C--dPuqtePV/"
    },
    {
        "date": datetime(2024, 8, 19),
        "path": Path('2024-08-19-frog.jpg'),
        "instagram_url": "https://www.instagram.com/p/C-2xNP6tQNo/"
    },
    {
        "date": datetime(2024, 8, 18),
        "path": Path('2024-08-18-lizard.jpg'),
        "instagram_url": "https://www.instagram.com/p/C-0I-8KNd2f/"
    },
    {
        "date": datetime(2024, 8, 16),
        "path": Path('2024-08-16-birdhouse.jpg'),
        "instagram_url": "https://www.instagram.com/p/C-5Xo_fNDkg/"
    },
    {
        "date": datetime(2024, 8, 12),
        "path": Path('2024-08-12-moon.jpg'),
        "instagram_url": "https://www.instagram.com/p/C-k_hBBtLsK/"
    },
    {
        "date": datetime(2024, 8, 11),
        "path": Path('2024-08-11-protab.jpg'),
        "instagram_url": "https://www.instagram.com/p/C-iEwWLt4nI/"
    },
    {
        "date": datetime(2024, 8, 7),
        "path": Path('2024-08-07-cat.jpg'),
        "instagram_url": "https://www.instagram.com/p/C-X7nbfiEKq/"
    },
    {
        "date": datetime(2024, 7, 29),
        "path": Path('2024-07-29-berd.jpg'),
        "instagram_url": "https://www.instagram.com/p/C-DNxsUN-di/"
    },
    {
        "date": datetime(2024, 7, 26),
        "path": Path('2024-07-26-tatry-1.jpg'),
        "instagram_url": "https://www.instagram.com/p/C9m__DOtQt-/?img_index=3"
    },
    {
        "date": datetime(2024, 7, 26),
        "path": Path('2024-07-26-tatry-3.jpg'),
        "instagram_url": "https://www.instagram.com/p/C9m__DOtQt-/?img_index=2"
    },
    {
        "date": datetime(2024, 7, 26),
        "path": Path('2024-07-26-tatry-4.jpg'),
        "instagram_url": "https://www.instagram.com/p/C9m__DOtQt-/?img_index=1"
    },
    {
        "date": datetime(2024, 7, 22),
        "path": Path('2024-07-22-vrat.jpg'),
        "instagram_url": "https://www.instagram.com/p/C9kXxFKN3-s/"
    },
    {
        "date": datetime(2024, 7, 18),
        "path": Path('2024-07-18-squirrel.jpg'),
        "instagram_url": "https://www.instagram.com/p/C9uq4K5tiBR/?img_index=2"
    },
    {
        "date": datetime(2024, 7, 14),
        "path": Path('2024-07-14-moon.jpg'),
        "instagram_url": "https://www.instagram.com/p/C97fajytWD1/"
    },
    {
        "date": datetime(2024, 7, 9),
        "path": Path('2024-07-09-austria.jpg'),
        "instagram_url": "https://www.instagram.com/p/C9NV0xKNI1s/?img_index=1"
    },
    {
        "date": datetime(2021, 10, 31),
        "path": Path('2021-10-31-prague-4.jpg'),
        "instagram_url": "https://www.instagram.com/p/CVq_Gw3N-Y_/?img_index=4"
    },
    {
        "date": datetime(2021, 10, 31),
        "path": Path('2021-10-31-prague-3.jpg'),
        "instagram_url": "https://www.instagram.com/p/CVq_Gw3N-Y_/?img_index=3"
    },
    {
        "date": datetime(2021, 10, 31),
        "path": Path('2021-10-31-prague-2.jpg'),
        "instagram_url": "https://www.instagram.com/p/CVq_Gw3N-Y_/?img_index=2"
    },
    {
        "date": datetime(2021, 10, 31),
        "path": Path('2021-10-31-prague-1.jpg'),
        "instagram_url": "https://www.instagram.com/p/CVq_Gw3N-Y_/?img_index=1"
    },
    {
        "date": datetime(2020, 10, 2),
        "path": Path('2020-10-02-panorama-2.jpeg'),
    },
    {
        "date": datetime(2020, 10, 2),
        "path": Path('2020-10-02-panorama-1.jpeg'),
    },
    {
        "date": datetime(2020, 10, 2),
        "path": Path('2020-10-02-winter.jpg'),
    },
    {
        "date": datetime(2018, 6, 27),
        "path": Path('2018-06-27-fire.jpg'),
        "instagram_url": "https://www.instagram.com/p/Bkg1_sKFDB4/"
    },
    {
        "date": datetime(2017, 12, 25),
        "path": Path('2017-12-25-christmas.jpg'),
        "instagram_url": "https://www.instagram.com/p/BdI2KnOH_If/?img_index=4"
    },
    {
        "date": datetime(2017, 12, 25),
        "path": Path('2017-12-25-winter.jpg'),
        "instagram_url": "https://www.instagram.com/p/BcgD6DYlo57/"
    },
    {
        "date": datetime(2017, 7, 3),
        "path": Path('2017-07-03-other.jpg'),
        "instagram_url": "https://www.instagram.com/p/BWFzjsglya6/"
    },
    {
        "date": datetime(2017, 2, 26),
        "path": Path('2017-02-26-winter.jpg'),
        "instagram_url": "https://www.instagram.com/p/BH7PSl9AS5a/"
    },
    {
        "date": datetime(2016, 7, 16),
        "path": Path('2016-07-16-sunset.jpg'),
        "instagram_url": "https://www.instagram.com/p/BH7PSl9AS5a/"
    },
    {
        "date": datetime(2016, 6, 30),
        "path": Path('2016-06-30-sunset.jpg'),
        "instagram_url": "https://www.instagram.com/p/BHRgCv1AAVY/"
    },
    {
        "date": datetime(2015, 6, 8),
        "path": Path('2015-06-08-flower-2.jpg'),
        "instagram_url": "https://www.instagram.com/p/3rpA4whHD7/"
    },
    {
        "date": datetime(2015, 6, 8),
        "path": Path('2015-06-08-flower-1.jpg'),
        "instagram_url": "https://www.instagram.com/p/3rWUaeBHMQ/"
    },
    {
        "date": datetime(2015, 6, 6),
        "path": Path('2015-06-06-bee.jpg'),
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

