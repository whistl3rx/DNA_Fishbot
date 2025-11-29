# Duet Night Abyss — Automatic Fishing Bot

This Python project automates the fishing minigame in the Duet Night Abyss game. The bot runs in three clear phases — `waiting`, `biting`, and `reeling` — and controls Space (via a virtual input controller) to catch fish using template matching.

## 🎯 Features

- Phased operation: `waiting`, `biting`, and `reeling` for clearer behaviour and easier debugging
- Prefer single `templates/fish.png` sprite-sheet (fallback to `templates/fishes/*`)
- Unified template matcher: `Detector.find_template()`
- Capsule position tracking
- Intelligent Space key control (press/release via `InputController`)
- Debug mode with live overlays and saved diagnostics in `debug/`
- Inactivity retry during `waiting` (press Space to re-cast after a no-change timeout)
- Safe exit via the ESC key

## 📦 Installation

1. Create and activate your Python environment (recommended):

```powershell
python -m venv venv
.\n+venv\Scripts\Activate.ps1
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## 🖼️ Templates

- `templates/fish.png` — preferred: a 4x8 sprite sheet that the loader will split into 32 frames.
- If you don't have a sprite sheet, place multiple templates under `templates/fishes/` or individual files like `fish_1.png`.
- `templates/capsule.png` — capsule template used for position tracking.

Use `extract_templates.py` if you want to crop or produce templates from screenshots.

## ⚙️ Configuration

Configuration lives in `src/config.py` (or the top of `main.py` for quick edits). Important settings:

```python
# Screen region coordinates (example)
SCREEN_REGION = {
      "top": 640,
      "left": 3220,
      "width": 110,
      "height": 820
}

# Thresholds (0.0 - 1.0)
FISH_THRESHOLD = 0.7
CAPSULE_THRESHOLD = 0.7
CAST_THRESHOLD = 0.6
BITE_THRESHOLD = 0.6
CATCH_THRESHOLD = 0.7

# Timing
TARGET_FPS = 30
FRAME_DELAY = 1 / TARGET_FPS

# Debug
DEBUG_MODE = True
DEBUG_WINDOW_POSITION = (50, 50)

# Exit key
EXIT_KEY = 'esc'
```

Tweak thresholds for your screen and lighting conditions. Consider requiring consecutive-frame confirmation in code if you see noisy detections.

## 🚀 Usage

1. Start the game and go to the fishing minigame.
2. Run the bot:

```bash
python main.py
```

3. You have ~3 seconds to position things before the bot starts.
4. Press ESC to exit.

## 🐛 Debugging & Diagnostics

- Enable `DEBUG_MODE` to see a live overlay window showing detections.
- The `Debugger` saves per-frame diagnostic images to the `debug/` folder when enabled. Files include phase match heatmaps and marked visuals (e.g. `frame_0001_cast_match_result_marked.png`). These are helpful to inspect why `cv2.matchTemplate` returns low confidence despite a visible object.
- If `cast_template` appears visually but confidence is 0, check the saved heatmaps and the marked images to diagnose mismatches (alpha channels, color/grayscale differences, template scale, or threshold issues).

## 🐛 Troubleshooting (common)

- Bot doesn't find fish: ensure `templates/fish.png` or `templates/fishes/` exists; lower `FISH_THRESHOLD`; inspect `debug/` outputs.
- Bot doesn't find capsule: check `templates/capsule.png`; lower `CAPSULE_THRESHOLD`.
- False positives/noise: try increasing thresholds or require N consecutive positive frames.
- Space not working: ensure the game window accepts keyboard input; the bot uses an `InputController` which may use a virtual gamepad — run the script as an administrator if privileged input is required.

## 📝 Notes

- The bot monitors only the configured `SCREEN_REGION` for performance.
- Template matching is performed in grayscale for speed; detection code handles color/BGRA templates when needed.
- The bot now prefers a single fish sprite-sheet but supports multiple templates for robustness.

## ⚠️ Disclaimer

This script is intended for educational purposes only. Use it at your own risk — game developers may detect automated players and apply sanctions.

## 📄 License

This project is provided for educational use.


