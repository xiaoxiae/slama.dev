#!/bin/python
from pathlib import Path


EXPORT_DIRECTORY = Path("../Comeback Subtitles")

BEGINNING = "1\n00:00:00,000 --> 00:00:05,000\nhttps://slama.dev/comeback/\n"


for file in sorted(Path(".").rglob("*.srt")):
    if not file.is_file():
        continue

    lang = file.parent.name

    output_directory = EXPORT_DIRECTORY / lang
    output_directory.mkdir(parents=True, exist_ok=True)
    output_file = output_directory / file.name

    with open(file, "r") as f, open(output_file, "w") as g:
        g.write(BEGINNING + "\n")

        for i, line in enumerate(f):
            if i % 4 == 0:
                g.write(f"{i // 4 + 2}\n")
            else:
                g.write(line)
