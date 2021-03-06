"""
--------------------------------------------------------------------------------
Descriptive Name     : Parser for traffic cameras in Florida bay county's traffic website
Author               : Sanghyun Joo
Contact Info         : joos@purdue.edu OR toughshj@gmail.com
Date Written         : 21 June 2016
Description          : parses the city name, snapshot_url, latitude, and longitude for each camera
Command to run script: python FL_baycounty.py
Usage                : N/A
Input file format    : N/A
Output               : list_FL_baycounty.txt
Note                 : N/A
Other files required by : Geocoding.py and Useful.py in NetworkCameras/Discovery/Tools
this script and where     It requires Selenium and BeautifulSoup4 to be installed
located

----For Parsing Scripts---------------------------------------------------------
Website Parsed       : http://tmc.baycountyfl.gov/
In database (Y/N)    : Y
Date added to Database : 22 June 2016
--------------------------------------------------------------------------------
"""

# -*- coding: utf-8 -*-

import selenium.webdriver.support.ui as ui
import time
import re
import traceback
from Geocoding import Geocoding
from Useful import Useful
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup

class Florida(Useful):
    def __init__(self):
        # store the url of homepage, traffic page, the country code, and the state code
        self.home_url = "http://tmc.baycountyfl.gov"
        self.traffic_url = "http://tmc.baycountyfl.gov/"
        self.country = "USA"
        self.state = "FL"

        # open the file to store the list and write the format of the list at the first line
        self.f = open('list_FL_baycounty.txt', 'w')
        self.f.write("city#country#state#snapshot_url#latitude#longitude" + "\n")

        # open the web-browser
        firefox_profile = webdriver.FirefoxProfile()
        firefox_profile.set_preference("browser.download.folderList", 2)
        firefox_profile.set_preference("javascript.enabled", False)

        self.driver = webdriver.Firefox()
        self.wait = ui.WebDriverWait(self.driver, 10)

        # gps module
        self.gps = Geocoding('Google', None)

    def get_string(self, string):
        """ Extrac the description out of the string and return it

            The string might have character "@".
            If it has, get the right substring of @
            If not, get the entire string

            Args:
                string: the string that has description in it

            Return:
                result: the extracted description out of the string
        """
        result = None
        try:
            index = string.index("@")
            result = string[index + 1:]
        except:
            result = string

        return result

    def get_links_descrips(self, links_to_img, descrips):

        # loop through each camera to get the description and the link to the image of them
        for cam in self.driver.find_elements_by_class_name("cameras"):

            # click the camera to load the camera on a map
            cam.click()

            # wait for the element to load and parse it to get the data we need
            self.wait.until(lambda driver: self.driver.find_element_by_tag_name("iframe"))
            link_to_img = self.driver.find_element_by_tag_name("iframe").get_attribute('src')
            desc = cam.text
            
            # append the data to the lists 
            links_to_img.append(link_to_img)
            descrips.append(desc)
    
    def main(self):
        # open the browser and move to the traffic page
        self.driver.get(self.home_url)

        # lists to store the description and the link to the image of each camera
        links_to_img = []
        descrips = []

        self.get_links_descrips(links_to_img, descrips)

        # loop through the links to the images to get the image URLs
        for i in range(len(links_to_img)):
            
            # move to the webpage that has the image URL of the camera
            self.driver.get(links_to_img[i])

            # get the description, image URL, and the city name of the camera
            descrip = descrips[i]
            img_src = self.driver.find_element_by_id("CamImage").get_attribute('src')
            city = "Bay County"
            
            print(descrip, img_src)

            try:
                self.gps.locateCoords(descrip, city, self.state, self.country)
                result = self.gps.city + "#" + self.gps.country + "#" + self.gps.state + "#" + img_src + "#" + self.gps.latitude + "#" + self.gps.longitude + "\n"
                result = result.replace("##", "#")
                self.f.write(result)
            except:
                print("can't find")

if __name__ == '__main__':
    Florida = Florida()
    Florida.main()
