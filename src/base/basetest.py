"""
@author: Ashutosh Mishra | ashutosh_mishra_@outlook.com
@created: 11 Jan 2024
@last_modified: 03 Jun 2025
@desc: 
    Base Test class implementation
    It implements the basic setup for the tests say web-driver, config, logger etc.
    This class needs to be inherited by all the test classes
    This should not be used by creating object instances

Implementation Example for this BaseTest:
    Class YouTestClassName(BaseTest)
        ... everything else
"""


import pytest
# from src.utilities.selenium_driver import SeleniumDriver
from src.utilities.Logger import Logger


@pytest.mark.usefixtures("get_web_driver", "setup")
class BaseTest:
    # ------------------------------------------------------------------
    # initialisations from the fixture methods
    # So that for each child Test class we will have
    # all the properties after inheriting this BaseTest class
    # ------------------------------------------------------------------
    driver = None
    config = None
    log = Logger().get_logger()     # Get the logger

    # ------------------------------------------------------------------
    # Getting Session data for config
    # by just passing the fixture methods name
    # used for config extraction in the 'conftest.py'
    # ------------------------------------------------------------------
    def get_config_data_from_session(self, get_config):
        self.config = get_config
        self.log.debug(f"===> [From Base Test] Config Value: {self.config}")
        self.log.debug(f" URL  : {self.config.ENV_URL}")
        self.log.debug(f" TYPE : {self.config.ENV_TYPE}")
        self.log.debug(f" FROM TEST_DATA: {self.config.TEST_DATA}")

    # ------------------------------------------------------------------
    # Do anything extra for each test class
    # ------------------------------------------------------------------
    pass