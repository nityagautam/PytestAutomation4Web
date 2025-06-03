"""
@author: Ashutosh Mishra | ashutosh_mishra_@outlook.com
@created: 1 Sep 2022
@last_modified: 03 Jun 2025
@desc: Locators for the Page Object Classes;
    Contains Locators for the Page Object classes.
"""

ALL_LOCATORS = {

    # -----------------------------------------------------------------------------------------------------------
    # Each entry demote the Page object class, with its name
    # -----------------------------------------------------------------------------------------------------------
    "DEMO_PAGE_CLASS_NAME": {
        "PAGE_CLASS_ELEMENT_1": "<LOCATOR_TYPE>=<LOCATOR_VALUE>",
        "PAGE_SUBMIT_BTN_1": "xpath=//*[@role='button' and @type='submit']",
        "PAGE_SUBMIT_BTN_2": "id=submit_btn",
        "PAGE_SUBMIT_BTN_3": "name=submit_btn",
        "PAGE_SUBMIT_BTN_4": "css=.btn > submit",
        "PAGE_SUBMIT_BTN_5": "class=submit_btn_class",
        "PAGE_SUBMIT_BTN_6": "link=submit_btn_link",
    },

    # -----------------------------------------------------------------------------------------------------------
    # ANOTHER SAMPLE PAGE CLASS
    # -----------------------------------------------------------------------------------------------------------
    'SAMPLE':{
        "IDENTIFIER_NAME_FOR_ELEMENT": "xpath=<VALID_XPATH_VALUE_GOES_HERE>",
        "IDENTIFIER_NAME_FOR_ELEMENT": "ELEMENT_ID_VALUE_GOES_HERE",
        "EXAMPLE1_ELEMENT_WITH_XPATH": "xpath=//td[@title='{}']",
        "EXAMPLE2_ELEMENT_WITH_ID": "btn1"
    },

    # -----------------------------------------------------------------------------------------------------------
    # Start adding yours below this line [You may refer above demo/sample]
    # -----------------------------------------------------------------------------------------------------------
    
    # -----------------------------------------------------------------------------------------------------------
    # Locators for WikiSearch Page Class
    # -----------------------------------------------------------------------------------------------------------
    "GoogleSearchPage": {
        "SEARCH_BOX": "xpath=//input[@name='q']",
        "SEARCH_SUBMIT_BTN": "xpath=//*[@name='btnK' and @type='submit']",
        "SEARCH_RESULT_FIRST_LINK": "xpath=(//*[@id='rso']//a)[1]",
    },

    # -----------------------------------------------------------------------------------------------------------
    # Locators for WikiSearch Page Class
    # -----------------------------------------------------------------------------------------------------------
    'WikiSearch':{
        "SEARCH_INPUT_ID": "searchInput",
        "SEARCH_BTN": "xpath=//button[@type='submit']"
    }
}
