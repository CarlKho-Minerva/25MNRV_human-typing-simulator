#!/bin/zsh

set -e

APP_NAME="HumanTypingSimulator"
ENTRY="main.py"
ICON="image.png"

echo "Checking for Python..."
PYTHON=$(which python || which python3)
if [ -z "$PYTHON" ]; then
  echo "Python is required. Please install it from https://www.python.org/downloads/"
  exit 1
fi
echo "Using Python: $PYTHON"

# Check if we're running inside a virtualenv
if [[ -n "$VIRTUAL_ENV" ]]; then
  echo "Detected virtual environment: $VIRTUAL_ENV"
  PIP_CMD="$PYTHON -m pip install"
else
  echo "No virtual environment detected, using --user flag"
  PIP_CMD="$PYTHON -m pip install --user"
fi

echo "Installing dependencies..."
eval "$PIP_CMD -r requirements.txt"

echo "Checking for PyInstaller..."
$PYTHON -m pip show pyinstaller >/dev/null 2>&1 || eval "$PIP_CMD pyinstaller"

echo "Building the .app bundle..."
$PYTHON -m PyInstaller --windowed --onefile --name "$APP_NAME" "$ENTRY"

# Look for the app in both potential locations
if [ -d "dist/$APP_NAME.app" ]; then
  APP_PATH="dist/$APP_NAME.app"
elif [ -f "dist/$APP_NAME" ]; then
  echo "PyInstaller created an executable but not an .app bundle."
  echo "Creating app bundle structure manually..."
  
  # Create a basic app structure around the executable
  mkdir -p "dist/$APP_NAME.app/Contents/MacOS"
  cp "dist/$APP_NAME" "dist/$APP_NAME.app/Contents/MacOS/"
  chmod +x "dist/$APP_NAME.app/Contents/MacOS/$APP_NAME"
  
  # Create Info.plist file
  mkdir -p "dist/$APP_NAME.app/Contents"
  cat > "dist/$APP_NAME.app/Contents/Info.plist" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>CFBundleDisplayName</key>
	<string>$APP_NAME</string>
	<key>CFBundleExecutable</key>
	<string>$APP_NAME</string>
	<key>CFBundleIconFile</key>
	<string>AppIcon</string>
	<key>CFBundleIdentifier</key>
	<string>com.humantyping.$APP_NAME</string>
	<key>CFBundleInfoDictionaryVersion</key>
	<string>6.0</string>
	<key>CFBundleName</key>
	<string>$APP_NAME</string>
	<key>CFBundlePackageType</key>
	<string>APPL</string>
	<key>CFBundleShortVersionString</key>
	<string>1.0.0</string>
	<key>NSHighResolutionCapable</key>
	<true/>
</dict>
</plist>
EOF

  # Copy icon if it exists
  if [ -f "$ICON" ]; then
    mkdir -p "dist/$APP_NAME.app/Contents/Resources"
    cp "$ICON" "dist/$APP_NAME.app/Contents/Resources/AppIcon.icns"
  fi
  
  APP_PATH="dist/$APP_NAME.app"
else
  echo "Build failed. No app or executable found in dist/ directory."
  exit 1
fi

echo "Copying app to /Applications..."
# Use sudo since /Applications may require admin privileges
cp -R "$APP_PATH" /Applications/

echo "Cleaning up build files..."
rm -rf build "$APP_NAME.spec"

echo "Done! You can now find '$APP_NAME' in Spotlight or your Applications folder."