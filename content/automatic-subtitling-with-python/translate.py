#!/bin/python
from pathlib import Path
from subprocess import Popen, PIPE
from tempfile import NamedTemporaryFile
from tqdm import tqdm

import shutil


PROMPT = "Translate the following line from a Czech subtitle to English. Only include the response: "


for file in sorted(Path(".").rglob("*.srt")):
    if not file.is_file():
        continue

    # Czech -> English
    if file.parent.name != "cz":
        continue

    en_file = file.parent.parent / "en" / file.name
    en_file.parent.mkdir(parents=True, exist_ok=True)

    # Skip if it already exists
    if en_file.exists():
        continue

    print(f"Translating '{file.name}'...")
    with open(file, "r") as f, NamedTemporaryFile(mode="w", delete=False) as g:
        lines = f.read().splitlines()

        # I hope this is a safe assumption :)
        for i, line in tqdm(enumerate(lines), total=len(lines)):
            if i % 4 != 2:
                g.write(line + "\n")
                continue

            process = Popen(
                ["ollama", "run", "mistral", PROMPT + "[" + line.strip() + "]"],
                stdout=PIPE,
                stderr=PIPE,
            )

            if i > 10:
                break

            stdout, _ = process.communicate()

            # the LLM sometimes doesn't exactly follow the prompt, so we only keep the first line
            stdout = stdout.decode().strip().splitlines()[0]

            g.write(stdout + "\n")

    shutil.move(g.name, en_file)
