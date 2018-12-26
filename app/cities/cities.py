from time import sleep, time
import re

from selenium import webdriver

from zones import get_day_number
from nyc import NYC
from dc import DC

CHROME_PATH = "/usr/local/bin/chromedriver"

class Cities:
    def __init__(self, engine="CHROME"):
        self.browser = self.get_browser(engine)
        self.nyc = NYC(self.browser)
        self.dc = DC(self.browser)

    def get_browser(self, browser_engine="CHROME"):
        engine = browser_engine.upper()
        if engine == "FIREFOX":
            from selenium.webdriver.chrome.options import Options
            options = Options()
            options.add_argument('-headless')
            browser = webdriver.Firefox(firefox_options=options) 
        elif engine == "PHANTOM":
            browser = webdriver.PhantomJS()
        elif engine == "CHROME":
            from selenium.webdriver.chrome.options import Options
            options = Options()
            try:
                options.headless = True
            except AttributeError:
                options.set_headless(headless=True)
            browser = webdriver.Chrome(options=options, executable_path=CHROME_PATH)
        else:
            raise ValueError('Browser must be FIREFOX, PHANTOM or CHROME')
        return browser

    def close_browser(self):
        self.browser.close()

