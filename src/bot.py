import cv2
import keyboard
import time
from pathlib import Path

from src.config import (
    REFERENCE_WIDTH,
    REFERENCE_HEIGHT,
    REFERENCE_REGION,
    BITING_TIMEOUT,
    FISHING_TIME_MIN,
    FISH_CAUGHT_DELAY,
    BIGGER_FISH_DELAY,
    CAST_CATCH_THRESHOLD,
    BITE_THRESHOLD,
    TARGET_FPS,
    FRAME_DELAY,
    DEBUG_MODE,
    DEBUG_WINDOW_POSITION,
    EXIT_KEY,
    InputFix,
)
from src.template_loader import TemplateLoader
from src.screencapture import ScreenCapture
from src.input_controller import InputController
from src.detector import Detector
from src.debugger import Debugger


class FishingBot:
    """Main bot class that composes the other components and runs the loop."""

    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.template_loader = TemplateLoader(base_dir)
        self.capture = ScreenCapture()
        self.input = InputController()
        self.debug_dir = base_dir / "debug"
        self.init()

    def init(self):
        self.debug = None
        self.input_fixed = InputFix.NOT
        self.caps_start_pos = None
        self.caps_prev_pos = None

    def run(self):
        # Orchestration and setup for fishing phases. This method performs
        # initialization and then enters the appropriate phase. The
        # detailed reeling loop is implemented in `reeling()`.
        print("=" * 50)
        print("Duet Night Abyss - Auto Fishing Bot")
        print("=" * 50)

        # Basic configuration/logging
        screen_region, screen_width, screen_height = self.capture.get_screen_region()
        print(f"\nConfiguration:")
        print(f"  Screen resolution: {screen_width}x{screen_height}")
        print(f"  Screen region: {screen_region}")
        print(f"  Reference resolution: {REFERENCE_WIDTH}x{REFERENCE_HEIGHT}")
        print(f"  Reference region: {REFERENCE_REGION}")
        print(f"  Target FPS: {TARGET_FPS}")
        print(f"  Debug mode: {DEBUG_MODE}")
        print(f"  Exit key: {EXIT_KEY.upper()}")

        # Load templates and run a short input test
        print("\nLoading templates...")
        if not self.template_loader.load_templates():
            print("\n❌ Error: Failed to load templates!")
            return

        print(f"\n✓ All templates loaded.")

        # Initialize debugger for live overlays (used by waiting/biting/reeling)
        self.debug = Debugger(
            self.base_dir / "debug",
            cast_template=self.template_loader.cast_template,
            bite_template=self.template_loader.bite_template,
            catch_template=self.template_loader.catch_template,
        )

        print("\n⚠ Important: Running as administrator may be required for Space actions!")
        print("   If not working, try running the script as Administrator.")
        print("\nTesting Space (1 second)...")
        print("   Make sure the game window is active!")
        time.sleep(1)
        try:
            self.input.hold_space()
            time.sleep(0.1)
            self.input.release_space()
            print("✓ Space test successful!")
        except Exception as e:
            print(f"⚠ Space test error: {e}")
            print("   Try running as Administrator!")

        print("\nStarting in 3 seconds...")
        print("Position your game window appropriately!")
        print("⚠ IMPORTANT: Ensure the game window is active!")
        time.sleep(3)

        print("\n▶ Bot starting reeling phase now. Press ESC to exit.\n")

        self.idle()

    def idle(self, recast = False):
        """Stub for the waiting phase.

        This phase should wait for the fishing opportunity (cast complete, idle),
        and then transition to the biting phase. Currently a placeholder.
        """
        print("Entering waiting phase: looking for cast indicator...")

        if self.template_loader.cast_template is None:
            print("⚠ No cast template available; cannot run waiting phase.")
            return

        try:
            frame_num = 0
            start_time = time.time()
            while True:
                if keyboard.is_pressed(EXIT_KEY):
                    print("\n⏹ Exiting waiting phase (exit key pressed)")
                    return

                current_region, _, _ = self.capture.get_screen_region()

                try:
                    screenshot = self.capture.grab(current_region)
                except Exception:
                    time.sleep(FRAME_DELAY)
                    continue

                # Prepare BGR copy for live debug overlay
                try:
                    screenshot_bgr = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2BGR)
                except Exception:
                    screenshot_bgr = screenshot

                # Use the unified detector helper for cast detection. It accepts
                # either color/BGRA or grayscale screenshots and returns a center
                # coordinate and confidence when found.
                cast_pos, cast_conf = Detector.find_template(screenshot, self.template_loader.cast_template, CAST_CATCH_THRESHOLD)

                # Show live debug overlay for waiting phase and save per-frame phase matches
                if DEBUG_MODE and self.debug is not None:
                    detections = {
                        'cast': {'pos': cast_pos, 'conf': cast_conf, 'template': self.template_loader.cast_template, 'color': (0, 255, 255)}
                    }
                    self.debug.show_live(screenshot_bgr, detections, window_pos=DEBUG_WINDOW_POSITION)
                    try:
                        self.debug.save_debug_images(screenshot_bgr, screenshot, cast_pos, None, None, frame_num)
                    except Exception:
                        pass
                    

                if cast_pos is not None:
                    center_x, center_y = cast_pos
                    print(f"Detected cast at ({center_x}, {center_y}) with confidence {cast_conf:.2f}")

                    # Press Space to cast the bait into the water
                    try:
                        self.input.press_space()
                        print("✓ Cast action sent (Space)")
                    except Exception as e:
                        print(f"⚠ Error when attempting to cast: {e}")

                    # Transition to biting phase
                    self.waiting()
                    return
                else:
                    if recast and time.time() - start_time > BIGGER_FISH_DELAY:
                        print("⏲ Waiting phase: no cast detected yet, possible chance for bigger fish. Recasting...")
                        time.sleep(0.5)
                        self.input.press_space()
                        self.waiting()
                        return

                # Sleep a short time to avoid tight CPU loop
                time.sleep(FRAME_DELAY)
                frame_num += 1

        except KeyboardInterrupt:
            print("\n⏹ Waiting phase interrupted by user.")

    def waiting(self):
        """Stub for the waiting phase.

        This phase should wait for the fishing opportunity (cast complete, idle),
        and then transition to the biting phase. Currently a placeholder.
        """
        print("Entering waiting phase: waiting for cast to complete...")
        if self.template_loader.bite_template is None:
            print("⚠ Missing bite template; cannot run biting phase.")
            return

        try:
            frame_num = 0
            start_time = time.time()
            while True:
                if keyboard.is_pressed(EXIT_KEY):
                    print("\n⏹ Exiting biting phase (exit key pressed)")
                    return

                current_region, _, _ = self.capture.get_screen_region()
                try:
                    screenshot = self.capture.grab(current_region)
                except Exception:
                    time.sleep(FRAME_DELAY)
                    continue

                # Check current icon states
                # Prepare BGR for debug display
                try:
                    screenshot_bgr = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2BGR)
                except Exception:
                    screenshot_bgr = screenshot

                bite_pos, bite_conf = Detector.find_template(screenshot, self.template_loader.bite_template, BITE_THRESHOLD)

                # Save per-frame phase matches for debugging (cast/bite/catch)
                if DEBUG_MODE and self.debug is not None:
                    try:
                        gray = cv2.cvtColor(screenshot_bgr, cv2.COLOR_BGR2GRAY)
                    except Exception:
                        try:
                            gray = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2GRAY)
                        except Exception:
                            gray = None
                    try:
                        self.debug.save_debug_images(screenshot_bgr, gray, None, bite_pos, None, frame_num)
                    except Exception:
                        pass

                if DEBUG_MODE and self.debug is not None:
                    detections = {
                        'bite': {'pos': bite_pos, 'conf': bite_conf, 'template': self.template_loader.bite_template, 'color': (0, 128, 255)}
                    }
                    self.debug.show_live(screenshot_bgr, detections, window_pos=DEBUG_WINDOW_POSITION)

                if bite_pos is not None:
                    print(f"Detected bite at {bite_pos} with confidence {bite_conf:.2f}")
                    self.biting()
                    return
                else:
                    if time.time() - start_time > BITING_TIMEOUT:
                        print(f"⏲ Biting phase has not started after {BITING_TIMEOUT} seconds, pressing Space to retry cast.")
                        self.input.press_space()
                        start_time = time.time()
                
                frame_num += 1
                time.sleep(FRAME_DELAY)

        except KeyboardInterrupt:
            print("\n⏹ Waiting phase interrupted by user.")
        

    def biting(self):
        """Stub for the biting phase.

        This phase should detect a bite and transition into reeling. Currently a placeholder.
        """
        print("Entering biting phase: waiting for bite to appear and resolve...")

        if self.template_loader.catch_template is None:
            print("⚠ Missing catch template; cannot run biting phase.")
            return

        try:
            frame_num = 0
            biting_done = False
            start_time = time.time()
            while True:
                if keyboard.is_pressed(EXIT_KEY):
                    print("\n⏹ Exiting biting phase (exit key pressed)")
                    return

                current_region, _, _ = self.capture.get_screen_region()
                try:
                    screenshot = self.capture.grab(current_region)
                except Exception:
                    time.sleep(FRAME_DELAY)
                    continue

                # Check current icon states
                # Prepare BGR for debug display
                try:
                    screenshot_bgr = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2BGR)
                except Exception:
                    screenshot_bgr = screenshot

                catch_pos, catch_conf = Detector.find_template(screenshot, self.template_loader.catch_template, CAST_CATCH_THRESHOLD)

                # Save per-frame phase matches for debugging (cast/bite/catch)
                if DEBUG_MODE and self.debug is not None:
                    try:
                        gray = cv2.cvtColor(screenshot_bgr, cv2.COLOR_BGR2GRAY)
                    except Exception:
                        try:
                            gray = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2GRAY)
                        except Exception:
                            gray = None
                    try:
                        self.debug.save_debug_images(screenshot_bgr, gray, None, None, catch_pos, frame_num)
                    except Exception:
                        pass

                if DEBUG_MODE and self.debug is not None:
                    detections = {
                        'catch': {'pos': catch_pos, 'conf': catch_conf, 'template': self.template_loader.catch_template, 'color': (0, 0, 255)}
                    }
                    self.debug.show_live(screenshot_bgr, detections, window_pos=DEBUG_WINDOW_POSITION)

                if catch_pos is not None:
                    print(f"Detected bite at {catch_pos} with confidence {catch_conf:.2f}")
                    try:
                        self.input.press_space()
                        print("✓ Catch action sent (Space)")
                    except Exception as e:
                        print(f"⚠ Error when attempting to catch: {e}")
                    
                    self.restart_fishing()
                    return
                
                frame_num += 1
                time.sleep(FRAME_DELAY)

        except KeyboardInterrupt:
            print("\n⏹ Biting phase interrupted by user.")

    def restart_fishing(self):
        """Restart the fishing cycle by returning to the waiting phase."""
        print("\n🔄 Restarting fishing cycle...\n")
        self.init()

        # wait a short delay to allow fish caught animation to finish
        time.sleep(FISH_CAUGHT_DELAY)

        # confirm the captured fish dialog
        self.input.press_space()

        # small delay to endsure dialog is closed
        time.sleep(1.5)

        # restart the whole process
        self.idle(True)