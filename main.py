import time
from src.typing_engine import TypingSimulator
from src.utils import validate_config


def main():
    config = validate_config({"DEBUG": True})
    simulator = TypingSimulator(config)
    simulator.type_text("This is a test of the typing simulator.")


if __name__ == "__main__":
    main()