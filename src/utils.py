"""Utility functions for typing simulation."""

import numpy as np


def generate_delay(cpm_mean, cpm_std, min_cpm):
    """Generate typing delay in milliseconds."""
    cpm = max(np.random.normal(cpm_mean, cpm_std), min_cpm)
    return 60000 / cpm


def debug_print(config, message):
    """Print debug messages if debug mode is enabled."""
    if config["DEBUG"]:
        print(message)


def validate_config(config):
    """Validate and set default configuration values."""
    defaults = {
        "STARTUP_DELAY": 5,
        "DEBUG": False,
        "WPM_MEAN": 60,
        "WPM_STD": 10,
        "MIN_CPM": 100,
        "ERROR_RATE": 0.05,
        "ERROR_TYPES": ["adjacent", "transpose", "omit"],
        "CORRECTION_DELAY_MIN": 200,
        "CORRECTION_DELAY_MAX": 1000,
        "BACKSPACE_DELAY": 100,
    }

    return {**defaults, **config}
