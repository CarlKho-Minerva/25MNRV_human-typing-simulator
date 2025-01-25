"""Keyboard layout and related functions."""

QWERTY_LAYOUT = {
    "q": ["w", "a"],
    "w": ["q", "e", "a", "s"],
    # ...existing keyboard layout...
}

def get_adjacent_key(char):
    """Get a random adjacent key for the given character."""
    import random

    char = char.lower()
    if char in QWERTY_LAYOUT:
        return random.choice(QWERTY_LAYOUT[char])
    return char
