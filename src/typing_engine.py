"""Core typing simulation engine (refactored for clarity and modularity)."""

import random
import pyautogui
from typing import List, Dict, Any
from .utils import generate_delay, debug_print
from .keyboard_layout import get_adjacent_key

class TypingErrorSimulator:
    """Handles error simulation logic for typing."""
    def __init__(self, config: Dict[str, Any]):
        self.config = config

    def should_make_error(self, delay: float, cpm_mean: float, base_error_rate: float) -> bool:
        speed_factor = (60000 / delay) / cpm_mean
        dynamic_error_rate = base_error_rate * (1 + (speed_factor - 1) * 0.5)
        return self.config.get("ENABLE_ERRORS", True) and random.random() < dynamic_error_rate

    def get_error_char(self, error_type: str, char: str, index: int, text: List[str]) -> str:
        if error_type == "adjacent":
            return get_adjacent_key(char)
        elif error_type == "transpose" and index + 1 < len(text):
            return text[index + 1]
        elif error_type == "omit":
            return ""
        return char

class TypingSimulator:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.cpm_mean = config["WPM_MEAN"] * 5
        self.cpm_std = config["WPM_STD"] * 5
        self.base_error_rate = config["ERROR_RATE"]
        self.current_speed = 0
        self.stop_typing = False
        self.error_sim = TypingErrorSimulator(config)
        pyautogui.MINIMUM_DURATION = 0
        pyautogui.PAUSE = 0

    def type_text(self, text: List[str]) -> None:
        """Main typing method."""
        self.stop_typing = False
        for i, char in enumerate(text):
            if self.stop_typing:
                break
            self._type_char(i, char, text)

    def _type_char(self, index: int, char: str, text: List[str]) -> None:
        delay = generate_delay(self.cpm_mean, self.cpm_std, self.config["MIN_CPM"])
        self.current_speed = 60000 / delay
        debug_print(self.config, f"Typing '{char}' with delay {delay:.2f}ms")

        if self.error_sim.should_make_error(delay, self.cpm_mean, self.base_error_rate):
            error_type = random.choice(self.config["ERROR_TYPES"])
            wrong_char = self.error_sim.get_error_char(error_type, char, index, text)
            if wrong_char:
                pyautogui.write(wrong_char, interval=0)
                if not self.config.get("KEEP_ERRORS", False):
                    pyautogui.press("backspace")
                    pyautogui.write(char, interval=0)
                return
        pyautogui.write(char, interval=0)
