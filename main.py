import time
from src.config import DEFAULT_CONFIG
from src.typing_engine import TypingSimulator


def main():
    # Custom configuration
    config = DEFAULT_CONFIG.copy()
    config["WPM_MEAN"] = 500  # Faster typing
    config["ERROR_RATE"] = 0.1  # Fewer errors
    config["DEBUG"] = True

    # Initialize simulator
    simulator = TypingSimulator(config)

    # Wait before starting
    time.sleep(config["START_DELAY"])

    # Run simulation
    text = "Hello, World! This is a test of the typing function."
    simulator.type_text(list(text))


if __name__ == "__main__":
    main()
