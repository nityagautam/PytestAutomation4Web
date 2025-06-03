"""
@author: Ashutosh Mishra | ashutosh_mishra_@outlook.com
@created: 1 Sep 2022
@last_modified: 03 Jun 2025
@desc: GoogleSearch Page Class;
    Contains Page Object for the Google Search.
"""

from src.base.basepage import BasePage


class GoogleSearchPage(BasePage):
    def __init__(self, driver):
        # Init and load from super/parent class
        super().__init__(driver)
        self.driver = driver
        # Since we have inherited the 'BasePage'
        # - Logger will be attached to self.log
        # - All the methods from Selenium driver will be attached to self
        # - All the methods from the Utility class will be attached to self
        # - Locators from the 'locators.py' for 'LoginPage' will be attached to self

    def search(self, keyword):
        self.log.debug(f"Initiating google search with keyword: {keyword} ...")
        # self.type(locator="xpath=//input[@name='q']", value=keyword + "\n")
        self.type(locator=self.SEARCH_BOX, value=keyword + "\n")
        # self.click(locator="xpath=//*[@name='btnK' and @type='submit']")
        self.click(locator=self.SEARCH_SUBMIT_BTN)
        
    def extract_and_verify_for_results(self):
        self.log.debug(f"Initiating extraction of first element on the result page ...")
        # first_link = self.get_element_with_wait(locator="xpath=(//*[@id='rso']//a)[1]")
        first_link = self.get_element_with_wait(locator=self.SEARCH_RESULT_FIRST_LINK)
        self.log.debug(f"First result for the keyword: {first_link.text} ...")
        assert len(first_link.text) > 0, "Zero result found after search"

    def browse_first_result_link(self):
        # first_link = self.get_element_with_wait(locator="xpath=(//*[@id='rso']//a)[1]")
        first_link = self.get_element_with_wait(locator=self.SEARCH_RESULT_FIRST_LINK)
        self.log.debug(f"Browsing First result for the keyword: {first_link.text} ...")
        self.click(locator=self.SEARCH_RESULT_FIRST_LINK)

