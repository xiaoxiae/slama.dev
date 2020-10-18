#!/usr/bin/python3

import os
import sys
from subprocess import Popen, DEVNULL, PIPE

import re

from typing import *


base = os.path.dirname(os.path.realpath(__file__))

title = sys.argv[1]
filename = sys.argv[2]
regex = r"{%\s+match\s+(.+?)\s+%}"
languages = []

for root, dirs, files in os.walk(os.path.join(base, "../_wiki/languages/")):
    for f in files:
        if f.endswith(".md") and not f.endswith(os.path.basename(filename)):
            with open(os.path.join(base, root, f), "r") as fp:
                contents = fp.read()
                m = re.findall(regex, contents, re.MULTILINE)

                if title.strip() in m:
                    languages.append(
                        (
                            f,
                            (
                                re.findall("title:\s+(.+)$", contents, re.MULTILINE)
                                or [f[:-3].capitalize()]
                            )[0],
                        )
                    )


depth = title.split()[0].count("#")
name = " ".join(title.split()[1:])
links = (
    "["
    + ", ".join(
        [
            f'<a href="/wiki/languages/{filename[:-3]}/#{name.lower()}">{language}</a>'
            for filename, language in sorted(languages, key=lambda x: x[1])
        ]
    )
    + "]"
)

print(
    f"<h{depth} id='{name.lower()}'>{name} {links if links != '[]' else ''}</h{depth}>"
)
