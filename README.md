# Human Typing Simulator

A realistic human typing simulator that mimics natural typing patterns, including errors and speed variations.

![alt text](image.png)

## Features
- Realistic typing simulation with human-like patterns
- Configurable typing speed (20-1000+ WPM)
- Error simulation with adjustable rates
- Dark mode interface
- Speed presets from "Very Slow" to "Ultra Fast"
- Customizable error types and correction behavior

## Installation

### Option 1: Quick Install (macOS)

1. Clone this repository or download it as a ZIP file
2. Open Terminal and navigate to the project directory
3. Make the install script executable:
   ```
   chmod +x install_humantyping.sh
   ```
4. Run the install script:
   ```
   ./install_humantyping.sh
   ```
5. The application will be installed in your Applications folder

### Option 2: Manual Install

1. Make sure you have Python 3.6+ installed
2. Clone this repository:
   ```
   git clone https://github.com/yourusername/human-typing-simulator.git
   cd human-typing-simulator
   ```
3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
4. Run the application:
   ```
   python main.py
   ```

## Usage

1. Launch the application
2. Paste your text into the text area
3. Choose a typing speed preset (Slow, Medium, Fast, Ultra Fast) or set a custom speed
4. Configure error rate and simulation options
5. Click "Start" or press Ctrl+S
6. Place your cursor where you want the text to be typed
7. After the countdown, the simulator will begin typing with human-like patterns
8. Press Esc at any time to stop the simulation

## Configuration Options

- **Typing Speed**: Adjust WPM (words per minute) from 20 to 1000+
- **Error Simulation**: Toggle on/off and set error rate (percentage)
- **Keep Errors**: Choose whether to correct errors or leave them in
- **Font Size**: Adjust for better visibility

## Development

To modify or extend the application:

```
# Clone the repo
git clone https://github.com/yourusername/human-typing-simulator.git

# Install in development mode
pip install -e .
```

## License

MIT License - See LICENSE file for details (todo)

## Acknowledgments

- Built with PyAutoGUI for keyboard simulation
- Uses Tkinter for the user interface

