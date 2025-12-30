from typing import *


State = int
String = str


def kmp(needle: String, haystack: String) -> List[int]:
    """A KMP implementation to return all occurrences of a needle in a haystack."""
    needle += "\x00"  # a hack to force the automaton to go back when matching
    # please god, don't smite me down for this

    automaton = [0] * len(needle)

    def step(state: State, char: String) -> State:
        """A single step of the automaton, given a state and a character."""
        # keep returning back until the char matches or we're not at the beginning
        while needle[state] != char and state != 0:
            state = automaton[state]

        # move forward if the character matches
        if needle[state] == char:
            state += 1

        return state

    # build the automaton
    state = 0
    for i in range(2, len(needle)):
        state = step(state, needle[i - 1])
        automaton[i] = state

    # run the search
    occurrences = []
    state = 0
    for i, char in enumerate(haystack):
        state = step(state, char)

        if state == len(needle) - 1:
            # +2 for the needle having the extra hack character and to match the beginning
            occurrences.append(i - len(needle) + 2)

    return occurrences


print(kmp("aaba", "lmaabaabaoahojahoj aaba"))
