from actions.base_action import BaseAction
from components import highlight_message


class OpenAppAction(BaseAction):

    def execute(self, **kwargs):
        highlight_message("📱 Launching app...")

        if hasattr(self.manager.driver, "launch_app"):
            self.manager.driver.launch_app()

        elif hasattr(self.manager.driver, "start_activity"):
            self.manager.driver.start_activity(
                self.manager.app_package, self.manager.app_activity
            )

        elif hasattr(self.manager.driver, "activate_app"):
            self.manager.driver.activate_app(self.manager.app_package)

        else:
            raise AttributeError("The driver does not support app launching methods.")

