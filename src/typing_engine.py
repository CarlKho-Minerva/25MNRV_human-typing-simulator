"""Core typing simulation engine."""

import random
import time
import pyautogui
from .utils import generate_delay, debug_print
from .keyboard_layout import get_adjacent_key


class TypingSimulator:
    def __init__(self, config):
        self.config = config
        self.cpm_mean = config["WPM_MEAN"] * 5
        self.cpm_std = config["WPM_STD"] * 5

    def type_text(self, text):
        """Main typing method."""
        for i, char in enumerate(text):
            self._type_char(i, char, text)

    def _type_char(self, index, char, text):
        """Handle single character typing with error simulation."""
        delay = generate_delay(self.cpm_mean, self.cpm_std, self.config["MIN_CPM"])
        debug_print(self.config, f"Typing '{char}' with delay {delay:.2f}ms")

        time.sleep(delay / 1000)
        char_to_type, made_error = self._handle_errors(char, index, text)

        if char_to_type:
            pyautogui.typewrite(char_to_type)

        if made_error:
            self._handle_correction(char, index, text)

    def _handle_errors(self, char, index, text):
        """Simulate typing errors."""
        if random.random() < self.config["ERROR_RATE"]:
            error_type = random.choice(self.config["ERROR_TYPES"])
            return self._apply_error(error_type, char, index, text), True
        return char, False

    def _apply_error(self, error_type, char, index, text):
        """Apply specific error type."""
        if error_type == "adjacent":
            return get_adjacent_key(char)
        elif error_type == "transpose" and index + 1 < len(text):
            return text[index + 1]
        elif error_type == "omit":
            return ""
        return char

    def _handle_correction(self, original_char, index, text):
        """Handle error correction."""
        time.sleep(
            random.uniform(
                self.config["CORRECTION_DELAY_MIN"] / 1000,
                self.config["CORRECTION_DELAY_MAX"] / 1000,
            )
        )
        pyautogui.press("backspace")
        time.sleep(self.config["BACKSPACE_DELAY"] / 1000)
        pyautogui.typewrite(original_char)
