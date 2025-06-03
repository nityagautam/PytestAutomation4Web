"""
@author: Ashutosh Mishra | ashutosh_mishra_@outlook.com
@created: 11 Jan 2024
@last_modified: 03 Jun 2025
@desc: 
    Base Page class implementation
    It implements methods which are common to all the pages throughout the application
    This class needs to be inherited by all the page classes
    This should not be used by creating object instances

Implementation Example for this BasePage:
    Class YouPageObjectClassName(BasePage)
        ... everything else
"""

from src.pages.locators import ALL_LOCATORS as LOCATORS
# from src.utilities.selenium_driver import SeleniumDriver
from src.utilities.Logger import Logger
from src.utilities.SD import SeleniumDriver
from src.utilities.utilities import CollectAttributesFromDict


class BasePage(SeleniumDriver, CollectAttributesFromDict):

    # Collect all the attributes from the LOCATOR dict
    def __init__(self, driver):
        """
            Constructor for the basepage; Needs to be inherited by all the pageobject classes.
            It simply attach the driver objects and the provided locators attributes to the page where it is inherited.
            For the LOCATOR uses, refer the README.md

            :param driver: Needs Web driver object
            :return:
        """

        # Init the Selenium driver and Attach the web driver
        # ----------------------------------------------------
        SeleniumDriver.__init__(self, driver)
        self.driver = driver            # Attach the driver to self
        log = Logger().get_logger()     # Get the logger for this page

        # Collect the attributes from the LOCATOR object
        # For the LOCATOR uses, refer the README.md
        # ----------------------------------------------------
        if self.__class__.__name__ in LOCATORS:
            CollectAttributesFromDict.__init__(self, LOCATORS[self.__class__.__name__])
