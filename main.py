import pyautogui
import random
import time
import numpy as np


def type_humanly(text, wpm_mean=60, wpm_std=15, error_rate=0.02):
    """
    Simulates human-like typing of the given text.

    Args:
        text: The text to type.
        wpm_mean: The average typing speed in words per minute.
        wpm_std: The standard deviation of the typing speed (in WPM).
        error_rate: The probability of making a typing error (0.0 to 1.0).
    """
    cpm_mean = wpm_mean * 5p # Convert WPM to CPM (average 5 characters per word)
    cpm_std = wpm_std * 5

    for i, char in enumerate(text):
        # 1. Generate Delay (Normal Distribution)
        delay = generate_delay(cpm_mean, cpm_std)
        time.sleep(delay / 1000)  # Convert milliseconds to seconds

        # 2. Simulate Error (with a certain probability)
        if random.random() < error_rate:
            error_type = random.choice(["adjacent", "transpose", "omit"])
            if error_type == "adjacent":
                # type a random char that is close
                char = type_adjacent_error(char)
            elif error_type == "transpose":
                # swap with next char
                if i + 1 < len(text):
                    char, text[i + 1] = text[i + 1], char

            elif error_type == "omit":
                char = ""  # skip

        # 3. Type the Character (or error)
        if char != "":
            pyautogui.typewrite(char)

        # 4. Correct Error (if needed) - This is a simplified correction
        #    In a more advanced version, you could simulate backspace patterns
        #    based on the type of error.


def generate_delay(cpm_mean, cpm_std):
    """Generates a random delay in milliseconds based on a normal distribution."""
    cpm = np.random.normal(cpm_mean, cpm_std)
    if cpm < 50:  # Avoid extremely fast or negative delays
        cpm = 50
    delay_ms = 60000 / cpm
    return delay_ms


def type_adjacent_error(char):
    """Simulates an adjacent key error."""
    keyboard_layout = {
        "q": ["w", "a"],
        "w": ["q", "e", "a", "s"],
        "e": ["w", "r", "s", "d"],
        "r": ["e", "t", "d", "f"],
        "t": ["r", "y", "f", "g"],
        "y": ["t", "u", "g", "h"],
        "u": ["y", "i", "h", "j"],
        "i": ["u", "o", "j", "k"],
        "o": ["i", "p", "k", "l"],
        "p": ["o", "l"],
        "a": ["q", "w", "s", "z"],
        "s": ["w", "e", "a", "d", "z", "x"],
        "d": ["e", "r", "s", "f", "x", "c"],
        "f": ["r", "t", "d", "g", "c", "v"],
        "g": ["t", "y", "f", "h", "v", "b"],
        "h": ["y", "u", "g", "j", "b", "n"],
        "j": ["u", "i", "h", "k", "n", "m"],
        "k": ["i", "o", "j", "l", "m"],
        "l": ["o", "p", "k"],
        "z": ["a", "s", "x"],
        "x": ["s", "d", "z", "c"],
        "c": ["d", "f", "x", "v"],
        "v": ["f", "g", "c", "b"],
        "b": ["g", "h", "v", "n"],
        "n": ["h", "j", "b", "m"],
        "m": ["j", "k", "n"],
    }

    char = char.lower()
    if char in keyboard_layout:
        adjacent_keys = keyboard_layout[char]
        typo = random.choice(adjacent_keys)
        return typo
    else:
        return char  # Return the original character if not in the layout

# Example usage (you can paste your text here)
text_to_type = "The"
time.sleep(5)
type_humanly(list(text_to_type), 10000, 0.001, 0.02)

