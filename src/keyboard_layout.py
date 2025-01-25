"""Keyboard layout and related functions."""

QWERTY_LAYOUT = {
    "q": ["w", "a"],
    "w": ["q", "e", "s"],
    "e": ["w", "r", "d"],
    "r": ["e", "t", "f"],
    "t": ["r", "y", "g"],
    "y": ["t", "u", "h"],
    "u": ["y", "i", "j"],
    "i": ["u", "o", "k"],
    "o": ["i", "p", "l"],
    "p": ["o", "[", ";"],
    "a": ["q", "w", "s", "z"],
    "s": ["w", "a", "d", "x"],
    "d": ["e", "s", "f", "c"],
    "f": ["r", "d", "g", "v"],
    "g": ["t", "f", "h", "b"],
    "h": ["y", "g", "j", "n"],
    "j": ["u", "h", "k", "m"],
    "k": ["i", "j", "l", ","],
    "l": ["o", "k", ";", "."],
    "z": ["a", "s", "x"],
    "x": ["s", "z", "c"],
    "c": ["d", "x", "v"],
    "v": ["f", "c", "b"],
    "b": ["g", "v", "n"],
    "n": ["h", "b", "m"],
    "m": ["j", "n", ","],
}


def get_adjacent_key(char):
    """Get a random adjacent key for the given character."""
    import random

    char = char.lower()
    if char in QWERTY_LAYOUT:
        return random.choice(QWERTY_LAYOUT[char])
    return char
