"""
@author: Ashutosh Mishra | ashutosh_mishra_@outlook.com
@created: 1 Sep 2022
@last_modified: 03 Jun 2025
@desc: WikipediaSearch Test Class;
    Contains PTest methods for the Wikipedia Search.

    Execute: pytest --browser=edge --url 'https://www.wikipedia.org/' -v -k test_wiki
"""

import pytest
from src.base.basetest import BaseTest
from src.config import config
from src.pages.samples.wikipedia_search import WikiSearch


@pytest.mark.sample
class TestCaseWikipediaLandingPage(BaseTest):

    def test_wiki_search_and_open_topic(self):
        search_topic = "Programming languages"

        wiki_page = WikiSearch(self.driver)                     # PageObject Class
        wiki_page.get_screenshot("Wiki_landing_page")           # Take the screenshot of webpage with given name
        wiki_page.search(search_topic)
        wiki_page.script_wait(sleep_time=config.DEFAULT_WAIT)

