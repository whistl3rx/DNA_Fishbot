# Duet Night Abyss — Automatic Fishing Bot

This Python script automates the fishing minigame in the Duet Night Abyss game. The bot detects the fish icon and the capsule on screen and automatically presses the Space key when the fish is inside the capsule.

## 🎯 Features

- Automatic fish icon detection using template matching (multiple templates supported for robustness)
- Capsule position tracking for accurate timing
- Intelligent Space key control (press/release automatically based on fish position)
- Debug mode with visual overlays to help diagnose detections
- Designed for high FPS (target ~30 FPS)
- Safe exit via the ESC key

## 📦 Installation

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Prepare template images:

- Create the `templates/` folder if it does not exist.
- Fish icon: save the sprite sheet as `templates/fish.png`.
  - The script can automatically split a 4x8 sprite sheet into 32 frames.
  - If you don't have a sprite sheet, you can provide individual template images (e.g. `fish_1.png`, `fish_2.png`).
- Capsule: save the capsule image as `templates/capsule.png`.

## 🖼️ Template Images

### Fish icon (`templates/fish.png`) — Sprite Sheet (recommended)

The exported fish icon from the game is commonly a 4x8 sprite sheet (32 frames).

1. Export from the game files (see `EXTRACT_FROM_GAME_FILES.md`):
   - Use UABE or AssetStudio to export the fish sprite sheet as PNG.
   - Save it as `templates/fish.png`.

2. The script will:
   - Detect a 4x8 layout and split it into 32 frames.
   - Use the frames as templates for matching.

Alternatives: provide single-frame templates like `fish.png` or multiple templates `fish_1.png`, `fish_2.png`, etc.

### Capsule (`templates/capsule.png`)

1. Export the capsule image from game files or capture it from a screenshot.
2. Save it as `templates/capsule.png`.
3. You can use the helper `extract_templates.py` to crop templates interactively.

## ⚙️ Configuration

You can modify settings in `main.py` or the configuration section at the top of the script. Example configuration used by the project:

```python
# Screen region coordinates
SCREEN_REGION = {
    "top": 640,
    "left": 3220,
    "width": 110,
    "height": 820
}

# Template matching thresholds (0.0 - 1.0)
FISH_THRESHOLD = 0.7
CAPSULE_THRESHOLD = 0.7

# FPS target
TARGET_FPS = 30

# Debug mode
DEBUG_MODE = True
```

### Setting the screen region

1. Start the game and open the fishing minigame.
2. Determine coordinates for the region where the fish and capsule appear (use a coordinate tool or screenshot helper).
3. Set `SCREEN_REGION` accordingly.

Tip: The smaller the region, the faster the processing.

## 🚀 Usage

1. Start the game and go to the fishing minigame.
2. Run the script:

```bash
python main.py
```

3. You have ~3 seconds to position things.
4. The bot starts automatically.
5. Press ESC to exit at any time.

## 🐛 Troubleshooting

### Bot doesn't find the fish icon

- Verify that `templates/fish.png` exists and contains the correct images.
- Lower `FISH_THRESHOLD` (for example, to 0.6).
- Verify `SCREEN_REGION` coordinates are correct.
- Use `DEBUG_MODE` to visualize detections and see what the bot sees.

### Bot doesn't find the capsule

- Verify that `templates/capsule.png` is correct.
- Lower `CAPSULE_THRESHOLD` if needed.
- Check the `SCREEN_REGION` configuration.

### Bot is too slow

- Reduce the size of `SCREEN_REGION`.
- Increase `TARGET_FPS` (but be cautious; too high may cause instability).
- Use smaller template images to speed up matching.

### Space key doesn't work

- Ensure the game window is active and accepts keyboard input.
- Test pressing Space manually while the game is focused.
- Ensure no other program is intercepting or blocking keyboard events.

## 📝 Notes

- The bot only monitors the specified screen region.
- Template matching runs in grayscale for speed.
- The bot releases Space when no fish or capsule is detected.
- PyAutoGUI failsafe is active; move your mouse to a screen corner to abort.

## ⚠️ Disclaimer

This script is intended for educational purposes only. Use it at your own risk — game developers may detect automated players and apply sanctions.

## 📄 License

This project is provided for educational use.


