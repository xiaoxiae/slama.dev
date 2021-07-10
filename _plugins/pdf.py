#!/usr/bin/env python3

import sys
from liquid import *

path = sys.argv[1]
name = sys.argv[2]

print(path, name)

with open(path) as f:
    contents = f.read()

env = Environment(
    undefined=StrictUndefined,
)

template = env.from_string(contents)

print(template.render())
