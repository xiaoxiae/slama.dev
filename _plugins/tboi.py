#!/usr/bin/env python3

import os
import re
import tempfile
import yaml

from datetime import datetime
from random import choice
from string import ascii_lowercase
from subprocess import Popen, PIPE
from typing import *


INPUT_YAML = 'tboi.yaml'
INPUT_FOLDER = "/aux/Recording/"
OUTPUT_FOLDER = "/aux/tboi/"
OUTPUT_MD = "../_includes/tboi.md"

OUTPUT_SERVER = "https://tom.ggu.cz/big/tboi/"


def stub(string: str) -> str:
    for f, t in [
        (" ", "-"),
        ("&", "and"),
        ("'", ""),
        ("!", ""),
    ]:
        string = string.replace(f, t)

    return string.lower()

def get_random_string(length: int) -> str:
    """Generate a random string."""
    result = ""
    for _ in range(length):
        result += choice(ascii_lowercase)
    return result

def run_command(command: List[str]):
    process = Popen(command, stdout=PIPE, stderr=PIPE)
    return process.communicate()

def format_image(path, alt):
    return f"<img class='inline' src='/assets/tboi/{path}.webp' alt='{alt}'>"

def get_video_duration(path):
    seconds_str, _ = run_command(["ffprobe", "-i", path, "-show_entries", "format=duration", "-v", "quiet", "-of", "csv"])
    seconds = int(float(seconds_str.decode().strip().split(",")[1]))

    duration = f"{int(seconds / 60) % 60:0>2}:{seconds % 60:0>2}"

    # yuck lmao
    if seconds >= 3600:
        duration = f"{int(seconds / 60 ** 2)}:" + ('0' if len(duration) != 5 else '') + duration

    return duration


os.chdir(os.path.dirname(os.path.realpath(__file__)))

with open(INPUT_YAML) as file:
    videos = yaml.safe_load(file)

for video in videos:
    # parse if the name is not present
    if 'name' not in video:

        # if date is missing, parse it from the file
        if 'date' not in video:
            date = datetime.strptime(video['input'][0][0], '%Y-%m-%d %H-%M-%S.mkv')

            video['date'] = date

        random_chars = get_random_string(8)

        # it's either a challenge or a regular run, they have different formats
        if 'challenge' in video:
            mid = stub(video['challenge'])
        else:
            mid = stub(video['character'])

        name = f"{video['date'].strftime('%Y-%m-%d')}-{mid}-{random_chars}.mp4"
        name_path = os.path.join(OUTPUT_FOLDER, name)

        print(f"Parsing {name}...", end="", flush=True)

        # trim and encode the individual files
        individual_files = []
        for file, start, end in video['input']:
            file_path = os.path.join(INPUT_FOLDER, file)
            tmp_path = tempfile.NamedTemporaryFile().name + ".mp4"

            individual_files.append(tmp_path)

            command = ["ffmpeg", "-y", "-i", file_path]

            if start:
                command += ["-ss", start]
            if end:
                command += ["-to", end]

            command += ["-vcodec", "libx264", "-crf", "15", tmp_path]

            run_command(command)

        # combine the files
        tmp_concat_file_path = tempfile.NamedTemporaryFile().name + ".txt"
        with open(tmp_concat_file_path, "w") as f:
            for file in individual_files:
                f.write(f"file '{file}'\n")

        command = ["ffmpeg", "-f", "concat", "-safe", "0",
                   "-i", tmp_concat_file_path, "-c", "copy", name_path]

        run_command(command)

        # cleanup
        video['name'] = name
        del video['input']

        for file_path in individual_files:
            os.remove(file_path)

        os.remove(tmp_concat_file_path)

        print(f"done.", flush=True)

    name_path = os.path.join(OUTPUT_FOLDER, video['name'])

    if not os.path.exists(name_path):
        print(f"WARNING: non-existent file '{name_path}'")

with open(INPUT_YAML, "w") as file:
    file.write(yaml.dump(videos))


with open(OUTPUT_MD, "w") as file:
    file.write("{: .center}\n### Regular runs\n\n")

    file.write(f"| Date | Character | Beaten | Link |\n| :-: | --- | --- | --: | --- |\n")

    for video in sorted(videos, key=lambda x: x['date']):
        if 'challenge' in video:
            continue

        # date
        date_str = video['date'].strftime('%Y/%m/%d')

        # character
        character = video['character']
        character_img = format_image(f"characters/{stub(character)}", f"{character} character image.")

        # bosses
        beaten_bosses = video['beaten'].split(", ")
        beaten_str = ""
        for boss in beaten_bosses:
            beaten_img = format_image(f"marks/{stub(boss)}", f"{boss} completion mark.")
            beaten_str += f"{boss} {beaten_img}<br> "

        # link
        file_duration = get_video_duration(os.path.join(OUTPUT_FOLDER, video['name']))
        file_url = os.path.join(OUTPUT_SERVER, video['name'])

        file.write(f"| **{date_str}** | {character} {character_img} | {beaten_str} | [{file_duration}]({file_url}) |\n")


    file.write("\n{: .center}\n### Challenges\n\n")

    file.write(f"| Date | Challenge | Link |\n| :-: | --- | --: | --- |\n")
    for video in sorted(videos, key=lambda x: x['date']):
        if 'challenge' not in video:
            continue

        # link
        file_duration = get_video_duration(os.path.join(OUTPUT_FOLDER, video['name']))
        file_url = os.path.join(OUTPUT_SERVER, video['name'])

        file.write(f"| **{date_str}** | {video['challenge']} | [{file_duration}]({file_url}) |\n")

print("generated!")
