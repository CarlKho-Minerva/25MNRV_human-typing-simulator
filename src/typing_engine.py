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
        self.base_error_rate = config["ERROR_RATE"]
        self.current_speed = 0
        self.stop_typing = False  # Add stop flag
        pyautogui.MINIMUM_DURATION = 0  # Remove artificial delay
        pyautogui.PAUSE = 0  # Remove pause between actions

    def type_text(self, text):
        """Main typing method with human-like pauses."""
        self.stop_typing = False  # Reset stop flag
        prev_char = ''
        for i, char in enumerate(text):
            if self.stop_typing:
                break
            # Thinking moment: pause after sentence-ending punctuation or newlines
            if prev_char in '.!?\n':
                thinking_delay = random.uniform(0.6, 1.5)  # 0.6-1.5s pause
                time.sleep(thinking_delay)
            # Occasional mid-sentence hesitation (after comma or long word)
            elif prev_char == ',' or (i > 4 and text[i-5:i].isalpha() and len(text[i-5:i]) > 4 and random.random() < 0.08):
                hesitation_delay = random.uniform(0.2, 0.5)
                time.sleep(hesitation_delay)
            # Hand movement delay: switching between letter and non-letter
            elif prev_char and ((prev_char.isalpha() and not char.isalpha()) or (not prev_char.isalpha() and char.isalpha())):
                hand_move_delay = random.uniform(0.08, 0.18)
                time.sleep(hand_move_delay)
            self._type_char(i, char, text)
            prev_char = char

    def _calculate_dynamic_error_rate(self, delay):
        """Calculate error rate based on current typing speed."""
        speed_factor = (
            60000 / delay
        ) / self.cpm_mean  # Ratio of current speed to mean speed
        return self.base_error_rate * (
            1 + (speed_factor - 1) * 0.5
        )  # Increase error rate with speed

    def _type_char(self, index, char, text):
        """Handle single character typing with error simulation and pauses."""
        delay = generate_delay(self.cpm_mean, self.cpm_std, self.config["MIN_CPM"])
        self.current_speed = 60000 / delay
        dynamic_error_rate = self._calculate_dynamic_error_rate(delay)
        debug_print(self.config, f"Typing '{char}' with delay {delay:.2f}ms")
        time.sleep(max(delay / 1000, 0.03))  # Always sleep for at least 30ms
        if self.config.get("ENABLE_ERRORS", True) and random.random() < dynamic_error_rate:
            error_type = random.choice(self.config["ERROR_TYPES"])
            wrong_char = self._apply_error(error_type, char, index, text)
            if wrong_char:
                pyautogui.write(wrong_char, interval=0)
                if not self.config.get("KEEP_ERRORS", False):
                    # Hesitation before correction
                    time.sleep(random.uniform(0.12, 0.35))
                    pyautogui.press("backspace")
                    time.sleep(self.config.get("BACKSPACE_DELAY", 100) / 1000)
                    pyautogui.write(char, interval=0)
                return
        pyautogui.write(char, interval=0)

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
        # Remove sleep for instant correction
        # time.sleep(
        #     random.uniform(
        #         self.config["CORRECTION_DELAY_MIN"] / 1000,
        #         self.config["CORRECTION_DELAY_MAX"] / 1000,
        #     )
        # )
        pyautogui.press("backspace")
        # time.sleep(self.config["BACKSPACE_DELAY"] / 1000)
        pyautogui.typewrite(original_char)
