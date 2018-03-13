import mechanize
import re
import datetime
import MySQLdb
from address import AddressParser, address

import schedule_helpers

#Philadelphia subroutines

################################################################################################################################################################################
#   Zone and day Philadelphia specific
################################################################################################################################################################################

#Find Philadelphia day information
def get_trash_zone(address, zip):


    #Make cookie jar.  See wwwsearch.sourceforge.dat/mechanize/hints.html
    cj=mechanize.LWPCookieJar()
    opener=mechanize.build_opener(mechanize.HTTPCookieProcessor(cj))
    mechanize.install_opener(opener)

    #Create a browser
    browser=mechanize.Browser()

    #Save cookies
    cj.save("/usr/local/django/recyclocity/recyclocity_static/cookies/cookie_jar", ignore_discard=True, ignore_expires=True)

    #Fill in form
    #browser.open('http://citymaps.phila.gov/portal/')
    #browser.select_form(name="form1")
    #browser.form['txtSearchAddress'] = address

    #Fill in form
    browser.open('https://alpha.phila.gov/property/')
    browser.form = list(browser.forms())[0]
    browser.form['a'] = address

    #Submit form
    browser.submit()

    #Extract content
    content = browser.response().read()

    print content

    #Use pattern match to extract trash day
    m=re.search('<div data-hook="rubbish-day" class="xtra-lg no-margin">([A-Z]+)', content)

    print m

    if m:
	day,=m.groups()
	day_number = schedule_helpers.get_day_number(day)
    else:
	return
    
    #Use pattern match to extract zip
    #m=re.search('<b>Zip \+4:</b> (\d{5})-', content)
    m=re.search('<b>Zip \+4:</b> (\d{5})', content)

    if m:
	match_zip,=m.groups()
    else:
	return

    #Verify that the zip returned from citymaps matches expected value.  Philadelphia only uses days, so return day_number for zone.
    if int(match_zip)==int(zip):
	return day_number, day_number
    else:
     	return
   

