from selenium.webdriver.support.wait import WebDriverWait
from actions.base_action import BaseAction


class WaitForScreenAction(BaseAction):

    def execute(self, **kwargs):
        timeout = kwargs.get("timeout", 5)
        element_id = kwargs.get("element_id", "search_box")

        WebDriverWait(self.manager.driver, timeout).until(
            lambda driver: driver.find_element_by_id(element_id)
        )