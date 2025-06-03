"""
@author: Ashutosh Mishra | ashutosh_mishra_@outlook.com
@created: 1 Sep 2022
@last_modified: 03 Jun 2025
@desc: Utilities Class;
    Contains all the utilities for this automation framework.
"""

import datetime
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import urllib
import requests
import urllib3
import platform
import json
from openpyxl import load_workbook


class CollectAttributesFromDict(dict):
    def __getattr__(self, item):
        return self[item]

    def __dir__(self):
        return super().__dir__() + [str(k) for k in self.keys()]
    

# [DEPRICATION WARNING] This class is deprecated and will be removed in future versions.
# Use CollectAttributesFromDict instead.
class PageLocatorDict(dict):
    def __getattr__(self, item):
        return self[item]

    def __dir__(self):
        return super().__dir__() + [str(k) for k in self.keys()]


class ReadExcel:
    def __init__(self, file_name, sheet_name):
        self.workbook = load_workbook(file_name)
        self.worksheet = self.workbook[sheet_name]

    def read_from_excel(self, column, row):
        cell = "{}{}".format(column, row)
        cell_value = self.worksheet[cell].value
        return cell_value


class SubprocessCallError(Exception):
    pass


class Utilities:
    def __init__(self):
        pass

    def is_windows(self):
        return re.search("Windows", platform.platform()) is not None

    def is_solaris(self):
        return re.search("SunOS", platform.platform()) is not None

    def is_mac(self):
        return re.search('Darwin', platform.platform()) is not None

    def is_linux(self):
        return re.search('Linux', platform.platform()) != None

    def get_os_platform(self):
        return platform.platform()

    def get_os_language(self):
        pass

    # File/Folder Operations
    # ----------------------------

    def get_path(self, location, file):
        """
        This function will return Full path of given file
        :param location: Folder address
        :param file: File name
        :return: Full Path for file
        """
        _TempFile = file[1:] if file and file[0] == "/" else file
        return os.path.join(location, _TempFile)

    def get_current_working_dir(self):
        """
        This function used to get current working directory
        :return: working path
        """
        return os.getcwd()

    def base_name(self, path):
        """
        # Go to two folder back as project folder have the directory
        This function get core name in specified path
        :param path: A path-like object representing a file system path.
        :return: his method returns a string value which represents the core name the specified path.
        """
        return os.path.basename(path)

    def get_executable_path(self, executable):
        if "PATH" in os.environ:
            paths = os.environ["PATH"].split(os.pathsep)
            for path in paths:
                if os.path.exists(os.path.join(path, self.get_executable_name(executable))):
                    return os.path.dirname(os.path.abspath(path))
        return None

    def get_executable_name(self, executable):
        return (executable + ".exe") if self.is_windows() else executable

    def get_downloads_dir(self):
        return self.get_path(os.path.expanduser('~'), 'downloads' if self.is_windows() else 'Downloads')

    def remove_file(self, file):
        os.remove(file)

    def get_directory_name(self, path, back=True):
        """
        This function gets directory name
        :param path: A path-like object representing a file system path. A path-like object representing a file system path.
        :param back: True for get back in path
        :return: This method returns a string value which represents the directory name from the specified path.
        """
        if back:
            return os.path.dirname(os.path.dirname(path))
        return os.path.dirname(path)

    def get_basename(self, path, ext=False):
        """
        This function will get basename of path
        :param Path: Path like string
        :return: path object
        """
        return os.path.basename(path).replace(".py", "") if ext else os.path.basename(path)

    def copy_file(self, src, dest, file_name=None):
        """
        This function used to copy one file to another location
        :param Source: Location of file
        :param Destination: Where to copy the file
        :param FileName: File name
        :return: Full path of file after copied
        """
        if file_name:
            src = self.get_path(src, file_name)
            dest = self.get_path(dest, file_name)
        # else:
        #     # FileName = BaseName(Source)
        #     # Destination = self.GetPath(Destination,
        #     #                       self.BaseName(Source))  # DirectoryPath(Destination, Back=False),BaseName(Source))
        #     # Source = GetPath(DirectoryPath(Source, Back=False),BaseName(Source))

        print(f"Source file --> {src}, Destination File --> {dest}")

        if not self.file_folder_validation(src, Type="-o"):  # Check if Folder or not
            print(f"File or Folder not valid --> {src}")
            return False
        return shutil.copyfile(src, dest)

    def file_folder_validation(self, FName, Type="-o", Print=False, create=False):
        """
        This function check whether given input if file , folder or path exist or not
        :param FName: full path for file/folder under test
        :param Type: for file ="-f", for directory ="-d" and for Path ="-o"
        :return: boolean with TRUE / FALSE
        """
        if Type == "-f":
            if os.path.isfile(FName):
                return True
            if Print:
                print(f'No File found with: {FName}')
        elif Type == "-d":
            if os.path.isdir(FName):
                return True
            if Print:
                print(f'No directory found with: {FName}')
        elif Type == "-o":
            if os.path.exists(FName):
                return True
            if Print:
                print(f'No path found with: {FName}')
        else:
            print('Please chose for file ="-f", for directory ="-d" and for Path ="-o"')
            sys.exit(0)
        if create and Type == "-d":
            os.mkdir(FName)
            return True
        return False

    def unzip_file(self, archives, extract_path):
        shutil.unpack_archive(archives, extract_path)

    def get_files(self, dir, filter=None):
        return os.listdir(dir) if not filter else [file for file in os.listdir(dir) if self.find_text(file, filter)]

    def get_newest_file(self, file_path, filter=None):
        files = os.listdir(file_path)
        if filter:
            paths = [os.path.join(file_path, basename) for basename in files if self.find_text(basename, filter)]
        else:
            paths = [os.path.join(file_path, basename) for basename in files]
        return max(paths, key=os.path.getctime)

    def is_file_in_dir_present(self, dir_path, file_pattern):
        for file_name in os.listdir(dir_path):
            if file_pattern in file_name:
                return True
        return False

    def change_permissions_recursive(self, path, mode=0o777):
        for root, dirs, files in os.walk(path, topdown=False):
            for dir in [os.path.join(root, d) for d in dirs]:
                os.chmod(dir, mode)
            for file in [os.path.join(root, f) for f in files]:
                os.chmod(file, mode)

    def remove_readonly(self, func, path, _):
        """
        Clear the readonly bit and reattempt the removal
        """
        print(f"value of path = {path} and value of func = {func} and value of _ = {_} in remove_readonly function")
        os.chmod(path, 0o777)
        func(path)

    def create_file(self, file_name, data, new_line_at_the_end=True, mode="w", save_as=None):
        """
        This function used to append data to file if available
        else this will create a file and write data to it

        @return: True
        @param save_as: Save file to a location
        @param mode: mode append or write
        @param new_line_at_the_end:
        @param data: data to write
        @param file_name: File name (absolute name)
        """
        print(f"writing data to {file_name if not save_as else os.path.join(save_as, file_name)} with text {data}")
        data = data if type(data) == str else str(data)
        try:
            with open(file_name if not save_as else os.path.join(save_as, file_name), mode) as f:
                f.write(f"{data}\n" if new_line_at_the_end else data)
        except Exception as e:
            print(f"Error writing file: {e}")
            return False
        return True

    def read_file(self, filename, filter=None, debug=False, encoding="utf-8"):
        """
        This will open and read a file with filter string
        :param encoding:  utf coding enable
        :param filename: Name of the file
        :param Filter: Optional to filter out some line as regular expression
        :return: Generator expression with file line
        """
        status = []
        try:
            with open(filename, errors='ignore', encoding=encoding) as f:
                lines = f.readlines()
                try:
                    if debug:
                        print(lines)
                    if filter:
                        return (line for line in lines if self.find_text(line, reg_exp=filter))
                    else:
                        return (line for line in lines)
                except StopIteration:
                    pass
        except GeneratorExit:
            pass
        except:
            print(f"File not valid please check error at {filename}", exc_info=True)
        return status

    def read_xml_file(self, filename):
        print(f"Reading {filename} XML file ")
        import xml.etree.ElementTree as ET
        tree = ET.parse(filename)
        root = tree.getroot()
        return root

    def unzip_file(self, archives, extract_path):
        shutil.unpack_archive(archives, extract_path)

    # String Operations
    # --------------------

    def replace_str(self, string, reg_exp, replace_with=""):
        """
        This function used to replace a specif String
        :param Data: String which need to change
        :param reg_exp: Finding string for this given regular expression
        :param replace_with: Replace string
        :return: String after replace
        """
        return re.sub(reg_exp, replace_with, string)

    def find_text(self, string, reg_exp, position=None, plus=True):
        """
        This Function used to find text on given string
        :param string: Which needs to scan
        :param reg_exp: string to finding data
        :param position: get a specific position after filter
        :return: Data after finding
        """
        reg_exp = reg_exp.replace("+", "\+") if not plus else reg_exp
        matches = re.findall(reg_exp, string)
        try:
            return matches[position] if position is not None and matches else matches
        except IndexError:
            print("String not found")
            return None

    def split(self, string, reg_exp, position=None):
        """
        This Function splits the given stringbased on the provided reguler expression
        :param string: Which needs to scan
        :param reg_exp: string from where break the main string
        :param position: get a specific position after filter
        :return: array of strings after splitting
        """
        arr_strings = re.split(reg_exp, string)
        return arr_strings[position] if not (position is None) and arr_strings else arr_strings

    # System Call/Process Operation
    # --------------------------------------

    def execute_command(self, command, log_output=False, fail_on_error=False):
        process = subprocess.Popen(command, stdout=subprocess.PIPE)
        output = process.communicate()

        if log_output:
            print("Output:" + str(output))
            print("----------------------------------------------------------------------")

        if fail_on_error:
            if process.returncode != 0:
                raise SubprocessCallError(output)

        return output

    def run_command(self, *argv, shell=True, log_output=False):
        """
        This function used to run command on cmd prompt and return output print
        :param Print:
        :param argv: list of command to run
        :param Op: This required if system needs to use bash file
        :return: STDOUT and estimate time
        """
        output = ""
        _commands = " ".join(str(x) for x in argv)
        if shell:
            argv = _commands

        # Status = True
        with subprocess.Popen(argv, shell=shell, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1,
                              universal_newlines=True, encoding="UTF-8") as p:
            for line in p.stdout:
                output += line
                if log_output:
                    print(line)  # process line here
        return output

    # Date Operations
    # --------------------

    def get_date_now(self, ):
        return datetime.datetime.now()

