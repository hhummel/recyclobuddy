from time import sleep, time
import re

#from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
#from selenium.webdriver import Firefox
#from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException

from zones import get_day_number

class NYC:
    def __init__(self, browser):
        self.browser = browser
        self.url = "http://www1.nyc.gov/apps/311utils/addressinfo.htm"
        self.zip_codes = {
            "BRONX": [10453, 10457, 10460, 10458, 10467, 10468, 10451, 10452, 10456, 10454, 10455,
                10459, 10474, 10463, 10471, 10466, 10469, 10470, 10475, 10461, 10462, 10464, 10465,
                10472, 10473],

            "BROOKLYN": [11212, 11213, 11216, 11233, 11238, 11209, 11214, 11228, 11204, 11218,
                11219, 11230, 11234, 11236, 11239, 11223, 11224, 11229, 11235, 11201, 11205, 11215,
                11217, 11231, 11203, 11210, 11225, 11226, 11207, 11208, 11211, 11222, 11220, 11232,
                11206, 11221, 11237],

            "MANHATTAN": [10026, 10027, 10030, 10037, 10039, 10001, 10011, 10018, 10019, 10020,
                10036, 10029, 10035, 10010, 10016, 10017, 10022, 10012, 10013, 10014, 10004, 10005,
                10006, 10007, 10038, 10280, 10002, 10003, 10009, 10021, 10028, 10044, 10065, 10075,
                10128, 10023, 10024, 10025, 10031, 10032, 10033, 10034, 10040],

            "QUEENS": [11361, 11362, 11363, 11364, 11354, 11355, 11356, 11357, 11358, 11359, 11360,
                11365, 11366, 11367, 11412, 11423, 11432, 11433, 11434, 11435, 11436, 11101, 11102,
                11103, 11104, 11105, 11106, 11374, 11375, 11379, 11385, 11691, 11692, 11693, 11694,
                11695, 11697, 11004, 11005, 11411, 11413, 11422, 11426, 11427, 11428, 11429, 11414,
                11415, 11416, 11417, 11418, 11419, 11420, 11421, 11368, 11369, 11370, 11372, 11373,
                11377, 11378],

            "STATEN ISLAND": [10302, 10303, 10310, 10306, 10307, 10308, 10309, 10312, 10301, 10304,
                10305, 10314]
        }

    def get_zone(self, address, zip):
        MAX_WAIT = 5
        RETRY_INCREMENT = 0.01

        #Check arguments
        if not address or not zip:
            return ("Requires a street address and zip code")

        #Try to get borough from the zip
        borough =  self.get_borough(zip)
        if not borough:
            return ("Zip code not found in NYC")

        #Split out the building number from the street name
        m = re.match('([0-9]+)\s+(.+)', address)
        if not m or not m.group(1) or not m.group(2):
            return

        number = m.group(1)
        street = m.group(2)

        time0 = time()
    
        self.browser.get(self.url)
        element0 = self.browser.find_element_by_id("building_address")
        element1 = self.browser.find_element_by_id("street_name")
        element2 = Select(self.browser.find_element_by_id("borough"))
        element3 = self.browser.find_element_by_id("searchButton")

        #Submit input information to form
        element0.send_keys(number)
        element1.send_keys(street)
        element2.select_by_value(borough)
        element3.send_keys(Keys.ENTER)

        #Poll every RETRY_INCREMENT seconds for up to MAX_WAIT seconds for the result.
        trash = recycle = {}
        start_time = time()
        while len(trash) == 0 and time()-start_time < MAX_WAIT:
            sleep(RETRY_INCREMENT)
            trash = self.browser.find_element_by_id("trash_pickup_days").get_attribute('textContent')
            recycle = self.browser.find_element_by_id("recycling_pickup_days").get_attribute('textContent')
    
        if trash and recycle:
            trash_days = [str(get_day_number(day)) for day in trash.split(",")]
            trash_zone = "_" + "".join(trash_days)

            recycle_list = re.findall(r"[\w']+", recycle)
            recycle_zone = "_" + "".join([str(get_day_number(day)) for day in recycle_list if day.strip() != "Every"])

            return ("Success", (trash_zone, recycle_zone), time() - time0)
        else:
            return ("Zone not found for that address")

    def get_borough(self, zip):
        '''Return the NYC borough name from the zip code, or '' if not found'''
        for key, value in self.zip_codes.items():
            if zip in value:
                return key
        return ''

