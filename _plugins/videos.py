#!/usr/bin/env python3

from glob import glob
import os
import shutil
from datetime import date

OTHER_CATEGORY_NAME = "Other"

ROOT = "../ignored/videos/"
OUT = "../_includes/videos.md"
VIDEO_FOLDER = "../videos/"
URL_ROOT = "https://github.com/xiaoxiae/videos/tree/master/"

videos = {
    "Graph Theory": [
        (
            date(2021, 10, 6),
            "https://www.youtube.com/watch?v=g-QyzzPM4rU",
            "Cayley's Formula",
            "07-",
        ),
        (
            date(2021, 8, 23),
            "https://www.youtube.com/watch?v=3roPs1Bvg1Q",
            "The Blossom algorithm",
            "06-",
        ),
        (
            date(2021, 6, 1),
            "https://www.youtube.com/watch?v=Koc63QhxPgk",
            "Weak Perfect Graph Theorem",
            "04-",
        ),
        (
            date(2021, 4, 28),
            "https://www.youtube.com/watch?v=OZWZpQmGp0g",
            "Vizing's theorem",
            "03-",
        ),
    ],
    OTHER_CATEGORY_NAME: [
        (
            date(2021, 12, 31),
            "https://www.youtube.com/watch?v=KlaEp6ydVhA",
            "Bathroom Tile Programming",
            "09-",
        ),
    ],
}

os.chdir(os.path.dirname(os.path.realpath(__file__)))

result = ""

# ensure that the category "other" is the last one
# not pretty, but it works :P
for category in [v for v in videos if v != OTHER_CATEGORY_NAME] + [OTHER_CATEGORY_NAME]:
    category_str = f"### {category}\n"

    for date, youtube_link, video, folder_prefix in videos[category]:
        match = glob(os.path.join(ROOT, folder_prefix + "*"))

        if len(match) == 0:
            print(f"ERROR: video '{video}' doesn't have a folder.")

        if len(match) != 1:
            print(f"ERROR: video '{video}' has multiple folders: {match}")

        folder = match[0]

        video_slug = video.lower().replace("'", "").replace(" ", "-")

        if not os.path.exists(VIDEO_FOLDER):
            os.mkdir(VIDEO_FOLDER)

        this_video_folder = os.path.join(VIDEO_FOLDER, video_slug)

        if not os.path.exists(this_video_folder):
            os.mkdir(this_video_folder)

        # rozlišení
        resolution_paths = [f for f in glob(os.path.join(folder, "export", "*.mp4"))]
        resolutions = sorted(
            [
                int(os.path.basename(f).strip(".mp4").strip("p"))
                for f in resolution_paths
            ]
        )

        # kopírování videí
        for resolution_path in resolution_paths:
            filename = os.path.basename(resolution_path)

            if not os.path.exists(os.path.join(this_video_folder, filename)):
                shutil.copy(resolution_path, os.path.join(this_video_folder, filename))

        # kopírování titulků
        subtitle_name = "subtitles.srt"
        subtitles = glob(os.path.join(folder, "*.srt"))
        if len(subtitles) == 1:
            if not os.path.exists(os.path.join(this_video_folder, subtitle_name)):
                shutil.copy(
                    subtitles[0], os.path.join(this_video_folder, subtitle_name)
                )

        resolution_links = [
            f"[{r}p](/videos/{video_slug}/{r}p.mp4)" for r in resolutions
        ]

        with open(os.path.join(folder, "DESCRIPTION.md"), "r") as f:
            description = f.read().splitlines()[0]

        url_string = f"[code]({URL_ROOT + os.path.basename(folder)})"

        category_str += f"{date.strftime('%Y/%0m/%0d')} -- **{video}** [[YouTube]({youtube_link})] [{', '.join(resolution_links)}] [{url_string}]\n- _{description}_\n\n"

    result += category_str

with open(OUT, "w") as f:
    f.write(result)
    print("videos generated.")
