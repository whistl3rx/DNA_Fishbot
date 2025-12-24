from enum import Enum

# Screen / reference configuration
REFERENCE_WIDTH = 3840
REFERENCE_HEIGHT = 2160
REFERENCE_REGION = {
    "left": 3210,
    "top": 1620,
    "width": 350,
    "height": 350,
}

REGION_RATIOS = {
    "left_ratio": REFERENCE_REGION["left"] / REFERENCE_WIDTH,
    "top_ratio": REFERENCE_REGION["top"] / REFERENCE_HEIGHT,
    "width_ratio": REFERENCE_REGION["width"] / REFERENCE_WIDTH,
    "height_ratio": REFERENCE_REGION["height"] / REFERENCE_HEIGHT,
}

BITING_TIMEOUT = 4.0 # seconds
FISHING_TIME_MIN = 5.0 # seconds
FISH_CAUGHT_DELAY = 4.5 # seconds
DIALOG_CONFIRM_DELAY = 1.5 # seconds
BIGGER_FISH_DELAY = 2.5 # seconds

# Detection thresholds
CAST_CATCH_THRESHOLD = 0.7
BITE_THRESHOLD = 0.7

# FPS / timing
TARGET_FPS = 60
FRAME_DELAY = 0.1

# Debug / window
DEBUG_MODE = False
DEBUG_SAVE_IMAGES = False
DEBUG_WINDOW_POSITION = None
EXIT_KEY = 'esc'


class FishingState(Enum):
    IDLE = 0,
    CASTING = 1,
    WAITING_FOR_BITE = 2,
    CATCHED = 3

class InputFix(Enum):
    NOT = 0
    FIXING = 1
    DONE = 2
