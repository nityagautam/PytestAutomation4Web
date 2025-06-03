
# =====================================================================================
# This class is to take the performance dict and generate an HTML report for the same.
# =====================================================================================
import json
import os
from src.config import config
from src.utilities.utilities import Utilities


class GeneratePagePerformanceReport:
    def __init__(self):
        # Prepare the report path
        self.raw_report_file_path = os.path.join(config.OUT_DIR_NAME, config.REPORT_DIR_NAME, config.PERFORMANCE_RAW_REPORT_FILE_NAME)
        self.performance_report_path = os.path.join(config.OUT_DIR_NAME, config.REPORT_DIR_NAME, config.PERFORMANCE_REPORT_FILE_NAME)

        # We are expecting some data from config.page_performance_data (list type variable)
        self.data = {
            "author": config.AUTHOR_NAME,
            "report_title": config.PERFORMANCE_REPORT_TITLE,
            "page_performance_data": config.PAGE_PERFORMANCE_DATA
        }

        # Start processing
        self.__run__()

    def __run__(self):
        # TODO: try/catch

        # Generate the raw performance report as json right away with current data.
        Utilities().create_file(self.raw_report_file_path, json.dumps(self.data, indent=8, sort_keys=True))

        # Start processing for HTML report
        for entry in self.data:
            print(f"[PAGE PERFORMANCE ENTRY]====> {entry}")

    def __report_template(self):
        output = ""
        report_style = ""
        a = 0
        head = f'''
                <head>
                    <meta charset="utf-8"/>
                    <title id="head-title"> {config.PERFORMANCE_REPORT_TITLE} </title>
                    <style type="text/css"> 
                        {report_style}
                    </style>
                </head>
        '''
        html_report_template = f'''
            <html>
                {head}
                
            </html>
        '''

        return output
