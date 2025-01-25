"""Configuration settings for the typing simulator."""

DEFAULT_CONFIG = {
    # Typing speed settings
    "WPM_MEAN": 100,
    "WPM_STD": 15,
    "MIN_CPM": 50,

    # Error simulation
    "ERROR_RATE": 0.02,
    "ERROR_TYPES": ["adjacent", "transpose", "omit"],

    # Timing settings (milliseconds)
    "CORRECTION_DELAY_MIN": 200,
    "CORRECTION_DELAY_MAX": 400,
    "BACKSPACE_DELAY": 100,

    # Initial delay before typing starts
    "START_DELAY": 3,

    # Debug mode
    "DEBUG": False,
}
