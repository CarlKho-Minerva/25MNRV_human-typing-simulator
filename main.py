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
    text = """"""
    simulator.type_text(list(text))


if __name__ == "__main__":
    main()
