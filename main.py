import time
from src.config import DEFAULT_CONFIG
from src.typing_engine import TypingSimulator


def main():
    # Custom configuration
    config = DEFAULT_CONFIG.copy()
    config["WPM_MEAN"] = 5000000000  # Faster typing
    config["MIN_CPM"] = 2000000000  # Faster typing
    config["WPM_STD"] = 100  # Variation
    config["ERROR_RATE"] = 0.1  # Fewer errors
    config["DEBUG"] = True

    # Initialize simulator
    simulator = TypingSimulator(config)

    # Wait before starting
    time.sleep(config["START_DELAY"])

    # Run simulation
    text = """
Topic: Brain-Computer Interfaces (BCIs), specifically using EEG to control a computer cursor.
Specific Focus/Problem: The project addresses the problem of computer accessibility for individuals with paralysis who cannot use traditional input devices. It focuses on developing a simple BCI application that allows users to control a cursor using their thoughts.
Implicit Question: Can a basic, functional EEG-based cursor control application be built using readily available consumer-grade hardware and software tools?s
"""
    simulator.type_text(list(text))


if __name__ == "__main__":
    main()
