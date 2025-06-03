"""
@author: Ashutosh Mishra | ashutosh_mishra_@outlook.com
@created: 1 Sep 2022
@last_modified: 03 Jun 2025
@desc: WikipediaSearch Page Class;
    Contains Page Object for the Wikipedia Search.
"""
from src.base.basepage import BasePage


class WikiSearch(BasePage):
    KEY = "Programming languages"

    # ===[ PLACED inside LOCATOR object inside locators_map.py ]===
    # SEARCH_INPUT_ID = "searchInput"
    # SEARCH_BTN = "xpath=//button[@type='submit']"

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def search(self, key: str = ""):
        self.log.debug("Trying to search")
        self.log.debug("PAGE Title before search: ====> " + self.driver.title)
        self.type(self.SEARCH_INPUT_ID, key)
        self.click(self.SEARCH_BTN)
        self.log.debug("PAGE Title after search: ====> " + self.driver.title)
