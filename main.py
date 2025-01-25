import pyautogui
import random
import time
import numpy as np

# Configuration variables
CONFIG = {
    # Typing speed settings
    'WPM_MEAN': 100,          # Average typing speed (words per minute)
    'WPM_STD': 15,           # Standard deviation of typing speed
    'MIN_CPM': 50,           # Minimum characters per minute

    # Error simulation
    'ERROR_RATE': 0.02,      # Probability of making a typing error
    'ERROR_TYPES': ["adjacent", "transpose", "omit"],

    # Timing settings (milliseconds)
    'CORRECTION_DELAY_MIN': 200,  # Minimum delay before error correction
    'CORRECTION_DELAY_MAX': 400,  # Maximum delay before error correction
    'BACKSPACE_DELAY': 100,      # Delay between backspace presses

    # Initial delay before typing starts
    'START_DELAY': 3,        # Seconds to wait before starting

    # Debug mode (prints timing info)
    'DEBUG': True
}

def type_humanly(text, config=CONFIG):
    """
    Simulates human-like typing of the given text using configuration parameters.
    """
    cpm_mean = config['WPM_MEAN'] * 5
    cpm_std = config['WPM_STD'] * 5

    for i, char in enumerate(text):
        # 1. Generate Delay (Normal Distribution)
        delay = generate_delay(cpm_mean, cpm_std, config['MIN_CPM'])
        if config['DEBUG']:
            print(f"Typing '{char}' with delay {delay:.2f}ms")
        time.sleep(delay / 1000)

        # Initialize error handling variables
        made_error = False
        error_type = None
        original_char = char

        # 2. Simulate Error (with a certain probability)
        if random.random() < config['ERROR_RATE']:
            made_error = True
            error_type = random.choice(config['ERROR_TYPES'])
            if error_type == "adjacent":
                char = type_adjacent_error(char)
            elif error_type == "transpose":
                if i + 1 < len(text):
                    char, text[i + 1] = text[i + 1], char
            elif error_type == "omit":
                char = ""

        # 3. Type the Character (or error)
        if char != "":
            pyautogui.typewrite(char)

        # 4. Correct Error (if needed)
        if made_error and error_type:
            time.sleep(random.uniform(config['CORRECTION_DELAY_MIN'] / 1000, config['CORRECTION_DELAY_MAX'] / 1000))

            if error_type == "adjacent":
                pyautogui.press('backspace')
                time.sleep(generate_delay(cpm_mean, cpm_std, config['MIN_CPM']) / 1000)
                pyautogui.typewrite(original_char)
            elif error_type == "transpose":
                pyautogui.press('backspace')
                time.sleep(config['BACKSPACE_DELAY'] / 1000)
                pyautogui.press('backspace')
                time.sleep(generate_delay(cpm_mean, cpm_std, config['MIN_CPM']) / 1000)
                pyautogui.typewrite(original_char)
                if i + 1 < len(text):
                    time.sleep(generate_delay(cpm_mean, cpm_std, config['MIN_CPM']) / 1000)
                    pyautogui.typewrite(text[i + 1])
            elif error_type == "omit":
                time.sleep(generate_delay(cpm_mean, cpm_std, config['MIN_CPM']) / 1000)
                pyautogui.typewrite(original_char)


def generate_delay(cpm_mean, cpm_std, min_cpm):
    """Generates a random delay in milliseconds based on a normal distribution."""
    cpm = max(np.random.normal(cpm_mean, cpm_std), min_cpm)
    return 60000 / cpm


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

# Example usage with custom configuration
if __name__ == "__main__":
    # You can override any config values here
    custom_config = CONFIG.copy()
    custom_config['WPM_MEAN'] = 500  # Faster typing
    custom_config['ERROR_RATE'] = 0.11  # Fewer errors

    text_to_type = "Hello, World! This is a test of the typing function."
    time.sleep(custom_config['START_DELAY'])
    type_humanly(list(text_to_type), custom_config)

