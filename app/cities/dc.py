from time import sleep, time
import sys, os
sys.path.append(os.path.dirname(__file__))

#from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from zones import get_day_number

MAX_WAIT = 5
RETRY_INCREMENT = 0.01

class DC:
 
    def __init__(self, browser):
        self.browser = browser
        self.url = "http://collectionday.dcgis.dc.gov/"
        self.zip_codes =    [
            20222, 20060, 20226, 20064, 20229, 20530, 20533, 20532, 20250, 20091, 20543, 20542, 20546, 20262, 20509,  20515, 
            20268, 20549, 20303, 20317, 20319, 20373, 20593, 20390, 20402, 20401, 20001, 20003, 20002, 20005, 20004, 
            20007, 20006, 20009, 20008, 20011, 20010, 20422, 20012, 20016, 20015, 20018, 20017, 20020, 20019, 20433, 
            20431, 20024, 20032, 20030, 20037, 20036, 20202, 20203, 20044, 20052, 20057, 20507, 20510, 20059, 20220, 
        ]

    def get_zone(self, address, zip):

        if zip not in self.zip_codes:
            return ('Zip code not found')

        time0 = time()     

        self.browser.get(self.url)
        element = self.browser.find_element_by_id("txtLocation")
        element.send_keys(address, Keys.TAB)
        element.send_keys(Keys.ENTER)

        tags = []

        start_time = time()
        while len(tags) == 0 and time() - start_time < MAX_WAIT:
            sleep(RETRY_INCREMENT)
            tags = self.browser.find_element_by_id("results").find_elements_by_css_selector("td")

        if tags and len(tags) >= 3:
            trash = tags[1].get_attribute('textContent').split('/')
            recycle = tags[3].get_attribute('textContent')

            if trash[0].upper() == "NO PICK UP" or recycle.upper() == "NO PICK UP":
                print("Sorry, there's no pick up at that address")

            trash_zone = "_" + "".join(str(get_day_number(day)) for day in trash)
            recycle_zone = "_" + str(get_day_number(recycle))

            element.clear()
            return ("Success", (trash_zone, recycle_zone), time() - time0)
        else:
            element.clear()
            return ("Couldn't find that address")

         
