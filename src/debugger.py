import cv2
from pathlib import Path

from src.config import DEBUG_SAVE_IMAGES

class Debugger:
    """Saves debug images and overlays detection visuals."""

    def __init__(self, debug_dir: Path, fish_template=None, capsule_template=None, cast_template=None, bite_template=None, catch_template=None):
        self.debug_dir = debug_dir
        self.debug_dir.mkdir(exist_ok=True)
        self.fish_template = fish_template
        self.capsule_template = capsule_template
        self.cast_template = cast_template
        self.bite_template = bite_template
        self.catch_template = catch_template

    def save_debug_images(self, screenshot_bgr, screenshot_gray, cast_pos, bite_pos, catch_pos, fish_pos, capsule_pos, frame_num):
        if not DEBUG_SAVE_IMAGES:
            return

        screenshot_path = self.debug_dir / f"frame_{frame_num:04d}_screenshot.png"
        cv2.imwrite(str(screenshot_path), screenshot_bgr)

        screenshot_gray_path = self.debug_dir / f"frame_{frame_num:04d}_screenshot_gray.png"
        cv2.imwrite(str(screenshot_gray_path), screenshot_gray)

        if frame_num == 0:
            if self.cast_template is not None:
                cast_template_path = self.debug_dir / "cast_template_.png"
                cv2.imwrite(str(cast_template_path), self.cast_template)

            if self.bite_template is not None:
                bite_template_path = self.debug_dir / "bite_template_.png"
                cv2.imwrite(str(bite_template_path), self.bite_template)

            if self.catch_template is not None:
                catch_template_path = self.debug_dir / "catch_template_.png"
                cv2.imwrite(str(catch_template_path), self.catch_template)

            if self.fish_template is not None:
                fish_template_path = self.debug_dir / "fish_template_.png"
                cv2.imwrite(str(fish_template_path), self.fish_template)

            if self.capsule_template is not None:
                capsule_template_path = self.debug_dir / "capsule_template.png"
                cv2.imwrite(str(capsule_template_path), self.capsule_template)

        debug_img = screenshot_bgr.copy()

        if cast_pos is not None and self.cast_template is not None:
            h, w = self.cast_template.shape
            x1 = max(0, cast_pos[0] - w // 2)
            y1 = max(0, cast_pos[1] - h // 2)
            x2 = min(debug_img.shape[1], cast_pos[0] + w // 2)
            y2 = min(debug_img.shape[0], cast_pos[1] + h // 2)
            cv2.rectangle(debug_img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(debug_img, "CAST", (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)

        if bite_pos is not None and self.bite_template is not None:
            h, w = self.bite_template.shape
            x1 = max(0, bite_pos[0] - w // 2)
            y1 = max(0, bite_pos[1] - h // 2)
            x2 = min(debug_img.shape[1], bite_pos[0] + w // 2)
            y2 = min(debug_img.shape[0], bite_pos[1] + h // 2)
            cv2.rectangle(debug_img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(debug_img, "BITE", (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)

        if catch_pos is not None and self.catch_template is not None:
            h, w = self.catch_template.shape
            x1 = max(0, catch_pos[0] - w // 2)
            y1 = max(0, catch_pos[1] - h // 2)
            x2 = min(debug_img.shape[1], catch_pos[0] + w // 2)
            y2 = min(debug_img.shape[0], catch_pos[1] + h // 2)
            cv2.rectangle(debug_img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(debug_img, "CATCH", (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)

        if fish_pos is not None and self.fish_template is not None:
            h, w = self.fish_template.shape
            x1 = max(0, fish_pos[0] - w // 2)
            y1 = max(0, fish_pos[1] - h // 2)
            x2 = min(debug_img.shape[1], fish_pos[0] + w // 2)
            y2 = min(debug_img.shape[0], fish_pos[1] + h // 2)
            cv2.rectangle(debug_img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(debug_img, "FISH", (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)

        if capsule_pos is not None and self.capsule_template is not None:
            h, w = self.capsule_template.shape
            x1 = max(0, capsule_pos[0] - w // 2)
            y1 = max(0, capsule_pos[1] - h // 2)
            x2 = min(debug_img.shape[1], capsule_pos[0] + w // 2)
            y2 = min(debug_img.shape[0], capsule_pos[1] + h // 2)
            cv2.rectangle(debug_img, (x1, y1), (x2, y2), (255, 0, 0), 2)
            cv2.putText(debug_img, "CAPSULE", (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 0, 0), 1)

        debug_img_path = self.debug_dir / f"frame_{frame_num:04d}_debug.png"
        cv2.imwrite(str(debug_img_path), debug_img)

        if self.capsule_template is not None:
            if len(screenshot_bgr.shape) == 3:
                screenshot_gray_for_match = cv2.cvtColor(screenshot_bgr, cv2.COLOR_BGR2GRAY)
            else:
                screenshot_gray_for_match = screenshot_gray

            result = cv2.matchTemplate(screenshot_gray_for_match, self.capsule_template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

            result_normalized = cv2.normalize(result, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
            result_path = self.debug_dir / f"frame_{frame_num:04d}_capsule_match_result.png"
            cv2.imwrite(str(result_path), result_normalized)

            result_vis = cv2.cvtColor(result_normalized, cv2.COLOR_GRAY2BGR)
            cv2.circle(result_vis, max_loc, 5, (0, 0, 255), -1)
            cv2.putText(result_vis, f"Max: {max_val:.3f} @ {max_loc}", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
            result_vis_path = self.debug_dir / f"frame_{frame_num:04d}_capsule_match_result_marked.png"
            cv2.imwrite(str(result_vis_path), result_vis)

    def show_live(self, screenshot_bgr, detections: dict, window_name: str = "Debug - Duet Night Abyss Bot", window_pos=None):
        """Display a live debug overlay in an OpenCV window.

        detections: dict where keys are labels and values are dicts with:
          - 'pos': (x,y) center or None
          - 'conf': float confidence
          - 'template': optional grayscale template image (to get size)
          - 'color': optional BGR tuple for rectangle/text
        """
        img = screenshot_bgr.copy()

        for label, info in (detections or {}).items():
            pos = info.get('pos')
            conf = info.get('conf', 0)
            tmpl = info.get('template')
            color = info.get('color', (0, 255, 255))

            if pos is None:
                continue

            x, y = pos
            if tmpl is not None:
                h, w = tmpl.shape
                x1 = max(0, x - w // 2)
                y1 = max(0, y - h // 2)
                x2 = min(img.shape[1], x + w // 2)
                y2 = min(img.shape[0], y + h // 2)
                cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
                cv2.putText(img, f"{label}: {conf:.2f}", (x1, max(0, y1 - 5)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
            else:
                cv2.circle(img, (x, y), 6, color, -1)
                cv2.putText(img, f"{label}: {conf:.2f}", (x + 8, y - 8), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        if window_pos is not None:
            try:
                cv2.moveWindow(window_name, int(window_pos[0]), int(window_pos[1]))
            except Exception:
                pass
        cv2.imshow(window_name, img)
        cv2.waitKey(1)
