#!/usr/bin/env python3
import os
from pathlib import Path
from datetime import datetime

os.chdir(os.path.dirname(os.path.realpath(__file__)))


OUTPUT = "../_includes/photos.md"


# Define the list of image information
images = [
    {
        "path": Path('2024-11-19-paris-duck.jpg'),
    },
    {
        "path": Path('2024-11-16-paris-statue.jpg'),
    },
    {
        "path": Path('2024-11-13-paris-eiffel.jpg'),
    },
    {
        "path": Path('2024-11-10-oviedo-seagul.jpg'),
        "instagram_url": "https://www.instagram.com/p/DCM2X8YoDex/"
    },
    {
        "path": Path('2024-11-06-oviedo-crow.jpg'),
        "instagram_url": "https://www.instagram.com/p/DCCBhNCoCfI/"
    },
    {
        "path": Path('2024-11-03-oviedo-lake.jpg'),
        "instagram_url": "https://www.instagram.com/p/DB6AlhnIr1m/"
    },
    {
        "path": Path('2024-10-31-oviedo-lizard.jpg'),
        "instagram_url": "https://www.instagram.com/p/DBzAUUYI6MV/"
    },
    {
        "path": Path('2024-10-28-oviedo-panorama.jpg'),
        "instagram_url": "https://www.instagram.com/p/DBrLFBBIBog/"
    },
    {
        "path": Path('2024-10-16-panorama.jpg'),
        "instagram_url": "https://www.instagram.com/p/DBMKqFVo8yn/"
    },
    {
        "path": Path('2024-10-13-fire.jpg'),
        "instagram_url": "https://www.instagram.com/p/DBEcVFSIYYM/"
    },
    {
        "path": Path('2024-10-10-bird.jpg'),
        "instagram_url": "https://www.instagram.com/p/DA8uhEutbjS/"
    },
    {
        "path": Path('2024-10-07-austria-10-cows.jpg'),
        "instagram_url": "https://www.instagram.com/p/DA0-9NWtBFq/"
    },
    {
        "path": Path('2024-10-04-austria-9-mountains.jpg'),
        "instagram_url": "https://www.instagram.com/p/DAtQo4Xtpk7/"
    },
    {
        "path": Path('2024-10-01-austria-8-mountains.jpg'),
        "instagram_url": "https://www.instagram.com/p/DAlloUrNi28/"
    },
    {
        "path": Path('2024-09-28-austria-7-otis.jpg'),
        "instagram_url": "https://www.instagram.com/p/DAd0XEPtCIy/"
    },
    {
        "path": Path('2024-09-25-austria-6-water.jpg'),
        "instagram_url": "https://www.instagram.com/p/DAWE0Yytsy3/"
    },
    {
        "path": Path('2024-09-23-austria-5-mountains.jpg'),
        "instagram_url": "https://www.instagram.com/p/DAQ9B3ytjw8/"
    },
    {
        "path": Path('2024-09-21-austria-4-clouds.jpg'),
        "instagram_url": "https://www.instagram.com/p/DALy2oqtW3g/"
    },
    {
        "path": Path('2024-09-19-austria-3-water.jpg'),
        "instagram_url": "https://www.instagram.com/p/DAGpP9LN-pY/"
    },
    {
        "path": Path('2024-09-17-austria-2-stars.jpg'),
        "instagram_url": "https://www.instagram.com/p/DABfnHytIH-/"
    },
    {
        "path": Path('2024-09-15-austria-1-sunset.jpg'),
        "instagram_url": "https://www.instagram.com/p/C_8VcJhtyq6/"
    },
    {
        "path": Path('2024-09-12-romania-10-catto.jpg'),
    },
    {
        "path": Path('2024-09-11-romania-9-forest.jpg'),
        "instagram_url": "https://www.instagram.com/p/C_yC3rztXDn/"
    },
    {
        "path": Path('2024-09-10-romania-8-feather.jpg'),
        "instagram_url": "https://www.instagram.com/p/C_vdfYGtpzB/"
    },
    {
        "path": Path('2024-09-09-romania-7-doggo.jpg'),
        "instagram_url": "https://www.instagram.com/p/C_sxVMdNrY2/"
    },
    {
        "path": Path('2024-09-08-romania-6-doggo.jpg'),
        "instagram_url": "https://www.instagram.com/p/C_qL6T-NekZ/"
    },
    {
        "path": Path('2024-09-07-romania-5-statue.jpg'),
        "instagram_url": "https://www.instagram.com/p/C_nnElXtAw8/"
    },
    {
        "path": Path('2024-09-06-romania-4-doggo.jpg'),
        "instagram_url": "https://www.instagram.com/p/C_lC4WINB3E/"
    },
    {
        "path": Path('2024-09-05-romania-3-crows.jpg'),
        "instagram_url": "https://www.instagram.com/p/C_ic_17Nlvb/"
    },
    {
        "path": Path('2024-09-04-romania-2-dome.jpg'),
        "instagram_url": "https://www.instagram.com/p/C_f3jZltPjF/"
    },
    {
        "path": Path('2024-09-03-romania-1-summit.jpg'),
        "instagram_url": "https://www.instagram.com/p/C_dSzOitq8U/"
    },
    {
        "path": Path('2024-08-30-cabin.jpg'),
        "instagram_url": "https://www.instagram.com/p/C_TIOcVNtUo/"
    },
    {
        "path": Path('2024-08-25-frog.jpg'),
        "instagram_url": "https://www.instagram.com/p/C-2xNP6tQNo/"
    },
    {
        "path": Path('2024-08-22-duck.jpg'),
        "instagram_url": "https://www.instagram.com/p/C--dPuqtePV/"
    },
    {
        "path": Path('2024-08-18-lizard.jpg'),
        "instagram_url": "https://www.instagram.com/p/C-0I-8KNd2f/"
    },
    {
        "path": Path('2024-08-16-birdhouse.jpg'),
        "instagram_url": "https://www.instagram.com/p/C-5Xo_fNDkg/"
    },
    {
        "path": Path('2024-08-12-moon.jpg'),
        "instagram_url": "https://www.instagram.com/p/C-k_hBBtLsK/"
    },
    {
        "path": Path('2024-08-11-protab.jpg'),
        "instagram_url": "https://www.instagram.com/p/C-iEwWLt4nI/"
    },
    {
        "path": Path('2024-08-07-cat.jpg'),
        "instagram_url": "https://www.instagram.com/p/C-X7nbfiEKq/"
    },
    {
        "path": Path('2024-07-29-berd.jpg'),
        "instagram_url": "https://www.instagram.com/p/C-DNxsUN-di/"
    },
    {
        "path": Path('2024-07-26-tatry-1.jpg'),
        "instagram_url": "https://www.instagram.com/p/C9m__DOtQt-/?img_index=3"
    },
    {
        "path": Path('2024-07-26-tatry-3.jpg'),
        "instagram_url": "https://www.instagram.com/p/C9m__DOtQt-/?img_index=2"
    },
    {
        "path": Path('2024-07-26-tatry-4.jpg'),
        "instagram_url": "https://www.instagram.com/p/C9m__DOtQt-/?img_index=1"
    },
    {
        "path": Path('2024-07-22-vrat.jpg'),
        "instagram_url": "https://www.instagram.com/p/C9kXxFKN3-s/"
    },
    {
        "path": Path('2024-07-18-squirrel.jpg'),
        "instagram_url": "https://www.instagram.com/p/C9uq4K5tiBR/?img_index=2"
    },
    {
        "path": Path('2024-07-14-moon.jpg'),
        "instagram_url": "https://www.instagram.com/p/C97fajytWD1/"
    },
    {
        "path": Path('2024-07-09-austria.jpg'),
        "instagram_url": "https://www.instagram.com/p/C9NV0xKNI1s/?img_index=1"
    },
    {
        "path": Path('2021-10-31-prague-4.jpg'),
        "instagram_url": "https://www.instagram.com/p/CVq_Gw3N-Y_/?img_index=4"
    },
    {
        "path": Path('2021-10-31-prague-3.jpg'),
        "instagram_url": "https://www.instagram.com/p/CVq_Gw3N-Y_/?img_index=3"
    },
    {
        "path": Path('2021-10-31-prague-2.jpg'),
        "instagram_url": "https://www.instagram.com/p/CVq_Gw3N-Y_/?img_index=2"
    },
    {
        "path": Path('2021-10-31-prague-1.jpg'),
        "instagram_url": "https://www.instagram.com/p/CVq_Gw3N-Y_/?img_index=1"
    },
    {
        "path": Path('2020-10-02-panorama-2.jpeg'),
    },
    {
        "path": Path('2020-10-02-panorama-1.jpeg'),
    },
    {
        "path": Path('2020-10-02-winter.jpg'),
    },
    {
        "path": Path('2018-06-27-fire.jpg'),
        "instagram_url": "https://www.instagram.com/p/Bkg1_sKFDB4/"
    },
    {
        "path": Path('2017-12-25-christmas.jpg'),
        "instagram_url": "https://www.instagram.com/p/BdI2KnOH_If/?img_index=4"
    },
    {
        "path": Path('2017-12-25-winter.jpg'),
        "instagram_url": "https://www.instagram.com/p/BcgD6DYlo57/"
    },
    {
        "path": Path('2017-07-03-other.jpg'),
        "instagram_url": "https://www.instagram.com/p/BWFzjsglya6/"
    },
    {
        "path": Path('2017-02-26-winter.jpg'),
        "instagram_url": "https://www.instagram.com/p/BH7PSl9AS5a/"
    },
    {
        "path": Path('2016-07-16-sunset.jpg'),
        "instagram_url": "https://www.instagram.com/p/BH7PSl9AS5a/"
    },
    {
        "path": Path('2016-06-30-sunset.jpg'),
        "instagram_url": "https://www.instagram.com/p/BHRgCv1AAVY/"
    },
    {
        "path": Path('2015-06-08-flower-2.jpg'),
        "instagram_url": "https://www.instagram.com/p/3rpA4whHD7/"
    },
    {
        "path": Path('2015-06-08-flower-1.jpg'),
        "instagram_url": "https://www.instagram.com/p/3rWUaeBHMQ/"
    },
    {
        "path": Path('2015-06-06-bee.jpg'),
        "instagram_url": "https://www.instagram.com/p/3k9LqVBHM5/"
    },
]

results = "<div class='grid'>"

for image in images:
    icons = ""

    path = image['path']

    date = datetime.strptime(path.name[:10], '%Y-%m-%d')
    date_string = date.strftime('%Y/%m/%d')

    if date > datetime.now():
        print(f"got future image '{path}' ({date_string} > today), skipping.")
        continue

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
            <div class="date">{date_string}</div>
            <img src="{photo_url}" alt="Image">
            <div class="icons">{icons}</div>
        </div>
"""

results += "</div>"

# Save the HTML content to a file
with open(OUTPUT, 'w') as file:
    file.write(results)

print("generated.", flush=True)

