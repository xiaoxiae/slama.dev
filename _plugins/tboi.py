#!/usr/bin/env python3

import os
import re
import sys
import tempfile
import yaml

from datetime import datetime
from random import choice
from string import ascii_lowercase
from subprocess import Popen, PIPE
from typing import *


INPUT_YAML = 'tboi.yaml'
OUTPUT_FOLDER = "/aux/tboi/"
OUTPUT_MD = "../_includes/tboi.md"

OUTPUT_SERVER = "https://tom.ggu.cz/big/tboi/"
SYNC_COMMAND = ["rsync", "-avz", OUTPUT_FOLDER, "-e", "ssh -p 222",
                "tom@ggu.cz:users/tom/www/big/tboi"]

dry_run = len(sys.argv) == 2 and sys.argv[1] in ("-n", "--dry-run")

if not os.path.exists(OUTPUT_FOLDER):
    print(f"output folder {OUTPUT_FOLDER} doesn't exist, not generating.")
    quit()


def stub(string: str) -> str:
    for f, t in [
        (" ", "-"),
        ("&", "and"),
        ("'", ""),
        ("!", ""),
        (".", ""),
        ("/", "-"),
        ("'", ""),
    ]:
        string = string.replace(f, t)

    return string.lower()

def get_random_string(length: int) -> str:
    """Generate a random string."""
    result = ""
    for _ in range(length):
        result += choice(ascii_lowercase)
    return result

def run_command(command: List[str], pipe=None):
    process = Popen(command, stdout=PIPE, stderr=PIPE)
    return process.communicate()

def format_image(path, alt):
    image_path = f"/assets/tboi/{path}.webp"

    if not os.path.exists('..' + image_path):
        print(f"WARNING: non-existent image {image_path}")

    alt = alt.replace("'", "")

    return f"<img class='inline' src='{image_path}' alt='{alt}'>"

def get_video_duration(path):
    seconds_str, _ = run_command(["ffprobe", "-i", path, "-show_entries", "format=duration", "-v", "quiet", "-of", "csv"])

    try:
        seconds = int(float(seconds_str.decode().strip().split(",")[1]))

        duration = f"{int(seconds / 60) % 60:0>2}:{seconds % 60:0>2}"

        # yuck lmao
        if seconds >= 3600:
            duration = f"{int(seconds / 60 ** 2)}:" + ('0' if len(duration) != 5 else '') + duration

        return duration
    except Exception:
        print(f"WARNING: unknown duration for file '{path}'")
        return "?"



os.chdir(os.path.dirname(os.path.realpath(__file__)))

change = False

with open(INPUT_YAML) as file:
    videos = yaml.safe_load(file)

for video in videos:
    # if date is missing, parse it from the input file
    if 'date' not in video:
        video['date'] = datetime.fromtimestamp(os.path.getmtime(video['input'][0][0]))

    # parse if the name is not present
    if 'name' in video:
        continue

    change = True

    random_chars = get_random_string(8)

    # it's either a challenge or a regular run, they have different formats
    if 'challenge' in video:
        mid = stub(video['challenge'])
    elif 'daily' in video:
        mid = "daily-" + stub(video['character']) + "-" + stub(video['daily'])
    else:
        mid = stub(video['character'])

    name = f"{video['date'].strftime('%Y-%m-%d')}-{mid}-{random_chars}.mp4"
    name_path = os.path.join(OUTPUT_FOLDER, name)

    if not dry_run:
        print(f"Parsing {name}...", end="", flush=True)
    else:
        print(f"Parsing {name}...", flush=True)

    # trim and encode the individual files
    individual_files = []
    for file, start, end in video['input']:
        tmp_path = tempfile.NamedTemporaryFile().name + ".mp4"

        individual_files.append(tmp_path)

        command = ["ffmpeg", "-y", "-i", file]

        if start:
            command += ["-ss", start]
        if end:
            command += ["-to", end]

        command += ["-vcodec", "libx264", "-crf", "15", tmp_path]

        if not dry_run:
            run_command(command)
        else:
            print("Dry run:", command)

    # combine the files
    tmp_concat_file_path = tempfile.NamedTemporaryFile().name + ".txt"
    with open(tmp_concat_file_path, "w") as f:
        for file in individual_files:
            f.write(f"file '{file}'\n")

    command = ["ffmpeg", "-f", "concat", "-safe", "0",
               "-i", tmp_concat_file_path, "-c", "copy", name_path]

    if not dry_run:
        run_command(command)
    else:
        print("Dry run:", command)

    # cleanup
    video['name'] = name

    if not dry_run:
        for file_path in individual_files:
            os.remove(file_path)

        os.remove(tmp_concat_file_path)

    if not dry_run:
        print(f"done.", flush=True)


note = """# New entry formats:
# (time format: 1:32:23.321; null to not cut)
#
# - beaten:
#   character:
#   input:
#   - ["/aux/Recording/", null, null]
#
# - challenge:
#   input:
#   - ["/aux/Recording/", null, null]
#
# - daily:
#   input:
#   - ["/aux/Recording/", null, null]
#
"""

if dry_run:
    quit()

# backup
os.rename(INPUT_YAML, "." + INPUT_YAML)

with open(INPUT_YAML, "w") as file:
    file.write(note)
    file.write(yaml.dump(videos))

with open(OUTPUT_MD, "w") as file:
    file.write("{: .center}\n### Regular runs\n\n")

    file.write(f"| Date | Character | Beaten | Link | Items |\n| :-: | --- | --- | --: | --- | --- |\n")

    for video in reversed(sorted(videos, key=lambda x: x['date'])):
        if 'name' not in video:
            print(f"WARNING: unprocessed run {video}")
            continue

        if 'challenge' in video:
            continue

        if 'daily' in video:
            continue

        # date
        date_str = video['date'].strftime('%Y/%m/%d')

        # character
        character = video['character']
        character_img = format_image(f"characters/{stub(character)}", f"{character} character image.")

        # bosses
        beaten_str = ""
        for boss in video['beaten'].split(", "):
            beaten_img = format_image(f"marks/{stub(boss)}", f"{boss} completion mark.")
            beaten_str += f"{boss} {beaten_img}<br> "

        items_str = ""
        if 'items' in video:
            for item in video['items'].split(", "):
                items_str += format_image(f"items/{stub(item)}", f"{item} item icon.") + " "

        # link
        file_duration = get_video_duration(os.path.join(OUTPUT_FOLDER, video['name']))
        file_url = os.path.join(OUTPUT_SERVER, video['name'])

        file.write(f"| **{date_str}** | {character} {character_img} | {beaten_str} | [{file_duration}]({file_url}) | {items_str} |\n")


    # NOTE: challenges commented out for now
    #
    # file.write("\n{: .center}\n### Challenges\n\n")

    # file.write(f"| Date | Challenge | Link |\n| :-: | --- | --: | --- |\n")
    # for video in reversed(sorted(videos, key=lambda x: x['date'])):
    #     if 'challenge' not in video:
    #         continue

    #     # date
    #     date_str = video['date'].strftime('%Y/%m/%d')

    #     # link
    #     file_duration = get_video_duration(os.path.join(OUTPUT_FOLDER, video['name']))
    #     file_url = os.path.join(OUTPUT_SERVER, video['name'])

    #     file.write(f"| **{date_str}** | {video['challenge']} | [{file_duration}]({file_url}) |\n")


    # NOTE: daily runs commented out for now
    #
    # file.write("\n{: .center}\n### Daily Runs\n\n")

    # file.write(f"| Date | Character | Target | Link |\n| :-: | --- | --- | --: | --- |\n")
    # for video in reversed(sorted(videos, key=lambda x: x['date'])):
    #     if 'daily' not in video:
    #         continue

    #     # date
    #     date_str = video['date'].strftime('%Y/%m/%d')

    #     # character
    #     character = video['character']
    #     character_img = format_image(f"characters/{stub(character)}", f"{character} character image.")

    #     # link
    #     file_duration = get_video_duration(os.path.join(OUTPUT_FOLDER, video['name']))
    #     file_url = os.path.join(OUTPUT_SERVER, video['name'])

    #     file.write(f"| **{date_str}** | {character} {character_img} | {video['daily']} | [{file_duration}]({file_url}) |\n")

if change or (len(sys.argv) == 2 and sys.argv[1] in ("-f", "--force")):
    print("generated, syncing... ", end="", flush=True)
    input("press enter to input server's password (to prevent SSH timeout):")
    run_command(SYNC_COMMAND)
    print("synced.")
else:
    print("generated, no changes.", flush=True)
