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
