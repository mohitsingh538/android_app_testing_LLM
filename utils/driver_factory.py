from appium.webdriver import Remote
from appium.options.android import UiAutomator2Options
from utils.config import Config


class DriverFactory:

    @staticmethod
    def create_driver(device_id, app_package, app_activity, platform_version):
        options = UiAutomator2Options()
        options.device_name = device_id
        options.app_package = app_package
        options.app_activity = app_activity
        options.platform_name = "Android"
        options.no_reset = True
        options.platform_version = platform_version
        options.new_command_timeout = 6000

        return Remote(Config.DRIVER_URL, options=options)