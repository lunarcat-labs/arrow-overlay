# arrow-overlay
A simple Python tool for screen recordings and tutorials that displays temporary orange arrows pointing to your mouse location.

## Features

- Press **Shift + Arrow Key** to show large orange arrows
- Arrow points in the direction of the arrow you key in
- Arrows point exactly where your mouse is located
- Automatically disappear after 2 seconds
- Click-through - doesn't interfere with mouse interactions
- Simple control window with easy exit

## Download

### Option 1: Download Executable
[Download Latest Release](https://github.com/lunarcat-labs/arrow-overlay/releases/latest)

### Option 2: Run from Source
```bash
# Install dependencies
pip install keyboard
pip install Pillow

Explanation:
keyboard - for the keyboard hotkey detection (import keyboard)
Pillow - for the image manipulation (from PIL import Image, ImageTk, ImageDraw)

The other imports are built into Python:
tkinter - GUI toolkit (comes with Python)
threading - built-in
time - built-in
sys - built-in
os - built-in

# Run the application
python arrow_overlay.py

## Privacy Note
This tool only listens for specific hotkeys (Shift+Arrow) and does NOT:
- Record any keyboard input
- Store or transmit any data
- Access files or network
- The arrows are purely visual overlays.
