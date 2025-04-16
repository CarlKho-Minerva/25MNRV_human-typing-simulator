#!/bin/zsh

set -e

APP_NAME="HumanTypingSimulator"
ENTRY="main.py"
ICON="image.png"

echo "Checking for Python 3..."
if ! command -v python3 >/dev/null 2>&1; then
  echo "Python 3 is required. Please install it from https://www.python.org/downloads/"
  exit 1
fi

echo "Installing dependencies..."
pip3 install --user -r requirements.txt

echo "Checking for PyInstaller..."
pip3 show pyinstaller >/dev/null 2>&1 || pip3 install --user pyinstaller

echo "Building the .app bundle..."
pyinstaller --windowed --onefile --name "$APP_NAME" --icon "$ICON" "$ENTRY"

APP_PATH="dist/$APP_NAME.app"

if [ ! -d "$APP_PATH" ]; then
  echo "Build failed. $APP_PATH not found."
  exit 1
fi

echo "Copying app to /Applications..."
cp -R "$APP_PATH" /Applications/

echo "Cleaning up build files..."
rm -rf build "$APP_NAME.spec"

echo "Done! You can now find '$APP_NAME' in Spotlight or your Applications folder."