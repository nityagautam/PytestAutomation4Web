"""
@package utilities
=================================================================
@author: Ashutosh Mishra | ashutosh_mishra_@outlook.com
@created: 1 Sep 2020
@last_modified: 11 Jan 2025
@desc: WebDriverEngine Class;
    returns the driver web instance based on browser name.
    Example:
            wde = WebDriverEngine(browser_name)
            driver = wde.install_and_get_web_driver()
=================================================================
"""

# core imports
# =====================
import os

# WEB-DRIVER imports
# =====================
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.ie.service import Service as IEService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.microsoft import IEDriverManager
from selenium.webdriver.chrome.options import Options

# Custom imports
# =====================
from src.utilities.Logger import Logger
from src.utilities.utilities import Utilities


class WebDriverFactory(Utilities):

    def __init__(self, browser_name, url_address=None):
        """
        Initiates WebDriverFactory class

        Returns:
            None
        """
        self.supported_browser_names = ["firefox", "chrome", "edge", "ie"]
        self.hub = url_address
        self.browser = browser_name
        self.driver = None
        self.options = None
        self.log = Logger().get_logger()

    def is_browser_name_supported(self):
        # Check
        print(f"Given Browser is: {self.browser}\n\n")
        if self.browser.lower() in self.supported_browser_names:
            return True
        else:
            return False

    def install_and_get_web_driver(self):
        """
        Download and install from the internet and setup the webdriver.

        @param browser_name:
        @return:
        """
        # Using selenium 4
        # ------------------

        # Get based on browser type
        self.log.info(f"Starting browser: {self.browser}")
        
        # Sanity Check for the browser name
        if self.is_browser_name_supported():
            try:
                if self.browser == 'chrome':
                    self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
                elif self.browser == 'firefox':
                    self.driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
                elif self.browser == 'ie':
                    self.driver = webdriver.Ie(service=IEService(IEDriverManager().install()))
                elif self.browser == 'edge':
                    self.driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))
            except Exception as e:
                self.log.error(e)
            finally:
                self.log.info("[LOG] web-driver retrival process completed.")

            # return web driver
            return self.driver
        else:
            self.log.error(f"[WD] Seems like you have provided the unsupported browser: {self.browser}."
                           "Supported browsers are: {self.supported_browser_names}")
            return False

    def get_web_driver_instance(self):
        """
        TODO: Setup/ Re-write the code for optimization.
        Get WebDriver Instance from the local binaries based on the browser configuration

        Returns:
            'WebDriver Instance'
            @return:
        """

        self.log.info("Starting browser: " + self.browser)
        
        if self.is_linux():
            version = self.get_chrom_driver_version_linux()
            chromedriver_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "drivers", "chromedriver", "linux")
            if self.file_folder_validation(self.GetPath(chromedriver_path, f"chromedriver{version}")):
                chromedriver_path = self.GetPath(chromedriver_path, f"chromedriver{version}")
            else:
                chromedriver_path = self.GetPath(chromedriver_path, "chromedriver")

        if self.is_windows():
            version = self.get_chrom_driver_version_windows()
            chromedriver_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                             "drivers", "chromedriver", "win")
            if self.file_folder_validation(self.GetPath(chromedriver_path, f"chromedriver{version}.exe")):
                chromedriver_path = self.GetPath(chromedriver_path, f"chromedriver{version}.exe")
            else:
                chromedriver_path = self.GetPath(chromedriver_path, "chromedriver.exe")

        if self.browser == "ie":
            driver = webdriver.Ie(
                executable_path=os.path.join(os.path.dirname(os.path.dirname(__file__)), "drivers", "iedriver",
                                             "IEDriverServer.exe"))
        # Local Firefox
        elif self.browser == "firefox":
            version = self.get_firefox_driver_version()
            geckodriver_path = self.GetPath_new(self.get_utilities_folder(), "drivers", "geckodriver")
            if self.is_linux():
                geckodriver_path = self.GetPath_new(geckodriver_path, "linux", "geckodriver")
                __Temp_path = f"{geckodriver_path}{version}"
                geckodriver_path = __Temp_path if self.file_folder_validation(__Temp_path) else geckodriver_path

            if self.is_windows():
                geckodriver_path = self.GetPath_new(geckodriver_path, "win", "geckodriver")

                __Temp_path = f"{geckodriver_path}{version}.exe"
                geckodriver_path = __Temp_path if self.file_folder_validation(__Temp_path) else f"{geckodriver_path}.exe"

            driver = webdriver.Firefox(executable_path=geckodriver_path)

        # Local Chrome
        elif self.browser == "chrome":
            # Set chrome driver
            self.options = Options()
            self.options.add_argument("--disable-features=VizDisplayCompositor")
            self.options.add_argument("--no-sandbox")
            self.options.add_argument("--disable-dev-shm-usage")
            self.options.add_experimental_option("useAutomationExtension", False)
            self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
            self.options.add_experimental_option("excludeSwitches", ["enable-logging"])
            self.options.add_experimental_option('prefs', {
                'credentials_enable_service': False,
                'profile': {
                    'password_manager_enabled': False
                },
                'safebrowsing.enabled': True,

            })

            driver = webdriver.Chrome(executable_path=chromedriver_path, options=self.options)

        # remote webdriver setup; #TODO SETUP
        elif "remote" in self.browser:
            self.log.info("Hub Address: " + self.hub)
            conf = self.browser.split(".")
            platformName = conf[1]
            browserName = conf[2]
            desiredCapabilities = \
                {
                    "browserName": browserName,
                    'javascriptEnabled': True,
                    'platformName': platformName
                }

            driver = webdriver.Remote(command_executor = self.hub + '/wd/hub',
                                      desired_capabilities=desiredCapabilities)
        else:
            raise Exception(
                "Please enter valid browser name (chrome, firefox, ie)."
                "If trying to execute on remote, enter in remote.platform.browser format.")
        
        # Maximize the window
        # driver.maximize_window()
        
        # Loading browser with App URL
        # driver.get(self.url)

        # Return the web driver
        return driver
