import cv2
import numpy as np


class Detector:
    """Contains template matching utilities for fish and capsule detection."""

    @staticmethod
    def find_template(screenshot, template, threshold):
        """Generic template matcher.

        Accepts either a grayscale screenshot (`screenshot` 2D) or a color/BGRA image
        (`screenshot` 3D). The `template` must be a grayscale image.

        Returns ((center_x, center_y), confidence) when confidence >= threshold,
        otherwise returns (None, 0). Preserves the special-case guard used for
        capsule detection where a low-confidence hit at (0,0) is ignored.
        """
        if template is None:
            return None, 0

        # Normalize screenshot to grayscale 2D
        if len(screenshot.shape) == 3:
            # handle BGRA/BGR
            try:
                screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2GRAY)
            except Exception:
                screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
        else:
            screenshot_gray = screenshot

        th, tw = template.shape
        sh, sw = screenshot_gray.shape
        if sw < tw or sh < th:
            return None, 0

        result = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        if max_val >= threshold:
            center_x = max_loc[0] + tw // 2
            center_y = max_loc[1] + th // 2
            # preserve capsule special-case: ignore very-low confidence at (0,0)
            if max_val < threshold + 0.1 and max_loc == (0, 0):
                return None, max_val
            return (center_x, center_y), max_val

        return None, 0

    @staticmethod
    def in_tolerance(a, b, tol=5):
        return abs(a[0] - b[0]) <= tol and abs(a[1] - b[1]) <= tol
