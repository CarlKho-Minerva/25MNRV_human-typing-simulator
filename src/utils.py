"""Utility functions for typing simulation."""

import numpy as np

def generate_delay(cpm_mean, cpm_std, min_cpm):
    """Generate typing delay in milliseconds."""
    if cpm_mean > 1000000:  # Ultra-fast mode
        return 0.001  # Minimal delay
    cpm = max(np.random.normal(cpm_mean, cpm_std), min_cpm)
    return max(60000 / cpm, 0.001)  # Ensure minimal delay

def debug_print(config, message):
    """Print debug messages if debug mode is enabled."""
    if config["DEBUG"]:
        print(message)

