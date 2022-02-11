#!/usr/bin/env python3

import yaml
import os
import argparse
import sys

from datetime import date


os.chdir(os.path.dirname(os.path.realpath(__file__)))

CLIMBING_FOLDER = "."
JOURNAL_PATH = os.path.join(CLIMBING_FOLDER, "journal.yaml")

parser = argparse.ArgumentParser(description="A script for adding today's climbing journal entry.")
parser.add_argument("-r", "--rebuilt", help="Whether there was a rebuild today.", action="store_true")
parser.add_argument("-f", "--force", help="Overwrite today's entry, if there was one.", action="store_true")

config = {}
if os.path.exists(JOURNAL_PATH):
    with open(JOURNAL_PATH, "r") as f:
        config = yaml.safe_load(f.read())

arguments = parser.parse_args()

entry = {
    "note": "TODO",
    "red": {"old": 0},
    "salmon": {"old": 0},
    "blue": {"old": 0},
    "yellow": {"old": 0},
}

if arguments.rebuilt:
    entry["rebuilt"] = None

if date.today() in config and not arguments.force:
    print("Today's entry exists. Use '-f' to overwrite.")
else:
    config[date.today()] = entry

    with open(JOURNAL_PATH, "w") as f:
        f.write(yaml.dump(config))
