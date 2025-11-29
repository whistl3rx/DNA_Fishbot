import mss
import numpy as np
from src.config import REGION_RATIOS


class ScreenCapture:
    """Handles screen region calculation and grabbing frames via mss."""

    def __init__(self):
        self.sct = mss.mss()

    def get_screen_region(self):
        monitor = self.sct.monitors[1]
        screen_width = monitor["width"]
        screen_height = monitor["height"]

        region = {
            "left": int(screen_width * REGION_RATIOS["left_ratio"]),
            "top": int(screen_height * REGION_RATIOS["top_ratio"]),
            "width": int(screen_width * REGION_RATIOS["width_ratio"]),
            "height": int(screen_height * REGION_RATIOS["height_ratio"]),
        }

        return region, screen_width, screen_height

    def grab(self, region):
        return np.array(self.sct.grab(region))
