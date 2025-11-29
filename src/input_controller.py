import time
import vgamepad as vg

from src.config import DEBUG_MODE

class InputController:
    """Handles virtual gamepad A button presses (mapped to Space behaviour)."""

    def __init__(self):
        self.space_pressed = False
        self.gamepad = vg.VX360Gamepad()

    def hold_space(self):
        if not self.space_pressed:
            try:
                # if DEBUG_MODE:
                #     print("🎮 A button pressed")
                self.gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
                self.gamepad.update()
                self.space_pressed = True
                time.sleep(0.1)
            except Exception as e:
                print(f"⚠ Error pressing A (Space): {e}")

    def release_space(self):
        if self.space_pressed:
            try:
                # if DEBUG_MODE:
                #     print("🎮 A button released")
                self.gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
                self.gamepad.update()
                self.space_pressed = False
            except Exception as e:
                print(f"⚠ Error releasing A (Space): {e}")

    def press_space(self, hold_duration=None):
        try:
            self.hold_space()

            if hold_duration is not None and hold_duration > 0.0:
                time.sleep(hold_duration)

            self.release_space()
        except Exception as e:
            print(f"⚠ Error pressing A (Space): {e}")

        time.sleep(0.1)

    def restart_space_pressing(self):
        try:
            # if DEBUG_MODE:
            #     print("🎮 Restarting A press")
            self.gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
            self.gamepad.update()
            time.sleep(0.1)
            self.gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
            self.gamepad.update()
            self.space_pressed = True
            time.sleep(0.1)
        except Exception as e:
            print(f"⚠ Error restarting A press: {e}")
