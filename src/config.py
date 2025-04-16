"""Configuration settings for the typing simulator."""

SPEED_PRESETS = {
    "Slow": {"wpm": 30, "desc": "30 WPM - Beginner typing speed"},
    "Medium": {"wpm": 60, "desc": "60 WPM - Average typing speed"},
    "Fast": {"wpm": 100, "desc": "100 WPM - Professional typing speed"},
    "Ultra Fast": {"wpm": 150, "desc": "150 WPM - Expert typing speed"},
    "Custom": {"wpm": 80, "desc": "Use slider to set custom speed"}
}

DEFAULT_CONFIG = {
    # Typing speed settings
    "WPM_MEAN": 100,
    "WPM_STD": 15,
    "MIN_CPM": 50,
    "SPEED_PRESET": "Medium",
    # Error simulation
    "ERROR_RATE": 0.02,
    "ERROR_TYPES": ["adjacent", "transpose", "omit"],
    "ENABLE_ERRORS": True,  # New setting for error toggle
    # Timing settings (milliseconds)
    "CORRECTION_DELAY_MIN": 200,
    "CORRECTION_DELAY_MAX": 400,
    "BACKSPACE_DELAY": 100,
    # Initial delay before typing starts
    "START_DELAY": 3,
    # Debug mode
    "DEBUG": False,
}
