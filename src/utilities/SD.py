import datetime
import logging
import os
import re
import time
from datetime import datetime
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
import requests

# Custom imports
# =====================
# import src.config as config
import src.config.config as config
from src.utilities.Logger import Logger
from src.utilities.utilities import Utilities
from src.utilities.jquery import jQuery


class SeleniumDriver:
    def __init__(self, driver):
        self.driver = driver
        self.timeout = config.TIMEOUT
        self.log = Logger().get_logger()

    def geturl(self, url):
        self.wait_for_page_loaded(url=url)

    def quit(self):
        self.quit()

    def script_wait(self, sleep_time=None):
        if sleep_time:
            time.sleep(sleep_time)
        else:
            time.sleep(self.timeout)

    # ----------------------------------------------------------------------
    # ---[ ELEMENT AND LOCATOR ]---
    # ----------------------------------------------------------------------
                
    def get_locator_and_strategy(self, locator):
        # Locator validation in case it directly starts with //
        if Utilities().find_text(locator, "^//.*\[.*\]"):
            self.log.critical(f"Something went wrong you might have missed ``xpath=`` before your locator --: {locator}")

        # separate the By type and locator
        strategy = locator[:locator.find("=")]
        locator = locator[locator.find("=") + 1:]

        # select the By strategy
        if strategy == "class":
            by = By.CLASS_NAME
        elif strategy == "css":
            by = By.CSS_SELECTOR
        elif strategy == "link":
            by = By.LINK_TEXT
        elif strategy == "name":
            by = By.NAME
        elif strategy == "xpath":
            by = By.XPATH
        elif strategy == "tagname":
            by = By.TAG_NAME
        elif strategy == "jquery":
            by = "jquery"
        else:
            by = By.ID

        # Return the By and the locator value
        return by, locator

    def find_element(self, locator_data, timeout=None, max_retry=2) -> any:
        # Set the timeout if not given
        if not timeout:
            timeout = self.timeout
        
        # Get the By and Locator value
        by, locator = self.get_locator_and_strategy(locator_data)

        # Get the wait object
        wait = WebDriverWait(self, timeout, ignored_exceptions=StaleElementReferenceException)

        # Re-Try approach
        retry_count = 0
        while retry_count <= max_retry:
            
            # Try to fetch element
            try:
                # Fetch
                element = wait.until(
                    lambda this: this.driver.find_element(by, locator), "Was unable to find the element with locator: %s" % locator)
                self.log.debug("Element found with locator: " + locator + " and find by type: " + by)
                
                # return the element
                return element
            except Exception as e:
                self.log.error("Element not found with locator: " + locator + " and find by type: " + by)
                if retry_count == max_retry:
                    self.log.error("[find_element_by_locator] Follwing error occured, Investigate !")
                    self.log.error(e)

            # Increase the retry count
            retry_count += 1
            self.log.debug("Retrying to find Element ... ")

        if retry_count > max_retry:
            self.log.debug(f"[SD] Max retry limit exausted ...")
        
        # Otherwise return None
        return None

    def find_element_when_visible(self, locator_data, timeout=None) -> any:
        # Set the timeout if not given
        if not timeout:
            timeout = self.timeout
        
        # Get the By and Locator value
        by, locator = self.get_locator_and_strategy(locator_data)

        # Get the wait object
        wait = WebDriverWait(self, timeout, ignored_exceptions=StaleElementReferenceException)

        # Try to fetch element
        try:
            # Fetch
            element = wait.until(
                        expected_conditions.visibility_of_element_located(by, locator), 
                        "Was unable to find the element with locator: %s" % locator
                    )
            self.log.debug("Element found with locator: " + locator + " and find by type: " + by)
            
            # return the element
            return element
        except Exception as e:
            self.log.error("Element not found with locator: " + locator + " and find by type: " + by)
            self.log.error("[find_element_by_locator] Follwing error occured, Investigate !")
            self.log.error(e)
            return None

    def find_element_when_present(self, locator_data, timeout=None) -> any:
        # Set the timeout if not given
        if not timeout:
            timeout = self.timeout
        
        # Get the By and Locator value
        by, locator = self.get_locator_and_strategy(locator_data)

        # Get the wait object
        wait = WebDriverWait(self, timeout, ignored_exceptions=StaleElementReferenceException)

        # Try to fetch element
        try:
            # Fetch
            element = wait.until(
                        expected_conditions.presence_of_element_located(by, locator), 
                        "Was unable to find the element with locator: %s" % locator
                    )
            self.log.debug("Element found with locator: " + locator + " and find by type: " + by)
            
            # return the element
            return element
        except Exception as e:
            self.log.error("Element not found with locator: " + locator + " and find by type: " + by)
            self.log.error("[find_element_by_locator] Follwing error occured, Investigate !")
            self.log.error(e)
            return None
        
    def find_element_when_clickable(self, locator_data, timeout=None) -> any:
        # Set the timeout if not given
        if not timeout:
            timeout = self.timeout
        
        # Get the By and Locator value
        by, locator = self.get_locator_and_strategy(locator_data)

        # Get the wait object
        wait = WebDriverWait(self, timeout, ignored_exceptions=StaleElementReferenceException)

        # Try to fetch element
        try:
            # Fetch
            element = wait.until(
                        expected_conditions.element_to_be_clickable(self.driver.find_element(by, locator)), 
                        "Was unable to find the element with locator: %s" % locator
                    )
            self.log.debug("Element found with locator: " + locator + " and find by type: " + by)
            
            # return the element
            return element
        except Exception as e:
            self.log.error("Element not found with locator: " + locator + " and find by type: " + by)
            self.log.error("[find_element_by_locator] Follwing error occured, Investigate !")
            self.log.error(e)
            return None

    def find_elements(self, locator_data, timeout=None, index=None):
        # Set the timeout if not given
        if not timeout:
            timeout = self.timeout
        
        # Get the By and Locator value
        by, locator = self.get_locator_and_strategy(locator_data)

        # Get the wait object
        wait = WebDriverWait(self, timeout, ignored_exceptions=StaleElementReferenceException)

        # Try to fetch element
        try:
            # fetch
            elements = wait.until(
                lambda self: self.driver.find_elements(by, locator), "Was unable to find the elements with locator: %s" % locator)
            self.log.debug("Element found with locator: " + locator + " and find by type: " + by)

            # If we have request for an element from specific index out of the list of elements
            if index:
                return elements[index]
            
            # return all the elements
            return elements
        except Exception as e:
            self.log.debug("Element not found with locator: " + locator + " and find by type: " + by)
            self.log.error("[SD] [find_elements_by_locator] Follwing error occured, Investigate !")
            self.log.error(e)
            return None

    # ----------------------------------------------------------------------
    # ---[ ELEMENT PROPERTIES ]---
    # ----------------------------------------------------------------------
    
    def get_attribute(self, locator, attribute_name, max_retry=2):
        self.log.debug("[SD] Trying to find element %s attribute: %s" % (locator, attribute_name))
        retry_count = 0
        attribute_value = None
        while retry_count <= max_retry:
            try:
                if retry_count > 0:
                    self.log.debug(f"[SD] Re-Trying to fetch Attibute: {attribute_name} ...")
                element = self.find_element_when_present(locator)
                attribute_value = element.get_attribute(attribute_name)
                self.log.debug("[SD] [Attibute:Value] : %s = %s" % (attribute_name, attribute_value))
                break
            except StaleElementReferenceException:
                self.log.debug("[SD] Stale Element Exception occured. Trying again after refreshing the page.")
                retry_count += 1
            except AttributeError:
                raise Exception(f"[SD] Attribute error occured. Attribute: {attribute_name} was NOT found for locator: {locator}.")
            except:
                raise Exception("[SD] Error occured while retrieving attribute.")
        
        # If max retry reached
        if retry_count > max_retry:
            self.log.debug(f"[SD] Max retry limit exausted ...")

        # Return the attribute value
        return attribute_value
    
    def get_text_of_element(self, locator, timeout=None):
        return self.find_elements(locator, timeout).text
    
    def get_text_of_elements(self, locator, timeout=None, index=None):
        return [ele.text for ele in self.find_elements(locator, timeout, index)]

    def get_striped_text_from_elements(self, locator) -> None:
        return [elem_txt.strip() for elem_txt in self.get_text_of_elements(locator)]
    
    # ----------------------------------------------------------------------
    # ---[ KEYBOARD OPERATIONS ]---
    # ----------------------------------------------------------------------
            
    def clear(self, locator) -> None:
        self.find_element(locator).clear()

    def delete_all_text(self, locator) -> None:
        self.log.debug("[SD] Clearing all text for 'Select All + DELETE' ...")
        to_clear = self.find_element(locator)
        if Utilities().is_mac():
            to_clear.send_keys(Keys.COMMAND + "a")
        else:
            to_clear.send_keys(Keys.CONTROL + "a")
        to_clear.send_keys(Keys.DELETE)

    def type(self, locator, text) -> None:
        self.log.debug("Keyboard Type: " + text)
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)

    def type_and_press_enter(self, locator, text) -> None:
        self.log.debug("webdriver.type_enter [%s]" % self.driver.current_url)
        element = self.find_element(locator)
        element.clear()
        if len(text) > 0:
            element.send_keys(text)
        element.send_keys(Keys.ENTER)

    def add_new_line_to_the_end(self, locator, new_line) -> None:
        self.log.debug("[SD][PAGE_URL : %s] Adding new line at the end... " % self.driver.current_url)
        element = self.find_element(locator)
        element.send_keys(Keys.CONTROL + Keys.END)
        element.send_keys(new_line)
        element.send_keys(Keys.ENTER)

    def press_enter(self, locator) -> None:
        self.log.debug("[SD][PAGE_URL : %s] Pressing ENTER key... " % self.driver.current_url)
        self.find_element(locator).send_keys(Keys.ENTER)

    def press_delete(self, locator) -> None:
        self.log.debug("[SD][PAGE_URL : %s] Pressing DELETE key... " % self.driver.current_url)
        self.find_element(locator).send_keys(Keys.DELETE)

    def type_and_press_esc(self, locator, text) -> None:
        self.log.debug("webdriver.type_enter [%s]" % self.driver.current_url)
        element = self.find_element(locator)
        element.clear()
        if len(text) > 0:
            element.send_keys(text)
        element.send_keys(Keys.ESCAPE)

    def press_up_key(self, locator) -> None:
        self.find_element(locator).send_keys(Keys.UP)

    def press_down_key(self, locator) -> None:
        self.find_element(locator).send_keys(Keys.DOWN)

    def press_end_key(self, locator) -> None:
        self.find_element(locator).clear()
        self.find_element(locator).send_keys(Keys.END)

    # ----------------------------------------------------------------------
    # ---[ MOUSE OPERATIONS ]---
    # ----------------------------------------------------------------------

    def click(self, locator) -> None:
        self.log.debug("[SD] Performing Click on locator [%s]" % (locator))
        self.find_element_when_clickable(locator).click()

    def toggle_check_box(self, locator, check_if_selected=False):
        # Just toggle if no check is asked
        if not check_if_selected:
            self.click(locator)
        # Otherwise
        else:
            # If it is not selected already then tick it.
            if not self.is_selected(locator):
                self.click(locator)

    # ----------------------------------------------------------------------
    # ---[ JAVASCRIPT EXECUTORS ]---
    # ----------------------------------------------------------------------
        
    def scroll_to(self, locator, scroll_width='0', scroll_height='10000'):
        self.log.debug("webdriver.scroll_to [{}]".format(self.driver.current_url))
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].scrollTo({},{});", element, scroll_width, scroll_height)

    def scroll_till_end(self, locator):
        self.log.debug("Scrolling till end on: [{}]".format(self.driver.current_url))
        self.find_element(locator).send_keys(Keys.END)

    def scroll_into_view(self, locator):
        self.log.debug("webdriver.scroll_into_view [%s] URL:[%s]" % (locator, self.driver.current_url))
        element = self.find_element(locator)
        self.driver.execute_script("return arguments[0].scrollIntoView()", element)

    def execute_script(self, cmd):
        return self.driver.execute_script(cmd)

    # ----------------------------------------------------------------------
    # ===[PAGE PERFORMANCE : TIME CALCULATIONS]=============================
    # ----------------------------------------------------------------------
    def is_there_any_pending_ajax_call_on_page(self):
        script = '''
                var pending_status = true;
                (function() {
                    var proxied = window.XMLHttpRequest.prototype.send;
                    window.XMLHttpRequest.prototype.send = function() {
                        var pointer = this;
                        var intervalId = window.setInterval(function(){
                                // set the pending status as true at this point 
                                pending_status = true;
                                
                                // If any ajax call is still pending
                                if(pointer.readyState != 4){
                                    console.log("--> Pending status:" + pending_status);
                                    return false;
                                }
                                
                                // set the pending status as false at this point
                                pending_status = false;
                                
                                // no pending ajax calls 
                                console.log("<-- Pending status:" + pending_status);
                                        
                                // then clear the interval for this time.
                                clearInterval(intervalId);
                                
                                // return some value for No pending ajax call left at this moment.
                                return pending_status;
                
                        }, 1);//I found a delay of 1ms to be sufficient, modify it as you need.
                        return proxied.apply(this, [].slice.call(arguments));
                    };
                })();
        '''
        return self.driver.execute_async_script(script)
        # return self.execute_script("return pending_status;")

    def calculate_page_load_timings(self, test_name: str = ""):
        # Use Navigation Timing API to calculate the timings
        navigation_start = self.driver.execute_script("return window.performance.timing.navigationStart")
        response_start = self.driver.execute_script("return window.performance.timing.responseStart")
        dom_complete = self.driver.execute_script("return window.performance.timing.domComplete")

        # now calculate the backend response time, and front-end page load time
        backend_performance_calc = response_start - navigation_start
        frontend_performance_calc = dom_complete - response_start

        # FOR Single Page Applications, calculate for the pending ajax call as well
        # TODO: Add some error in final page load time (~100 millis),
        #  as we were waiting to check for the pending ajax call
        #  even if it was not there any.
        # try continuously for 300 times, to see no further ajax call is made
        try_count = 300
        ajax_call_completion_time = 0
        while try_count > 0:
            # While any ajax call is pending
            print(f"AJAX PENDING: ===> {self.is_there_any_pending_ajax_call_on_page()}")
            # while self.is_there_any_pending_ajax_call_on_page():
            #     # start adding each millis under pending ajax calls
            #     ajax_call_completion_time += 1
            # reduce try count
            try_count -= 1
            # wait for 1 millis
            # time.sleep(0.001)

        # add this to config.page_performance_data, for reporting
        perf_data = {"test_name": test_name,
                     "page_title": self.driver.title,
                     "page_url": self.driver.current_url,
                     "frontend_page_load_time_in_millis": frontend_performance_calc + ajax_call_completion_time,
                     "backend_response_time_in_millis": backend_performance_calc
                     }
        config.PAGE_PERFORMANCE_DATA.append(perf_data)

        # return the timings (timings are in MilliSecs)
        return frontend_performance_calc, backend_performance_calc

    # ----------------------------------------------------------------------
    # ===[OTHER]============================================================
    # ----------------------------------------------------------------------
        
    def get_screenshot(self, filename=None):
        #
        # Very IMP -->
        # Needs Refactoring as Long name screenshots are not getting captured.
        #
        #
        temp_list = os.environ.get('PYTEST_CURRENT_TEST').split('::')
        test_script_name = temp_list[-2]
        test_func_name = temp_list[-1].split(' ')[0]
        print(f"From SD: {os.path.dirname(__file__)} \nCombined Path: {os.path.join(config.OUT_DIR_NAME, config.SCREENSHOT_DIR_NAME)}")
        # screenshot_dir_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "..", config.SCREENSHOT_DIR_NAME)
        screenshot_dir_path = os.path.join(config.OUT_DIR_NAME, config.SCREENSHOT_DIR_NAME)
        if not os.path.exists(screenshot_dir_path):
            os.mkdir(screenshot_dir_path)

        test_script_ss_dir_path = os.path.join(screenshot_dir_path, test_script_name)
        test_ss_dir_path = os.path.join(test_script_ss_dir_path, test_func_name)

        if not os.path.exists(test_script_ss_dir_path):
            os.mkdir(test_script_ss_dir_path)
        if not os.path.exists(test_ss_dir_path):
            os.mkdir(test_ss_dir_path)

        if filename is not None:
            screenshot_file_name = filename + '_' + datetime.now().strftime("%d-%m-%Y_%I-%M-%S_%p")
        else:
            screenshot_file_name = test_func_name + '_' + datetime.now().strftime("%d-%m-%Y_%I-%M-%S_%p")
        file_path = os.path.join(test_ss_dir_path, screenshot_file_name)
        self.log.info(f"taking screenshot as {screenshot_file_name}")
        self.driver.get_screenshot_as_file(file_path + ".png")
        return file_path + ".png"

    def get_element_offset(self, jquery_locator, timeout=config.TIMEOUT, index=0):
        by = self.get_locator_and_strategy(jquery_locator)

        if by != 'jquery':
            raise Exception('Must be jquery locator')

        locator = jquery_locator[jquery_locator.find("=") + 1:]

        wait = WebDriverWait(self.driver, timeout, ignored_exceptions=StaleElementReferenceException)

        locator_ = """return %s.map(function () {
                var t = window.jQuery(this);
                var ofs = t.offset();
                return [[ofs.left, ofs.top]];
            }).get(%s)""" % (jQuery(locator), str(index))
        return wait.until(lambda self: self.execute_script(locator_),
                          "Was unable to find the element: %s" % locator)

    def get_element_width(self, jquery_locator, timeout=config.TIMEOUT):
        by = self.get_locator_and_strategy(jquery_locator)

        if by != 'jquery':
            raise Exception('Must be jquery locator')

        locator = jquery_locator[jquery_locator.find("=") + 1:]

        wait = WebDriverWait(self.driver, timeout, ignored_exceptions=StaleElementReferenceException)

        locator_ = """return %s.map(function () {
                var t = window.jQuery(this);
                return t.width();
            }).get()""" % (jQuery(locator))
        return wait.until(lambda self: self.execute_script(locator_),
                          "Was unable to find the element: %s" % locator)

    def get_element_height(self, jquery_locator, timeout=config.TIMEOUT, index=0):
        by = self.get_locator_and_strategy(jquery_locator)

        if by != 'jquery':
            raise Exception('Must be jquery locator')

        locator = jquery_locator[jquery_locator.find("=") + 1:]

        wait = WebDriverWait(self.driver, timeout, ignored_exceptions=StaleElementReferenceException)

        locator_ = """return %s.map(function () {
                var t = window.jQuery(this);
                return t.height();
            }).get(%s)""" % (jQuery(locator), str(index))
        return wait.until(lambda self: self.execute_script(locator_),
                          "Was unable to find the element: %s" % locator)

    def get_elements_id_and_text(self, locator, timeout=config.TIMEOUT):
        by, locator = self.get_locator_and_strategy(locator)
        locator = locator[locator.find("=") + 1:]

        wait = WebDriverWait(self.driver, timeout, ignored_exceptions=StaleElementReferenceException)

        if by == "jquery":
            locator_ = """return %s.map(function () {
                return {'id':this.getAttribute('id'), 'text':jQuery(this).text()};
            }).get();""" % (jQuery(locator))
            return wait.until(lambda self: self.execute_script(locator_),
                              "Was unable to find the element: %s" % locator)
        else:
            return wait.until(lambda self: self.find_element(by, locator),
                              "Was unable to find the element: %s" % locator)

    def get_elements_id(self, locator, timeout=config.TIMEOUT):
        by, locator = self.get_locator_and_strategy(locator)
        locator = locator[locator.find("=") + 1:]

        wait = WebDriverWait(self.driver, timeout, ignored_exceptions=StaleElementReferenceException)

        if by == "jquery":
            locator_ = """return %s.map(function () {
                return this.getAttribute('id');
            }).get();""" % (jQuery(locator))
            return wait.until(lambda self: self.execute_script(locator_),
                              "Was unable to find the element: %s" % locator)
        else:
            return wait.until(lambda self: self.find_element(by, locator),
                              "Was unable to find the element: %s" % locator)

    def find_element_by_type_and_text(self, type, text):
        locator = "jquery=%s:contains('%s')" % (type, text)
        return self.find_element(locator)

    def click_link_by_text(self, text):
        elem = self.find_element_by_type_and_text("a", text)
        elem.click()

    def inject_jquery(self):
        # Read jquery libraries from local file. Not used for now but might need later
        with open(config.JQUERY_LIB_PATH, 'r') as jquery_lib:
            jquery = jquery_lib.read()
        # Activate jquery libraries
        self.execute_script(jquery)

    
    # def _click_onlocator(self, locator, timeout, TryCount):
    #     Status = False
    #     try:
    #         loc = locator[locator.find("=") + 1:]
    #         by = self.get_locator_strategy(locator)
    #         ele = WebDriverWait(self.driver, timeout).until(expected_conditions.element_to_be_clickable((by, loc)))
    #         ele.click()
    #         Status = True
    #     except StaleElementReferenceException:
    #         self.log.debug("Stale Element Exception occured. Trying again.")
    #     except:
    #         if TryCount == 1:
    #             self.log.error("ERROR: ", exc_info=True)
    #     return Status
    #
    # def click(self, locator, timeout=config.TIMEOUT, _try_count=3):
    #     self.log.debug("Performing Click on locator [%s]" % (locator))
    #     if self.is_element_exist(locator):
    #         for i in range(_try_count):
    #             if self._click_onlocator(locator, timeout, _try_count - i):
    #                 return None
    #         raise Exception("Click Failed. element found but some error occured.")
    #     raise Exception("Click Failed. Either element not visible or some error occured.")

    

    
    def get_value_of_css_property(self, locator, style):
        return self.find_element(locator).value_of_css_property(style)

    def is_element_text_bold(self, locator):
        weight = self.get_value_of_css_property(locator, 'font-weight')
        self.log.info(f"element value is {weight}")
        if int(weight) >= 700:
            return True
        return False

    def ctrl_click(self, locator, timeout=config.TIMEOUT):
        element = self.find_element(locator, timeout=timeout)
        ActionChains(self.driver).key_down(Keys.ALT).click(element).key_up(Keys.ALT).perform()
        return None

    def is_english_version(self):
        time.sleep(2)
        return self.get_text("help_dropdown_link") == "Help"

    def is_japanese_version(self):
        time.sleep(2)
        return self.get_text("help_dropdown_link") == "ヘルプ"

    def get_translated_text(self, text):
        if self.is_japanese_version():
            return self.translate_en_to_jp(text)
        elif self.is_english_version():
            return self.translate_jp_to_en(text)
        self.log.error("Language not detected please check help menu on dashboard")
        return None

    def click_js(self, locator):
        self.log.debug("webdriver.click_js [{}]".format(self.driver.current_url))
        by, locator = self.get_locator_and_strategy(locator)
        _locator = locator[locator.find("=") + 1:]

        if by == "jquery":
            self.driver.execute_script("{}.click()".format(jQuery(_locator)))
        elif by == By.ID:
            self.driver.execute_script("{}.click()".format(jQuery("[id='{}']".format(_locator))))
        else:
            element = self.find_element(locator)
            self.driver.execute_script("arguments[0].click();", element);

    def click_at(self, locator, xoffset, yoffset):
        self.log.debug("webdriver.click_at [%s]" % self.driver.current_url)
        mouse = ActionChains(self.driver)
        mouse.move_to_element_with_offset(self.find_element(locator), int(xoffset),
                                          int(yoffset)).click_and_hold().release()
        mouse.perform()

    def click_action(self, locator):
        self.log.debug("Performing Action Chains click at: " + locator)
        mouse = ActionChains(self.driver)
        mouse.click(self.find_element(locator))
        mouse.perform()

    def down_action(self):
        action = ActionChains(self.driver)
        action.send_keys(Keys.ARROW_DOWN).perform()

    def page_down_action(self):
        action = ActionChains(self.driver)
        action.send_keys(Keys.PAGE_DOWN).perform()

    # def page_up_action(self):
    #     action = ActionChains(self.driver)
    #     action.send_keys(Keys.PAGE_UP).perform()

    def enter_action(self):
        action = ActionChains(self.driver)
        action.send_keys(Keys.ENTER).perform()

    def ctrl_click(self, locator):
        self.log.debug("webdriver.ctrl_click [%s]" % self.driver.current_url)
        action = ActionChains(self.driver)
        action.key_down(Keys.CONTROL).move_to_element(self.find_element(locator)).click().key_up(
            Keys.CONTROL)
        action.perform()

    def context_click(self, locator):
        self.log.debug("webdriver.context_click [%s]" % self.driver.current_url)
        mouse = ActionChains(self.driver)
        mouse.context_click(self.find_element(locator)).perform()

    def context_click_elements(self, locator):
        self.log.debug("webdriver.context_click [%s]" % self.driver.current_url)
        mouse = ActionChains(self.driver)
        for ele in self.find_elements(locator):
            mouse.context_click(ele).perform()
            yield

    def mouse_move(self, locator):
        self.log.debug("webdriver.mouse_move [%s]" % self.driver.current_url)
        mouse = ActionChains(self.driver)
        mouse.move_to_element(self.find_element(locator))
        mouse.perform()

    def mouse_down(self, locator):
        self.log.debug("webdriver.mouse_down [%s]" % self.driver.current_url)
        mouse = ActionChains(self.driver)
        mouse.click(self.find_element(locator))
        mouse.perform()

    def mouse_move_at(self, locator, xoffset, yoffset, index=0):
        self.log.debug("webdriver.mouse_move_at [%s]" % self.driver.current_url)
        mouse = ActionChains(self.driver)
        mouse.move_to_element_with_offset(self.find_element(locator, index), int(xoffset), int(yoffset))
        mouse.perform()

    def rotate_element_to(self, selector, degrees):
        self.execute_script("$(\"" + selector + "\").css({transform: 'rotate(" + degrees +
                            "deg)', '-moz-transform': 'rotate(" + degrees + "deg)'})")

    def drag_and_drop(self, source_locator, target_locator):
        self.log.debug("webdriver.drag_and_drop [%s]" % self.driver.current_url)
        mouse = ActionChains(self.driver)
        mouse.click_and_hold(self.find_element(source_locator))
        mouse.perform()

        time.sleep(1)

        mouse = ActionChains(self.driver)
        mouse.release(self.find_element(target_locator))
        mouse.perform()

    def drag_and_drop_at(self, source_locator, source_xoffset, source_yoffset, target_locator, target_xoffset,
                         target_yoffset):
        self.log.debug("webdriver.drag_and_drop_at [%s]" % self.driver.current_url)
        mouse = ActionChains(self.driver)
        mouse.move_to_element_with_offset(self.find_element(source_locator), int(source_xoffset),
                                          int(source_yoffset)).click_and_hold()
        mouse.perform()

        mouse = ActionChains(self.driver)
        mouse.move_to_element_with_offset(self.find_element(target_locator), int(target_xoffset),
                                          int(target_yoffset)).release()
        mouse.perform()
        self.wait_for_loading_popup()

    def drag_and_drop_by_offset(self, locator, x_offset, y_offset):
        self.log.debug("webdriver.drag_and_drop_by_offset [%s]" % self.driver.current_url)
        mouse = ActionChains(self.driver)
        mouse.drag_and_drop_by_offset(self.find_element(locator), x_offset, y_offset)
        mouse.perform()

    # TILL HERE <<<<<<
        
    def tab(self, locator):
        self.log.debug("webdriver.tab [%s]" % self.driver.current_url)
        self.find_element(locator).send_keys(Keys.TAB)

    def select(self, locator, value):
        self.log.debug("webdriver.select [%s]" % self.driver.current_url)
        Select(self.find_element(locator)).select_by_value(value)

    def select_by_text(self, locator, text):
        self.log.debug("webdriver.select_by_text [%s]" % self.driver.current_url)
        Select(self.find_element(locator)).select_by_visible_text(text)

    def select_by_value(self, locator, value):
        self.log.debug("webdriver.select_by_text [%s]" % self.driver.current_url)
        Select(self.find_element(locator)).select_by_value(value)

    def select_by_index(self, locator, index):
        self.log.debug("webdriver.select_by_index [%s]" % self.driver.current_url)
        Select(self.find_element(locator)).select_by_index(index)

    def is_selected(self, locator):
        self.log.debug("webdriver.is_selected [%s]" % self.driver.current_url)
        return self.find_element(locator).is_selected()

    def select_get_values(self, locator):
        self.log.debug("webdriver.select_by_text [%s]" % self.driver.current_url)
        return Select(self.find_element(locator)).options

    def is_element_focused(self, element_id):
        locator = jQuery("*[id='" + element_id + "']")
        script = "return %s.is(':focus')" % locator
        return self.execute_script(script)

    def get_text(self, locator):
        self.log.debug("webdriver.get_text [%s]" % locator)
        tryAgain = 0
        success = 0
        text = None
        while tryAgain <= 2:
            if tryAgain <= 1 and success == 0:
                try:
                    loc = locator[locator.find("=") + 1:]
                    by, locator = self.get_locator_and_strategy(locator)
                    ele = WebDriverWait(self.driver, config.TIMEOUT).until(
                        expected_conditions.presence_of_element_located((by, loc)))
                    text = ele.text
                    success = 1
                    break
                except StaleElementReferenceException:
                    self.log.debug("Stale Element Exception occured. Trying again after refreshing the page.")
                    tryAgain += 1
                except AttributeError:
                    raise Exception(f"Attribute error occured. {locator} was NOT found to return text.")
                except:
                    raise Exception("Error occured while retrieving text.")
        return text

    def get_value(self, locator):
        self.log.debug("webdriver.get_value [%s]" % self.driver.current_url)
        return self.get_attribute(locator, 'value')

    

    def is_radio_btn_checked(self, locator):
        self.log.debug("webdriver.get_attribute [%s]" % self.driver.current_url)
        try:
            attribute = self.find_element(locator).get_attribute("checked")
        except StaleElementReferenceException:
            pass
        finally:
            return True if attribute is not None else False

    def get_alert_text_and_accept(self):
        # self.log caused issues in some tests so it's been commented out
        # self.log.debug("webdriver.get_alert_text [%s]" % self.driver.current_url)
        # Hangup 3 seconds for the server's reponse
        self.log.info("Accept alert button")
        time.sleep(3)
        alert = Alert(self.driver)
        text = alert.text
        alert.accept()
        return text

    def close_alert_if_present(self):
        try:
            self.get_alert_text_and_accept()
        except NoAlertPresentException:
            pass

    def print_js_variable(self, variable):
        if self.execute_script("return window.%s === undefined" % variable):
            self.log.debug("variable %s is not defined" % variable)
        else:
            self.log.debug("variable %s is %s" % (variable, self.execute_script("return window.%s" % variable)))

    def get_js_variable_raw(self, variable):
        return self.execute_script("return window.%s" % variable)

    def get_js_variable(self, variable, timeout=config.TIMEOUT):
        self.log.debug("webdriver.get_js_variable [%s]" % self.driver.current_url)
        wait = WebDriverWait(self.driver, timeout)
        wait.until(lambda self: not self.execute_script("return window.%s === undefined" % variable),
                   "The variable '%s' is undefined." % variable)
        value = self.execute_script("return window.%s === true" % variable)
        self.log.debug("webdriver.get_js_variable: %s = %s" % (variable, value))
        return value

    def is_js_variable_undefined(self, variable):
        self.log.debug("webdriver.is_js_variable_undefined [%s]" % self.driver.current_url)
        value = self.execute_script("return window.%s === undefined" % variable)
        self.log.debug("webdriver.is_js_variable_undefined: %s -> %s" % (variable, value))
        return value

    def set_js_variable(self, variable, value):
        self.log.debug(f"Setting variable: {variable} to value: {value}")
        self.execute_script("window.%s = %s" % (variable, value))

    def set_js_attribute_of_element(self,locator, attribute, value):
            self.log.debug(f"Setting HTML attribute: {attribute} to value: {value}")
            webele = self.find_element(locator)
            self.driver.execute_script("arguments[0].setAttribute(arguments[1],arguments[2])",webele, attribute, value);

    def wait_for_js_variable_false(self, variable, timeout=config.TIMEOUT):
        try:
            self.log.debug("webdriver.wait_for_js_variable_false [%s]" % self.driver.current_url)
            wait = WebDriverWait(self.driver, timeout)
            wait.until(lambda self: self.execute_script("return window.%s === false" % variable),
                       "The variable '%s' isn't false." % variable)
        except TimeoutException as e:
            self.print_js_variable(variable)
            raise e
        except UnexpectedAlertPresentException as e:
            self.wait_for_alert_present()
            alert = self.switch_to.alert()
            alert.dismiss()
            raise e

    def wait_for_js_variable_true(self, variable, timeout=config.TIMEOUT):
        self.log.debug("webdriver.wait_for_js_variable_true [%s]" % self.driver.current_url)
        wait = WebDriverWait(self.driver, timeout)
        wait.until(lambda self: self.execute_script("return window.%s === true" % variable),
                   "The variable '%s' isn't true." % variable)

    def wait_for_js_variable_not_null(self, variable, timeout=config.TIMEOUT):
        self.log.debug("webdriver.wait_for_js_variable_not_null [%s]" % self.driver.current_url)
        wait = WebDriverWait(self.driver, timeout)
        wait.until(lambda self: self.execute_script("return window.%s != null" % variable),
                   "The variable '%s' is null or undefined." % variable)

    def wait_for_element_not_present(self, locator, timeout=config.TIMEOUT):
        self.log.debug("webdriver.wait_for_element_not_present [%s]" % self.driver.current_url)
        by, locator = self.get_locator_and_strategy(locator)
        locator = locator[locator.find("=") + 1:]

        wait = WebDriverWait(self.driver, timeout, ignored_exceptions=StaleElementReferenceException)

        if by == "jquery":
            return wait.until_not(lambda self: self.execute_script("return %s[0]" % jQuery(locator)),
                                  "Expected element: %s is NOT present" % locator)
        else:
            return wait.until_not(lambda self: self.find_element(by, locator),
                                  "Expected element: %s is NOT present" % locator)

    def wait_for_element_clickable(self, locator, timeout=config.TIMEOUT):
        loc = locator[locator.find("=") + 1:]
        by, locator = self.get_locator_and_strategy(locator)
        # self.log.debug("webdriver.wait_for_element_clickable [%s] [%s]" % (locator, self.driver.current_url))
        return WebDriverWait(self.driver, timeout).until(expected_conditions.element_to_be_clickable((by, loc)))

    def wait_for_element_visible(self, locator, timeout=config.TIMEOUT):
        self.log.debug("webdriver.wait_for_element_visible [%s] [%s]" % (locator, self.driver.current_url))
        wait = WebDriverWait(self.driver, timeout, ignored_exceptions=StaleElementReferenceException)
        element = self.find_element(locator, timeout)
        wait.until(lambda self: element.is_displayed(), "The element wasn't visible: %s" % locator)

    def wait_for_element_enabled(self, locator, timeout=config.TIMEOUT):
        self.log.debug("webdriver.wait_for_element_enabled [%s] [%s]" % (locator, self.driver.current_url))
        wait = WebDriverWait(self.driver, timeout)
        element = self.find_element(locator, timeout)
        self.log.debug("Is [%s] enabled? [%s]" % (locator, element.is_enabled()))
        wait.until(lambda self: element.is_enabled(), "The element wasn't enabled: %s" % locator)

    def wait_for_alert_present(self, timeout=config.TIMEOUT):
        self.log.debug("webdriver.wait_for_alert_visible")
        wait = WebDriverWait(self.driver, timeout, ignored_exceptions=StaleElementReferenceException)
        try:
            wait.until(expected_conditions.alert_is_present(), "Expected 'Alert' dialog present")
            return True
        except TimeoutException:
            return False

    def is_visible(self, locator, timeout=config.TIMEOUT):
        self.log.debug("webdriver.is_visible Element:[%s]" % (locator))
        try:
            wait = WebDriverWait(self, timeout, ignored_exceptions=StaleElementReferenceException)
            wait.until(lambda self: self.find_element_by_locator(locator, timeout).is_displayed())
            return True
        except (TimeoutException, AttributeError):
            return False

    def is_invisible(self, locator, timeout=config.TIMEOUT):
        loc = locator[locator.find("=") + 1:]
        by, locator = self.get_locator_and_strategy(locator)
        try:
            WebDriverWait(self.driver, timeout).until(expected_conditions.invisibility_of_element((by, loc)))
            self.log.debug("Object with locator: %s and type: %s doesn't exist." % (loc, by))
            return True
        except TimeoutException:
            return False

    def is_enabled(self, locator):
        self.log.debug("webdriver.is_enabled [%s] [%s]" % (self.driver.current_url, locator))
        ENABLED_TIMEOUT = 3
        try:
            wait = WebDriverWait(self, ENABLED_TIMEOUT, ignored_exceptions=StaleElementReferenceException)
            wait.until(lambda self: self.find_element_by_locator(locator, ENABLED_TIMEOUT).is_enabled())
            return True
        except TimeoutException:
            return False

    def wait_for_element_not_visible(self, locator, timeout=config.TIMEOUT):
        self.log.debug("webdriver.wait_for_element_not_visible [%s]" % self.driver.current_url)
        try:
            wait = WebDriverWait(self.driver, timeout, ignored_exceptions=StaleElementReferenceException)
            wait.until(lambda self: not self.find_element_by_locator(locator, timeout).is_displayed(),
                       "The element was still visible: %s" % locator)
        except TimeoutException:
            pass

    def wait_for_text_present(self, locator, text):
        self.log.debug("webdriver.wait_for_text_present [%s]" % self.driver.current_url)
        wait = WebDriverWait(self.driver, config.TIMEOUT, ignored_exceptions=StaleElementReferenceException)
        wait.until(lambda self: self.find_element_by_locator(locator).text.find(text) != -1,
                   "Was unable to find the text: %s" % locator)

    def select_from_hover_drop_down(self, locator, selection_locator):
        self.mouse_move(locator)
        self.find_element(selection_locator)
        self.click_js(selection_locator)
        self.mouse_move_at(locator, -5, -5)  # move mouse out so that view selector gets hidden

    def wait_for_attribute(self, locator, attribute_name, attribute_value):
        wait = WebDriverWait(self.driver, config.TIMEOUT)
        attribute_has_value = AttributeHasValue(locator, attribute_name, attribute_value)
        wait.until(lambda self: self.find_element_by_locator(attribute_has_value.locator),
                   "Was unable to find the element with the attribute: %s" % attribute_name + ": " + attribute_value)

    def wait_for_page_loaded(self, url=None):
        try:
            if url is None:
                url = self.driver.current_url
            self.driver.get(url)
            WebDriverWait(self.driver, 30).until(
                lambda self: self.execute_script("return document.readyState") == "complete",
                "Page wasn't completely loaded.")
        except WebDriverException:
            pass

    # TODO: Refactor with 'does_element_exist'
    def is_element_exist(self, locator, timeout=config.TIMEOUT):
        # element = self.find_element_by_locator(locator)
        loc = locator[locator.find("=") + 1:]
        by, locator = self.get_locator_and_strategy(locator)
        try:
            WebDriverWait(self.driver, timeout).until(expected_conditions.presence_of_element_located((by, loc)))
            self.log.debug("Object with locator: %s and type: %s exists." % (loc, by))
            return True
        except TimeoutException:
            self.log.debug("Object with locator: %s and type: %s doesn't exist." % (loc, by))
            return False

    def get_location_of_element(self, locator):
        _Dict = self.find_element(locator).location
        self.log.info(f"element location available at {_Dict}")
        return _Dict['x'], _Dict['y']

    def Set_window_size(self, x, y):
        self.driver.set_window_size(x, y)

    def refresh_page(self):
        self.driver.refresh()

    def get_window_title(self):
        self.log.debug("Window Title returned as: " + self.driver.title)
        return self.driver.title

    def get_all_windows(self):
        return self.driver.window_handles

    def close_current_window(self):
        self.driver.close()
        return self

    def close_browser_tab_by_index(self, index=0):
        self.driver.switch_to.window(self.driver.window_handles[index])
        open_windows = self.driver.window_handles
        self.log.debug("Closing browser tab with index=: " + index + ". Total windows open: " + len(open_windows))
        for i in range(len(open_windows)):
            self.driver.switch_to.window(open_windows[i])
            if i == index:
                self.driver.close()
                break
        remaining_tabs = self.driver.window_handles
        remaining_total_windows = len(remaining_tabs)
        if remaining_total_windows == len(open_windows):
            self.log.error("Browser didn't had " + index + "'th tab.")
        return self

    def switch_browser_tab_by_index(self, index=0):
        self.driver.switch_to.window(self.driver.window_handles[index])
        return self

    def switch_to_last_opened_browser_tab(self):
        self.driver.switch_to.window(self.driver.window_handles[-1])
        return self

    def close_window_with_title(self, winTitle):
        openWindows = self.driver.window_handles
        totalWindows = len(openWindows)
        self.log.debug("Closing window with title: " + winTitle + ". Total windows open: " + str(totalWindows))
        for i in range(totalWindows):
            self.driver.switch_to.window(openWindows[i])
            if self.get_window_title() == winTitle:
                self.driver.close()
                break
        remainingOpenWindows = self.driver.window_handles
        remainingtotalWindows = len(remainingOpenWindows)
        if remainingtotalWindows == totalWindows:
            self.log.error("Window with title: " + winTitle + " not found.")
        return self

    def switch_to_window(self, winTitle):
        openWindows = self.driver.window_handles
        totalWindows = len(openWindows)
        self.log.debug("Switching to window with title: " + winTitle + ". Total windows open: " + str(totalWindows))
        for i in range(totalWindows):
            self.driver.switch_to.window(openWindows[i])
            if self.get_window_title() == winTitle:
                break
        return self

    def is_window_title_present(self, wintitle, wait_time=2):
        self.wait(wait_time)
        openWindows = self.driver.window_handles
        totalWindows = len(openWindows)
        present = False
        self.log.debug("Checking window with title: \"" + wintitle + "\" is present or not.")
        for i in range(totalWindows):
            self.driver.switch_to.window(openWindows[i])
            if self.get_window_title() == wintitle:
                present = True
                break
        return present

    def get_current_window(self):
        # return the window opener
        return self.driver.current_window_handle

    def get_current_url(self):
        return self.driver.current_url

    def download_image(self, locator, saveas="", name="image.jpg"):
        self.find_elements(locator)
        data = requests.get(self.get_attribute(locator, 'src'))
        saveas = self.GetPath(saveas, name)
        with open(saveas, 'wb') as f:
            f.write(data.content)
        return self.abs_path(saveas)

    def abs_path(self, File):
        return os.path.abspath(File)

    def send_home_key(self):
        action = ActionChains(self.driver)
        action.send_keys(Keys.HOME).perform()


class AttributeHasValue:
    def __init__(self, locator, attribute_name, attribute_value):
        self.locator = locator
        self.attribute_name = attribute_name
        self.attribute_value = attribute_value

    def __call__(self, driver):
        element = driver.find_element_by_id(self.locator)
        if self.attribute_value in element.get_attribute(self.attribute_name):
            return self.locator
        else:
            return False
