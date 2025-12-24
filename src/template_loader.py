import cv2
import numpy as np
from pathlib import Path


class TemplateLoader:
    """Loads fish and capsule templates from the `templates` directory."""

    def __init__(self, base_dir: Path):
        self.templates_dir = base_dir / "templates"
        self.fish_template = None
        self.capsule_template = None
        self.cast_template = None
        self.bite_template = None
        self.catch_template = None

    def detect_frame_bounds(self, sprite_sheet, rows=4, cols=8, threshold=10):
        """Automatically detect frame bounds and padding in a sprite sheet."""
        height, width = sprite_sheet.shape
        horizontal_proj = np.sum(sprite_sheet > threshold, axis=1)
        vertical_proj = np.sum(sprite_sheet > threshold, axis=0)
        non_empty_rows = np.where(horizontal_proj > 0)[0]
        non_empty_cols = np.where(vertical_proj > 0)[0]

        if len(non_empty_rows) == 0 or len(non_empty_cols) == 0:
            return None

        min_row = non_empty_rows[0]
        max_row = non_empty_rows[-1]
        min_col = non_empty_cols[0]
        max_col = non_empty_cols[-1]

        active_height = max_row - min_row + 1
        active_width = max_col - min_col + 1

        frame_height = active_height // rows
        frame_width = active_width // cols

        return {
            'offset_x': min_col,
            'offset_y': min_row,
            'frame_width': frame_width,
            'frame_height': frame_height,
            'active_width': active_width,
            'active_height': active_height
        }

    def load_templates(self):
        cast_path = self.templates_dir / "1_cast_line.png"
        if cast_path.exists():
            self.cast_template = cv2.imread(str(cast_path), cv2.IMREAD_GRAYSCALE)
            if self.cast_template is not None:
                print("✓ Loaded: 1_cast_line.png")
            else:
                print("⚠ Warning: Failed to load 1_cast_line.png")
        else:
            print(f"⚠ Warning: 1_cast_line.png not found in {self.templates_dir}!")

        bite_path = self.templates_dir / "2_fish_bite.png"
        if bite_path.exists():
            self.bite_template = cv2.imread(str(bite_path), cv2.IMREAD_GRAYSCALE)
            if self.bite_template is not None:
                print("✓ Loaded: 2_fish_bite.png")
            else:
                print("⚠ Warning: Failed to load 2_fish_bite.png")
        else:
            print(f"⚠ Warning: 2_fish_bite.png not found in {self.templates_dir}!")

        cath_path = self.templates_dir / "3_catch.png"
        if cath_path.exists():
            self.catch_template = cv2.imread(str(cath_path), cv2.IMREAD_GRAYSCALE)
            if self.catch_template is not None:
                print("✓ Loaded: 3_catch.png")
            else:
                print("⚠ Warning: Failed to load 3_catch.png")
        else:
            print(f"⚠ Warning: 3_catch.png not found in {self.templates_dir}!")

        return self.cast_template is not None \
                and self.bite_template is not None \
                and self.catch_template is not None
