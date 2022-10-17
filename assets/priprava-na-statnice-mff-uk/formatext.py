from typing import *
from random import randint, choice, seed
from string import ascii_lowercase
from functools import lru_cache


def format(l: List[str], w=80):
    """Format a list of words into a paragraph (even the last line!)
    Do so in a way that minimizes the square of the space in a given line."""

    @lru_cache
    def _format(i: int, p: bool) -> int:
        """Return the minimal score when starting the line with the i-th word.
        If p == True, result will be printed."""
        if i == len(l) - 1:
            return 0

        # attempt to create newline at all positions (until we run out of space)
        candidates = []
        remaining = w
        for j in range(i + 1, len(l)):
            remaining -= len(l[j - 1])

            word = l[j]

            if remaining < len(word) + 1:
                break

            candidates.append((_format(j, False) + remaining ** 2, j, remaining))
            remaining -= 1

        candidates = sorted(candidates)

        # some formatting code
        if p:
            r = candidates[0][2]
            avg = r // (candidates[0][1] - i)
            r -= avg * (candidates[0][1] - i - 1)

            for j in range(i, candidates[0][1]):
                print(l[j], end=" " + (" " * avg) +
                      (" " if (j - i + 1) <= r else ""))
            print()

            _format(candidates[0][1], True)

        # take the minimum
        return candidates[0][0]

    _format(0, True)


seed(0)

n = 100
word_size = (1, 9)

words = ["".join([choice(ascii_lowercase) for _ in range(randint(*word_size))]) for _ in range(n)]

format(words)
