#!/usr/bin/env python3

from glob import glob
import os
import shutil
from PIL import Image
from datetime import date

OTHER_CATEGORY_NAME = "Other"

ROOT = "../ignored/videos/"
OUT = "../_includes/videos.md"
VIDEO_FOLDER = "../videos/"
URL_ROOT = "https://github.com/xiaoxiae/videos/tree/master/"

videos = [
    ("Graph Theory", [
        (
            date(2023, 4, 9),
            "https://www.youtube.com/watch?v=lifFgyB77zc",
            "The Most Elegant Search Structure | (a,b)-trees",
            "17-",
        ),
        (
            date(2021, 10, 6),
            "https://www.youtube.com/watch?v=g-QyzzPM4rU",
            "Cayley's Formula",
            "07-",
        ),
        (
            date(2021, 8, 23),
            "https://www.youtube.com/watch?v=3roPs1Bvg1Q",
            "The Blossom Algorithm",
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
            "Vizing's Theorem",
            "03-",
        ),
    ]),
    (OTHER_CATEGORY_NAME, [
        (
            date(2021, 12, 31),
            "https://www.youtube.com/watch?v=KlaEp6ydVhA",
            "Bathroom Tile Programming",
            "09-",
        ),
        (
            date(2022, 8, 16),
            "https://www.youtube.com/watch?v=OV82ab-C85w",
            "The Remarkable BEST-SAT Algorithm",
            "10-",
        ),
        (
            date(2023, 1, 20),
            "https://www.youtube.com/watch?v=umszOeerdsU",
            "Thesesus and the Minotaur | Exploring State Space",
            "12-",
        ),
        (
            date(2023, 7, 3),
            "https://www.youtube.com/watch?v=E72DWgKP_1Y",
            "The Art of Linear Programming",
            "18-",
        ),
    ]),
    ("Shorts", [
        (
            date(2022, 11, 14),
            "https://www.youtube.com/shorts/JY0_ApbZYkQ",
            "Encoding Numbers using Dots and Parentheses",
            "13-",
        ),
        (
            date(2022, 11, 16),
            "https://youtube.com/shorts/X9pN7XZFbyE",
            "What does this weird C program do?",
            "14-",
        ),
        (
            date(2023, 2, 4),
            "https://youtube.com/shorts/q8Zuymd-ljc",
            "Undirected graphs can't equal a polynomial... or can they?",
            "16-",
        ),
        (
            date(2023, 7, 10),
            "https://youtube.com/shorts/1tYtjRSWkVk",
            "The real difference between BFS and DFS",
            "20-",
        ),
    ]),
]

os.chdir(os.path.dirname(os.path.realpath(__file__)))

result = ""

latest_video_date = date(1970, 1, 1)
latest_video = None

# ensure that the category "other" is the last one
# not pretty, but it works :P
for category, video_contents in videos:
    result += f"### {category}\n\n"

    for date, youtube_link, video, folder_prefix in reversed(sorted(video_contents)):
        match = glob(os.path.join(ROOT, folder_prefix + "*"))

        if category != "Shorts" and date > latest_video_date:
            latest_video_date = date
            latest_video = youtube_link, video

        if len(match) == 0:
            print(f"ERROR: video '{video}' doesn't have a folder.")

        if len(match) != 1:
            print(f"ERROR: video '{video}' has multiple folders: {match}")

        folder = match[0]

        video_slug = video.lower().replace(".", "").replace(" | ", " ").replace("'", "").replace(" ", "-").replace("?", "")

        if not os.path.exists(VIDEO_FOLDER):
            os.mkdir(VIDEO_FOLDER)

        this_video_folder = os.path.join(VIDEO_FOLDER, video_slug)

        if not os.path.exists(this_video_folder):
            os.mkdir(this_video_folder)

        is_short = os.path.exists(os.path.join(folder, ".short"))

        # kopírování thumbnailů
        thumbnail_name = "thumbnail.webp"
        thumbnails = glob(os.path.join(folder, "export", "thumbnail.png"))
        if len(thumbnails) == 1:
            if not os.path.exists(os.path.join(this_video_folder, thumbnail_name)):
                image = Image.open(thumbnails[0])

                if is_short:
                    size = (640, 360)
                else:
                    size = (360, 640)

                image.thumbnail(size)
                image.save(os.path.join(this_video_folder, thumbnail_name))

        with open(os.path.join(folder, "DESCRIPTION.md"), "r") as f:
            contents = f.read()

            # short has a first line that's #shorts
            if not is_short:
                description = contents.splitlines()[0]
            else:
                description = contents.splitlines()[1]

        video_escaped = video.replace(r"|", r"\|")

        if len(thumbnails) == 1 and not is_short:
            result += f"\n[![Thumbnail for the '{video_escaped}' video](/videos/{video_slug}/thumbnail.webp){{: .video-thumbnail}}]({youtube_link})\n"

        result += f"{date.strftime('%Y/%0m/%0d')} -- **{video}** [[YouTube]({youtube_link})]\n"

        description_rest = contents.split("\n\n", maxsplit=1)[1]
        result += f"<details><summary><em>{description}</em></summary> <pre>{description_rest}</pre></details>\n"
        result += "\n"


with open(OUT, "w") as f:
    f.write(result)
    print("videos generated.")
