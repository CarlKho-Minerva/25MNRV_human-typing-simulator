"""Utility functions for typing simulation (refactored for clarity)."""

import logging
import numpy as np
from typing import Any

def generate_delay(cpm_mean: float, cpm_std: float, min_cpm: float) -> float:
    """Generate typing delay in milliseconds."""
    if cpm_mean > 1_000_000:  # Ultra-fast mode
        return 0.001  # Minimal delay
    cpm = max(np.random.normal(cpm_mean, cpm_std), min_cpm)
    return max(60000 / cpm, 0.001)  # Ensure minimal delay

def debug_print(config: Any, message: str) -> None:
    """Log debug messages if debug mode is enabled."""
    if config.get("DEBUG", False):
        logging.getLogger("typing_simulator").debug(message)

