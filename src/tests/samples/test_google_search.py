"""
@author: Ashutosh Mishra | ashutosh_mishra_@outlook.com
@created: 1 Sep 2022
@last_modified: 03 Jun 2025
@desc: Test class for Google Search;
    Contains tests methods for the Google Search.

    Execute: pytest --browser=edge --url 'https://www.wikipedia.org/' -v -k test_google
"""


import pytest
import sys
import allure
from src.base.basetest import BaseTest
from src.pages.samples.google_search_page import GoogleSearchPage


@pytest.mark.sanity
@pytest.mark.first
class TestGoogleSearch(BaseTest):

    # ------------------------------------------------
    # Before each Test def,
    # we need to initialize some page objects
    # ------------------------------------------------
    # @pytest.fixture(autouse=True)
    # def class_setup(self):
    #     self.loginPage = LoginPage(self.driver)
    #     self.config = Config()
    # -[END]-----------------------------------------------
    google_search_page = None

    # -[TESTs STARTS FROM HERE]-----------------------------------------------

    def test_search_google_and_browse_first_result(self):
        # Create object for page(s)
        self.google_search_page = GoogleSearchPage(self.driver)

        # Steps
        self.google_search_page.search('EARTH')
        self.google_search_page.extract_and_verify_for_results()
        self.google_search_page.browse_first_result_link()

    def test_sample(self):
        assert True, "All good"
