#!/bin/python
from pathlib import Path
from tempfile import NamedTemporaryFile
from subprocess import Popen

import re
import shutil


REPLACEMENT_RULES = """
Add -> all
rules -> here.
"""


replacement_rules_list = []
for line in REPLACEMENT_RULES.strip().splitlines():
    source, target = line.strip().split(" -> ")
    replacement_rules_list.append((source, target))


def perform_replacements_in_file(in_path, out_path):
    with open(in_path, "r") as file:
        content = file.read()

    for pattern, replacement in replacement_rules_list:
        content = re.sub(pattern, replacement, content)

    with open(out_path, "w") as file:
        file.write(content)


# First do replacements to a temporary file
temp_file_mapping = {}
for file in sorted(Path(".").rglob("*.srt")):
    if not file.is_file():
        continue

    with NamedTemporaryFile(delete=False, suffix=".srt") as f:
        out_file = Path(f.name)

        temp_file_mapping[file] = out_file
        perform_replacements_in_file(file, out_file)


# Check diffs
for orig, tmp in sorted(temp_file_mapping.items()):
    process = Popen(["diff", "-u", str(orig), str(tmp)])
    process.communicate()


i = None
while not i or i.lower() not in "yn":
    i = input("Confirm replacement [Y/n]: ")

if i.lower() == "y":
    print("Replacing...")
    for orig, tmp in temp_file_mapping.items():
        shutil.move(tmp, orig)
else:
    print("Removing tempfiles...")
    for _, tmp in temp_file_mapping.items():
        tmp.unlink()
