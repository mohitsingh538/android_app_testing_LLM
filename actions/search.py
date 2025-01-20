import re
from selenium.common import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from actions.base_action import BaseAction
from components import highlight_message
from components.nav_bar.search_bar import SearchBarComponent


class SearchBoxFinder(SearchBarComponent):

    def __init__(self, driver):
        super().__init__(driver)

    def locate_and_identify_search_box(self, timeout: int = 10):
        search_box_expression = "//android.widget.TextView[contains(translate(@text, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'search')]"

        try:
            search_label = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((By.XPATH, search_box_expression))
            )

            if search_label:
                print("\nSearch label found using XPath.")
                search_boxes = self._find_search_box()

                if search_boxes:
                    search_box = search_boxes[0]
                    search_box_id = search_box['attributes'].get('resource-id')
                    return search_box_id

            print("\n❌ No search box identified.")
        except Exception as e:
            print(f"\n❌ Error locating the search box: {e}")

        return None

    def _find_search_box(self):
        page_source = self.driver.page_source
        search_boxes = self.identify_search_bar(page_source)
        return search_boxes

    def search_for_item(self, search_text: str, search_box_id: str):
        """Click on the search box, type the search term, and press Enter"""
        try:
            # Wait for the search box to be visible and clickable
            search_box = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, search_box_id))
            )

            # Click the search box to focus on it
            search_box.click()

            # Wait for the input field to be available again (after the click)
            search_box = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//*[contains(@text, 'Search ')]"))
            )

            search_box.send_keys(search_text)
            ActionChains(self.driver).send_keys(Keys.ENTER).perform()

            WebDriverWait(self.driver, 2)

            print(f"🔍 Searched for '{search_text}' successfully.\n")
            return True

        except (Exception, NoSuchElementException) as e:
            print(f"Error searching for '{search_text}': {e}\n")

            return False


class SearchAction(BaseAction):

    def __init__(self, manager):
        super().__init__(manager)
        self.search_box_finder = SearchBoxFinder(manager.driver)

    def execute(self, **kwargs):
        search_box_id = self.search_box_finder.locate_and_identify_search_box()

        if search_box_id:
            if 'query' in kwargs:
                self._perform_search(search_box_id, kwargs['query'])

            else:
                self._perform_search(search_box_id, kwargs)

        else:
            print("❌ Unable to detect search box ID.\n")

    def _perform_search(self, search_box_id, action_args):
        if isinstance(action_args, dict):
            search_term = self._extract_search_term(action_args)

        else:
            search_term = action_args

        if search_term:
            highlight_message(f"Searching for: {search_term}")
            success = self.search_box_finder.search_for_item(search_term, search_box_id)
            if success:
                print(f"✅ Successfully searched for '{search_term}'.\n")

            else:
                print(f"❌ Failed to search for '{search_term}'.\n")

        else:
            print("❌ No valid search term found in action arguments.\n")

    @staticmethod
    def _extract_search_term(action_args):
        if not isinstance(action_args, dict):
            print(f"Invalid action_args type: {type(action_args)}. Expected dict.")
            return None

        for key, value in action_args.items():
            match = re.match(r'^(.*?)(\s*```|[~!@#$%^&*(){}\[\];:\'\",.<>?/\\|]|$)', value)
            if match:
                return match.group(1).strip()

            else:
                return value.strip()

        return None
