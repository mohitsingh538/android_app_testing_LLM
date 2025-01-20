from appium.webdriver import Remote



class AppReload:
    
    def __init__(self, driver: Remote, app_package: str):
        self.driver = driver
        self.app_package = app_package

    def is_app_running(self):
        """Check if the app is running."""
        try:
            # Query the app state
            app_state = self.driver.query_app_state(self.app_package)
            match app_state:
                
                case 4:  # Foreground
                    if app_state == 4:
                        print(f"App '{self.app_package}' is running in the foreground.")
                        return True
            
                case 3:  # Background
                    print(f"App '{self.app_package}' is running in the background.")
                    return True
                
                case _:
                    print(f"App '{self.app_package}' is not running.")
                    return False

        except Exception as e:
            print(f"Error checking app state: {e}")
            return False

    def kill_app(self):
        """Kill the app."""
        try:
            # Terminate the app
            if self.driver.terminate_app(self.app_package):
                print(f"App '{self.app_package}' has been terminated.")
            else:
                print(f"Failed to terminate app '{self.app_package}'.")
        
        except Exception as e:
            print(f"Error terminating app: {e}")
