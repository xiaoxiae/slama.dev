#!/usr/bin/env python3

import os

from pathlib import Path

os.chdir(os.path.dirname(os.path.realpath(__file__)))


solved = {
    2024: [(1, 25, 2)],
    2023: [(1, 19, 2), (20, 21, 1)],
    2022: [(1, 25, 2)],
    2021: [(1, 25, 2)],
    2020: [(1, 25, 2)],
    2019: [(1, 20, 2), (21, 22, 1), (24, 24, 1)],
    2018: [(1, 14, 2), (15, 15, 1), (16, 18, 2), (19, 19, 1), (20, 20, 2), (22, 23, 1), (25, 25, 1)],
    2017: [(1, 6, 2), (7, 7, 1), (8, 8, 2)],
    2016: [(1, 5, 2)],
    2015: [(1, 17, 2)],
}

def get_day_representation(year):
    """
    Generate the HTML representation for the days of a specific year.
    - If the value for a day is 2, return <span class="gold">*</span>
    - If the value for a day is 1, return <span class="silver">*</span>
    - If the value for a day is 0 or missing, return <span class="gray">*</span>

    :param year: The year to generate the representation for.
    :return: A concatenated string of 25 day representations.
    """
    # Initialize all days to 0 (gray)
    days = [0] * 25

    # If the year exists in the solved dictionary, process its intervals
    if year in solved:
        for start, end, value in solved[year]:
            for day in range(start, end + 1):
                days[day - 1] = value  # Convert 1-based day to 0-based index

    def value_to_html(day, value):
        if value == 0:
            return f'<a href="https://adventofcode.com/{year}/day/{day}" class="gray">*</a>'
        elif value == 1:
            return f'<a href="https://adventofcode.com/{year}/day/{day}" class="silver">*</a>'
        elif value == 2:
            return f'<a href="https://adventofcode.com/{year}/day/{day}" class="gold">*</a>'

    # Generate the concatenated string
    return ''.join(value_to_html(day + 1, days[day]) for day in range(25))


output = """<div class="aoc language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>     <span class="day">1234567890123456789012345</span>
"""
for year in sorted(solved.keys(), reverse=True):

    year_class = "year-silver"
    if solved[year] == [(1, 25, 2)]:
        year_class = "year-gold"

    output += f"<a class='{year_class}' href='https://adventofcode.com/{year}/'>{year}</a> {get_day_representation(year)}\n"
output += "</code></pre></div></div>"

with open("../_includes/aoc.md", "w") as f:
    f.write(output)