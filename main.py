import time
from src.config import DEFAULT_CONFIG
from src.typing_engine import TypingSimulator
from src.gui import TypingSimulatorGUI


def main():
    app = TypingSimulatorGUI()
    app.run()


if __name__ == "__main__":
    main()
