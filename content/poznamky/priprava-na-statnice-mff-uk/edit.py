from functools import lru_cache


@lru_cache
def edit(a: str, b: str):
    """Dynamické řešení editační vzdálenosti (odstranění, vložení nebo změna znaku)."""

    if len(a) == 0:
        return len(b)

    if len(b) == 0:
        return len(a)

    l_z = edit(a[1:], b[1:])
    if a[0] != b[0]:
        l_z += 1

    l_o = edit(a[1:], b) + 1
    l_v = edit(a, b[1:]) + 1

    return min(l_z, l_o, l_v)


print(edit("ahoja", "ahoooooooj"))
