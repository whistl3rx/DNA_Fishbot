import cv2
import keyboard
import time
from consolemenu import SelectionMenu
from pathlib import Path

from src.config import (
    REFERENCE_WIDTH,
    REFERENCE_HEIGHT,
    REFERENCE_REGION,
    BITING_TIMEOUT,
    FISHING_TIME_MIN,
    FISH_CAUGHT_DELAY,
    BIGGER_FISH_DELAY,
    CAST_THRESHOLD,
    BITE_THRESHOLD,
    CATCH_THRESHOLD,
    FISH_THRESHOLD,
    CAPSULE_THRESHOLD,
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

        self.waiting()

    def waiting(self, recast = False):
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
                cast_pos, cast_conf = Detector.find_template(screenshot, self.template_loader.cast_template, CAST_THRESHOLD)

                # Show live debug overlay for waiting phase and save per-frame phase matches
                if DEBUG_MODE and self.debug is not None:
                    detections = {
                        'cast': {'pos': cast_pos, 'conf': cast_conf, 'template': self.template_loader.cast_template, 'color': (0, 255, 255)}
                    }
                    self.debug.show_live(screenshot_bgr, detections, window_pos=DEBUG_WINDOW_POSITION)
                    try:
                        self.debug.save_debug_images(screenshot_bgr, screenshot, cast_pos, None, None, None, None, frame_num)
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
                    self.biting()
                    return
                else:
                    if recast and time.time() - start_time > BIGGER_FISH_DELAY:
                        print("⏲ Waiting phase: no cast detected yet, possible chance for bigger fish. Recasting...")
                        time.sleep(0.5)
                        self.input.press_space()
                        self.biting()
                        return

                # Sleep a short time to avoid tight CPU loop
                time.sleep(FRAME_DELAY)
                frame_num += 1

        except KeyboardInterrupt:
            print("\n⏹ Waiting phase interrupted by user.")

    def biting(self):
        """Stub for the biting phase.

        This phase should detect a bite and transition into reeling. Currently a placeholder.
        """
        print("Entering biting phase: waiting for bite to appear and resolve...")

        if self.template_loader.bite_template is None or self.template_loader.catch_template is None:
            print("⚠ Missing bite or catch template; cannot run biting phase.")
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

                cast_pos, cast_conf = Detector.find_template(screenshot, self.template_loader.cast_template, CAST_THRESHOLD)
                bite_pos, bite_conf = Detector.find_template(screenshot, self.template_loader.bite_template, BITE_THRESHOLD)
                catch_pos, catch_conf = Detector.find_template(screenshot, self.template_loader.catch_template, CATCH_THRESHOLD)

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
                        self.debug.save_debug_images(screenshot_bgr, gray, cast_pos, bite_pos, catch_pos, None, None, frame_num)
                    except Exception:
                        pass

                if DEBUG_MODE and self.debug is not None:
                    detections = {
                        # 'cast': {'pos': cast_pos, 'conf': cast_conf, 'template': self.template_loader.cast_template, 'color': (0, 255, 255)},
                        'bite': {'pos': bite_pos, 'conf': bite_conf, 'template': self.template_loader.bite_template, 'color': (0, 128, 255)},
                        'catch': {'pos': catch_pos, 'conf': catch_conf, 'template': self.template_loader.catch_template, 'color': (0, 0, 255)},
                    }
                    self.debug.show_live(screenshot_bgr, detections, window_pos=DEBUG_WINDOW_POSITION)

                if not biting_done:
                    if bite_pos is not None:
                        print(f"Detected bite at {bite_pos} with confidence {bite_conf:.2f}")
                        biting_done = True
                    else:
                        if time.time() - start_time > BITING_TIMEOUT:
                            print(f"⏲ Biting phase has not started after {BITING_TIMEOUT} seconds, pressing Space to retry cast.")
                            self.input.press_space()
                            start_time = time.time()
                else:
                    if bite_pos is None:
                        self.input.press_space()
                        print("✓ Catch action sent (Space)")
                    
                        # Transition into reeling phase
                        self.reeling()
                        return
                
                frame_num += 1
                time.sleep(FRAME_DELAY)

        except KeyboardInterrupt:
            print("\n⏹ Biting phase interrupted by user.")

    def reeling(self):
        """Reeling phase: contains the main loop responsible for detection and input.

        This was previously the `run()` method. It retains the same internal logic
        but is focused solely on reeling behavior.
        """
        frame_count = 0
        start_time = time.time()
        # Ensure debugger has all templates available when re-entering reeling
        if self.debug is None:
            self.debug = Debugger(
                self.base_dir / "debug",
                fish_template=self.template_loader.fish_template,
                capsule_template=self.template_loader.capsule_template,
                cast_template=self.template_loader.cast_template,
                bite_template=self.template_loader.bite_template,
                catch_template=self.template_loader.catch_template,
            )

        try:
            while True:
                if keyboard.is_pressed(EXIT_KEY):
                    print("\n⏹ Exiting...")
                    break

                frame_start = time.time()

                current_region, _, _ = self.capture.get_screen_region()

                try:
                    screenshot = self.capture.grab(current_region)
                    screenshot_bgr = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2BGR)
                    screenshot_gray = cv2.cvtColor(screenshot_bgr, cv2.COLOR_BGR2GRAY)
                except Exception:
                    continue

                fish_pos, fish_confidence = Detector.find_template(screenshot_gray, self.template_loader.fish_template, FISH_THRESHOLD)
                capsule_pos, capsule_confidence = Detector.find_template(screenshot_bgr, self.template_loader.capsule_template, CAPSULE_THRESHOLD)
                # print(f"Fish confidence: {fish_confidence:.3f}, Capsule confidence: {capsule_confidence:.3f}")

                if DEBUG_MODE and (frame_count % 10 == 0 or fish_pos is not None or capsule_pos is not None):
                    self.debug.save_debug_images(screenshot_bgr, screenshot_gray, None, None, None, fish_pos, capsule_pos, frame_count)

                action = ""
                if capsule_pos is not None:
                    if self.caps_start_pos is None:
                        self.caps_start_pos = capsule_pos

                    if fish_pos is not None:
                        if fish_pos is None or capsule_pos is None:
                            return False

                        fish_h, fish_w = self.template_loader.fish_template.shape
                        capsule_h, capsule_w = self.template_loader.capsule_template.shape

                        fish_top = fish_pos[1] - fish_h // 2
                        fish_bottom = fish_pos[1] + fish_h // 2
                        fish_left = fish_pos[0] - fish_w // 2
                        fish_right = fish_pos[0] + fish_w // 2

                        capsule_top = capsule_pos[1] - capsule_h // 2
                        capsule_bottom = capsule_pos[1] + capsule_h // 2
                        capsule_left = capsule_pos[0] - capsule_w // 2
                        capsule_right = capsule_pos[0] + capsule_w // 2
                        capsule_center = capsule_pos[1]

                        fish_in_capsule = (
                            fish_pos[0] >= capsule_left and
                            fish_pos[0] <= capsule_right and
                            fish_pos[1] >= capsule_top and
                            fish_pos[1] <= capsule_bottom
                        )

                        overlap = not (
                            fish_right < capsule_left or
                            fish_left > capsule_right or
                            fish_bottom < capsule_top or
                            fish_top > capsule_bottom
                        )

                        if InputFix.NOT == self.input_fixed:
                            print("Switching to controller input")
                            self.input_fixed = InputFix.FIXING
                            self.input.hold_space()
                            self.input_fixed = InputFix.DONE
                            self.input.release_space()
                            time.sleep(0.1)

                        if self.caps_prev_pos is not None and Detector.in_tolerance(capsule_pos, self.caps_start_pos, 5):
                            self.input.restart_space_pressing()
                            action = f"HOLD (capsule did not start moving yet {capsule_pos}, {capsule_top})"
                        elif fish_top < capsule_top:
                            self.input.hold_space()
                            action = "HOLD (fish above capsule)"
                        elif fish_bottom > capsule_center:
                            self.input.release_space()
                            action = "RELEASE (fish in lower third of capsule, release)"
                        elif fish_in_capsule or overlap:
                            action = "HOLD (fish inside capsule - overlap hides fish)"
                        else:
                            self.input.release_space()
                            action = "RELEASE (fish below capsule)"

                        self.caps_prev_pos = capsule_pos
                    else:
                        action = "HOLD (fish likely inside capsule - not visible)"
                elif fish_pos is not None:
                    self.input.release_space()
                    action = "RELEASE (no capsule)"
                else:
                    self.input.release_space()
                    time.sleep(0.1)
                    if InputFix.DONE == self.input_fixed:
                        self.input_fixed = InputFix.NOT
                    action = "SKIP (fish caoguht)"
                    if time.time() - start_time > FISHING_TIME_MIN:
                        print("✓ Fishing cycle complete.")
                        self.restart_fishing()
                        return

                if DEBUG_MODE:
                    debug_img = screenshot_bgr.copy()

                    if fish_pos is not None:
                        h, w = self.template_loader.fish_template.shape
                        if fish_pos[0] - w // 2 >= 0 and fish_pos[1] - h // 2 >= 0:
                            cv2.rectangle(debug_img, (fish_pos[0] - w // 2, fish_pos[1] - h // 2),
                                            (fish_pos[0] + w // 2, fish_pos[1] + h // 2), (0, 255, 0), 2)
                            cv2.putText(debug_img, f"Fish: {fish_confidence:.2f}",
                                        (fish_pos[0] - w // 2, fish_pos[1] - h // 2 - 5),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)

                    if capsule_pos is not None:
                        h, w = self.template_loader.capsule_template.shape
                        cv2.rectangle(debug_img, (capsule_pos[0] - w // 2, capsule_pos[1] - h // 2),
                                      (capsule_pos[0] + w // 2, capsule_pos[1] + h // 2), (255, 0, 255), 2)
                        cv2.putText(debug_img, f"Capsule: {capsule_confidence:.2f}",
                                    (capsule_pos[0] - w // 2, capsule_pos[1] - h // 2 - 5),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 0, 255), 1)

                    cv2.putText(debug_img, f"Action: {action}", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                                (255, 255, 255), 2)

                    window_name = "Debug - Duet Night Abyss Bot"
                    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
                    if DEBUG_WINDOW_POSITION is not None:
                        cv2.moveWindow(window_name, DEBUG_WINDOW_POSITION[0], DEBUG_WINDOW_POSITION[1])
                    cv2.imshow(window_name, debug_img)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break

                frame_count += 1
                elapsed = time.time() - frame_start
                sleep_time = max(0, FRAME_DELAY - elapsed)
                if sleep_time > 0:
                    time.sleep(sleep_time)

                if frame_count % 30 == 0:
                    current_fps = frame_count / (time.time() - start_time)
                    print(f"FPS: {current_fps:.1f} | Action: {action} | "
                          f"Fish: {'✓' if fish_pos else '✗'} | "
                          f"Capsule: {'✓' if capsule_pos else '✗'}")

        except KeyboardInterrupt:
            print("\n⏹ Interrupted by user.")
        finally:
            self.input.release_space()
            if DEBUG_MODE:
                cv2.destroyAllWindows()
            print("\n✓ Bot stopped. Goodbye!")

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
        self.waiting(True)