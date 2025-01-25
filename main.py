import time
from src.config import DEFAULT_CONFIG
from src.typing_engine import TypingSimulator


def main():
    # Custom configuration
    config = DEFAULT_CONFIG.copy()
    config["WPM_MEAN"] = 5000000000000  # Extremely fast typing
    config["MIN_CPM"] = 200000000000  # Minimum speed floor
    config["WPM_STD"] = 200  # More variation in speed
    config["ERROR_RATE"] = 0.08  # Base error rate
    config["DEBUG"] = True

    # Initialize simulator
    simulator = TypingSimulator(config)

    # Wait before starting
    time.sleep(config["START_DELAY"])

    # Run simulation
    text = """Programming: Proficiency in Python, including working with WebSockets, JSON-RPC, and relevant libraries.

Signal Processing: Basic understanding of signal processing concepts for analyzing EEG data.

Brain-Computer Interfaces: Familiarity with BCI principles, EEG technology, and the Emotiv platform.

Data Analysis: Ability to interpret basic data and make adjustments based on observed performance.

Technical Writing: Ability to document the project and explain it clearly."""
    simulator.type_text(list(text))


if __name__ == "__main__":
    main()
