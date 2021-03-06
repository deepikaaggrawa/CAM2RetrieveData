"""
--------------------------------------------------------------------------------
Descriptive Name     : Useful.py
Author               : Sanghyun Joo
Contact Info         : joos@purdue.edu OR toughshj@gmail.com
Date Written         : 18 July 2016
Description          : Class for some useful functions that are commonly used for many scripts
Command to run script: N/A
Usage                : N/A
Input file format    : N/A
Output               : N/A
Note                 : This class has some useful functions for parsing scripts.
                       Inherit this class to use them.
Other files required by : N/A
this script and where     
located                   

----For Parsing Scripts---------------------------------------------------------
Website Parsed       : N/A
In database (Y/N)    : N/A
Date added to Database : N/A
--------------------------------------------------------------------------------
"""

import urllib2
import traceback
from bs4 import BeautifulSoup

class Useful:
    def get_parser_with_soup(self, url):
        """ Create beautifulSoup object with the given url and return it

            Args:
                url: the URL address of the webpage to be parsed

            Return:
                soup: beautifulSoup object to parse the given URL
        """
        opener = urllib2.build_opener() 
        opener.addheaders = [('User-agent', 'Mozilla/5.0')] # Add header information
        response = opener.open(url)
        page = response.read()
        soup = BeautifulSoup(page, "html.parser")           # Create soup

        return soup

    def get_token_between(self, string, front, end):
        """ Extract the substring between <front> and <end> string
            
            The string contains string or html element
            This function extract the substring between <front> and <end> string
            If front string is empty, return string from the first character to the split of end string
            If end string is empty, return string from the end character to the split of the front string

            Args:
                string: string or html element
                front: string at the left of the wanted substring
                end: string at the right of the wanted substring

            Return:
                token: the string between <front> and <end> string OR if DNE, return empty string
        """
        try:
            s = str(string.encode("UTF-8"))
            if front == "":
                token = s.split(end)[0]
            elif end == "":
                token = s.split(front)[1]
            else:
                front_split = s.split(front)[1]
                token = front_split.split(end)[0]
        except:
            print("get_token error")
            traceback.print_exc()
            token = ""

        return token

    def convert_parsed_data_into_input_format(self, camera_data):
        """ Get the input format to the list file from the camera data

            Args:
                camera_data: CameraData object that contains all the data about a camera

            Return:
                input_format: one line input format that will be appended on the list file
        """
        self.gps.locateCoords(camera_data.get_description(),
                              camera_data.get_city(),
                              camera_data.get_state(),
                              camera_data.get_country())

        input_format = self.gps.city + "#" + self.gps.country + "#" + self.gps.state + "#" + camera_data.get_img_src() + "#" + self.gps.latitude + "#" + self.gps.longitude + "\n"
        input_format = input_format.replace("##", "#")    # if no state exists, state == ""

        return input_format

    def write_to_file(self, input_format):
        """ write the input file into the list file
        """
        self.list_file.write(input_format)
