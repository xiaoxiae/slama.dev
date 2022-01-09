#!/usr/bin/env python3

import os
import argparse
from lxml import etree

os.chdir(os.path.dirname(os.path.realpath(__file__)))

parser = argparse.ArgumentParser(description="Fill the closest point on the productivitree.")

group = parser.add_mutually_exclusive_group(required=True)

group.add_argument(
    "-e",
    "--education",
    action='store_true',
)

group.add_argument(
    "-o",
    "--other",
    action='store_true',
)

parser.add_argument(
    "-n",
    type=int,
    default=1,
)

arguments = parser.parse_args()

FILE = "../assets/productivitree.svg"

AVAILABLE_COLOR = "#e6e6e6"

EDUCATION_COLOR = "#0000ff"
OTHER_COLOR = "#000000"

for _ in range(arguments.n):
    doc = etree.parse(FILE)
    root = doc.getroot()
    g = [f for f in root.getchildren() if f.tag.endswith("g")][0]

    available_points = []
    taken_points = []

    def split_to_dict(string):
        return {k:v for k, v in [p.split(":") for p in string.split(";")]}

    def join_to_dict(dict):
        return ";".join([f"{k}:{v}" for k, v in dict.items()])

    for child in g.getchildren():
        d = split_to_dict(child.attrib['style'])

        if d['stroke'] == AVAILABLE_COLOR:
            available_points.append(child)
        else:
            taken_points.append(child)

    closest_point_distance = float('inf')
    closest_point = None

    def distance(p1, center):
        return (abs(float(p1.attrib['cx']) - center[0])) ** 2 + \
            (abs(float(p1.attrib['cy']) - center[1])) ** 2

    center = [0, 0]
    for p in taken_points:
        center[0] += float(p.attrib['cx'])
        center[1] += float(p.attrib['cy'])
    center[0] /= len(taken_points)
    center[1] /= len(taken_points)

    for p1 in available_points:
        if distance(p1, center) < closest_point_distance:
            closest_point_distance = distance(p1, center)
            closest_point = p1

    d = split_to_dict(p1.attrib['style'])

    if arguments.education:
        d['stroke'] = EDUCATION_COLOR
        d['fill'] = EDUCATION_COLOR
    elif arguments.other:
        d['stroke'] = OTHER_COLOR
        d['fill'] = OTHER_COLOR

    closest_point.attrib['style'] = join_to_dict(d)

    doc.write(FILE)
