"""Core typing simulation engine."""

import random
import time
import pyautogui
from src.utils import generate_delay, debug_print
from src.keyboard_layout import get_adjacent_key


class TypingSimulator:
    def __init__(self, config):
        self.config = config
        self.cpm_mean = config["WPM_MEAN"] * 5
        self.cpm_std = config["WPM_STD"] * 5
        pyautogui.FAILSAFE = True
        self.startup_delay = config.get("STARTUP_DELAY", 5)
        self.target_x = None
        self.target_y = None
        self._original_failsafe = pyautogui.FAILSAFE
        self._original_pause = pyautogui.PAUSE

    def _setup_pyautogui(self):
        """Configure PyAutoGUI for background typing."""
        pyautogui.FAILSAFE = False  # Temporarily disable failsafe
        pyautogui.PAUSE = 0  # Remove default pauses

    def _restore_pyautogui(self):
        """Restore original PyAutoGUI settings."""
        pyautogui.FAILSAFE = self._original_failsafe
        pyautogui.PAUSE = self._original_pause

    def select_target_window(self):
        """Let user select where to type."""
        print("\nWindow selection instructions:")
        print("1. Move your mouse to where you want to type")
        print("2. Press ENTER when ready")

    def type_text(self, text):
        """Main typing method with window targeting."""
        if not self.select_target_window():
            return

        print(f"\nStarting in {self.startup_delay} seconds...")
        print("You can now use your mouse freely!")
        print("To stop typing, press Ctrl+C")
        time.sleep(self.startup_delay)

        try:
            self._setup_pyautogui()

            # Store current mouse position
            for i, char in enumerate(text):
                current_x, current_y = pyautogui.position()

                # Move to target, click, type, and return
                pyautogui.moveTo(self.target_x, self.target_y, duration=0, _pause=False)
                pyautogui.click(_pause=False)
                self._type_char(i, char, text)
                pyautogui.moveTo(current_x, current_y, duration=0, _pause=False)

        except KeyboardInterrupt:
            print("\nTyping stopped by user")
        except Exception as e:
            print(f"\nError during typing: {str(e)}")
        finally:
            self._restore_pyautogui()

    def _type_char(self, index, char, text):
        """Handle single character typing with error simulation."""
        delay = generate_delay(self.cpm_mean, self.cpm_std, self.config["MIN_CPM"])
        debug_print(self.config, f"Typing '{char}' with delay {delay:.2f}ms")

        time.sleep(delay / 1000)
        char_to_type, made_error = self._handle_errors(char, index, text)

        if char_to_type:
            pyautogui.typewrite(char_to_type, _pause=False)

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
        pyautogui.press("backspace", _pause=False)
        time.sleep(self.config["BACKSPACE_DELAY"] / 1000)
        pyautogui.typewrite(original_char, _pause=False)
