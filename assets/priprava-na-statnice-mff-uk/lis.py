from typing import *
from functools import lru_cache


def longest_increasing_subsequence(l: List[int]):
    """Return the longest increasing subsequence of the list."""
    l = [float("-inf")] + l

    @lru_cache
    def _lis(i: int) -> int:
        """Return the longest increasing subsequence that starts with the i-th element."""
        if i == len(l) - 1:
            return 1

        candidates = [0]
        for j in range(i + 1, len(l)):
            if l[i] < l[j]:
                candidates.append(_lis(j))

        return 1 + max(candidates)

    return _lis(0) - 1

print(longest_increasing_subsequence([10, 10, 10, 10, 10, -1, 1, 2, 4, 3, 9, 7, 2, 9, 10] * 10))
