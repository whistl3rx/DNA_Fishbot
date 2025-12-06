from enum import Enum

# Screen / reference configuration
REFERENCE_WIDTH = 3840
REFERENCE_HEIGHT = 2160
REFERENCE_REGION = {
    "left": 3110,
    "top": 630,
    "width": 295,
    "height": 1210,
}

REGION_RATIOS = {
    "left_ratio": REFERENCE_REGION["left"] / REFERENCE_WIDTH,
    "top_ratio": REFERENCE_REGION["top"] / REFERENCE_HEIGHT,
    "width_ratio": REFERENCE_REGION["width"] / REFERENCE_WIDTH,
    "height_ratio": REFERENCE_REGION["height"] / REFERENCE_HEIGHT,
}

BITING_TIMEOUT = 2.0 # seconds
FISHING_TIME_MIN = 5.0 # seconds
FISH_CAUGHT_DELAY = 4.0 # seconds
BIGGER_FISH_DELAY = 2.5 # seconds

# Detection thresholds
CAST_THRESHOLD = 0.7
BITE_THRESHOLD = 0.7
CATCH_THRESHOLD = 0.7
FISH_THRESHOLD = 0.6
CAPSULE_THRESHOLD = 0.5

# FPS / timing
TARGET_FPS = 60
FRAME_DELAY = 1.0 / TARGET_FPS

# Debug / window
DEBUG_MODE = True
DEBUG_SAVE_IMAGES = False
DEBUG_WINDOW_POSITION = None
EXIT_KEY = 'esc'


class InputFix(Enum):
    NOT = 0
    FIXING = 1
    DONE = 2
