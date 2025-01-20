from device_manager.reload_app import AppReload
from utils.driver_factory import DriverFactory


class AppiumAppManager:

    def __init__(self, app_package: str, app_activity: str, **kwargs):

        __slots__ = ("app_package", "app_activity", "device_id", "platform_version", "driver")

        for key, value in kwargs.items():
            if key not in __slots__:
                raise TypeError(f"Unexpected keyword argument '{key}'")

        self.app_package = app_package
        self.app_activity = app_activity
        self.device_id = kwargs.get("device_id")
        self.platform_version = kwargs.get("platform_version")

        self.driver = DriverFactory.create_driver(
            self.device_id, app_package, app_activity, self.platform_version
        )

    def manage_state(self):
        app_state_manager = AppReload(driver=self.driver, app_package=self.app_package)
        if app_state_manager.is_app_running():
            app_state_manager.kill_app()

    def quit(self):
        """Quit the Appium driver"""
        if self.driver:
            self.driver.quit()
