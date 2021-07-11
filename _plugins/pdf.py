#!/usr/bin/env python3

# TODO:
# - proper margins
# - TOC
# - title page

import sys
import tempfile
import os
from subprocess import Popen, PIPE

os.chdir(os.path.dirname(os.path.realpath(__file__)))

path = sys.argv[1]  # path to the file
name = sys.argv[2]  # name of the post
pdf_path = os.path.join("..", "assets", name.strip("/").split("/")[-1] + ".pdf")  # resulting pdf path

with open(path) as f:
    contents = f.read()

tmp = tempfile.NamedTemporaryFile(mode="w")
tmp.write(contents)

print(Popen(["pandoc", "-f", "markdown+tex_math_single_backslash", "-i", path, "-o", pdf_path, "--pdf-engine=lualatex"], stdin=PIPE, stdout=PIPE))
