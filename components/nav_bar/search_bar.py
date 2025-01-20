import xml.etree.ElementTree as ET
from selenium.common import NoSuchElementException
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SearchBarComponent:
    def __init__(self, driver):
        self.driver = driver

    @staticmethod
    def identify_search_bar(xml_content):
        """Parse the UI dump XML file and identify search bars."""
        try:
            root = ET.fromstring(xml_content)
            search_results = []
            strategies = SearchBarComponent.get_identification_strategies()

            def search_node(node, parent_path=''):
                attrs = node.attrib
                current_path = f"{parent_path}/{node.tag}"

                if 'bounds' in attrs:
                    current_path += f"[{attrs['bounds']}]"

                for strategy in strategies:
                    result = strategy(node, attrs, current_path)
                    if result:
                        search_results.append(result)

                for child in node:
                    search_node(child, current_path)

            search_node(root)

            search_results.sort(key=lambda x: (not x.get('is_resource_match', False)))
            return search_results

        except ET.ParseError as e:
            print(f"Error parsing XML content: {e}")
            return []

    @staticmethod
    def get_identification_strategies():
        return [
            SearchBarComponent.match_resource_id,
            SearchBarComponent.match_text,
            SearchBarComponent.match_class_name
        ]

    @staticmethod
    def match_resource_id(node, attrs, path):
        resource_id = attrs.get('resource-id', '').lower()
        if 'search' in resource_id and attrs.get('enabled', 'false').lower() == 'true':
            return {
                'element': node.tag,
                'attributes': attrs,
                'path': path,
                'is_resource_match': True
            }

    @staticmethod
    def match_text(node, attrs, path):
        text = attrs.get('text', '').lower()
        if 'search' in text and attrs.get('enabled', 'false').lower() == 'true':
            return {
                'element': node.tag,
                'attributes': attrs,
                'path': path,
                'is_resource_match': False
            }

    @staticmethod
    def match_class_name(node, attrs, path):
        class_name = attrs.get('class', '').lower()
        if 'search' in class_name and attrs.get('enabled', 'false').lower() == 'true':
            return {
                'element': node.tag,
                'attributes': attrs,
                'path': path,
                'is_resource_match': False
            }


class SearchBoxFinder(SearchBarComponent):

    def __init__(self, driver):
        super().__init__(driver=driver)

    def _find_search_box(self):
        """Get the page source and identify search boxes."""
        page_source = self.driver.page_source
        search_boxes = self.identify_search_bar(page_source)
        return search_boxes

    def locate_and_identify_search_box(self, timeout: int = 10):
        # XPath expression to locate a potential search box
        search_box_expression = "//android.widget.TextView[contains(translate(@text, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'search')]"

        try:
            # Wait for the element to be visible
            search_label = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((By.XPATH, search_box_expression))
            )

            if search_label:
                print("Search label found using XPath.")

                # Use the SearchBarComponent to identify search boxes in the XML content
                search_boxes = self._find_search_box()

                if search_boxes:
                    search_box = search_boxes[0]  # Assuming we use the first result
                    search_box_id = search_box['attributes'].get('resource-id')

                    if search_box_id:
                        print("✅ Search box ID found:", search_box_id)
                        return search_box_id

                    else:
                        print("❌ No resource ID found for the search box.")

                else:
                    print("❌ No search boxes identified in the page source.")

            else:
                print("❌ Search label not found.")

        except Exception as e:
            print(f"❌ Error locating the search box: {e}")

        return None

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

            print(f"🔍 Searched for '{search_text}' successfully.")
            return True

        except (Exception, NoSuchElementException) as e:
            print(f"Error searching for '{search_text}': {e}")

            return False