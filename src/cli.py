import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from .gui import TypingSimulatorGUI
from .config import DEFAULT_CONFIG
from .logging_config import setup_logging

def main():
    setup_logging(DEFAULT_CONFIG.get("DEBUG", False))
    app = TypingSimulatorGUI()
    app.run()

if __name__ == "__main__":
    main()
