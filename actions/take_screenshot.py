import os
import datetime
from components import highlight_message
from .base_action import BaseAction


class TakeScreenshotAction(BaseAction):

    def execute(self, **kwargs):
        output_path = kwargs.get("output_path", None)

        try:
            if not output_path:
                output_path = os.path.join(os.getcwd(), "screenshots", self.manager.app_package)
                os.makedirs(output_path, exist_ok=True)

            SCREENSHOT_PATH = f"{output_path}/{datetime.datetime.now()}.png"

            highlight_message("📸 Taking screenshot...")
            self.manager.driver.save_screenshot(SCREENSHOT_PATH)
            print(f"💾 Screenshot saved to {SCREENSHOT_PATH}\n")

            return True

        except Exception as e:
            print(f"Failed to take screenshot: {e}\n")
            return False
