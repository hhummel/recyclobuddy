import urllib, urllib2


import mechanize
import re
import datetime
import MySQLdb
from address import AddressParser, address


#Lower Merion subroutines

################################################################################################################################################################################
#   Zone and day LM specific
################################################################################################################################################################################

#Find LM recycling day and zone
def get_recycling_zone(address, zip):
        #Set up the browser for recycling
        url = 'http://www.lowermerion.org/cgi-bin/recycle2.plx/'
        data = urllib.urlencode({
                'askrecycle' : address,
                'postcode' : zip
        })

        #Extract content
        content = urllib2.urlopen(url=url, data=data).read()

        return content

#Find Philadelphia day information
def get_trash_zone(address, zip):


    #Make cookie jar.  See wwwsearch.sourceforge.dat/mechanize/hints.html
    cj=mechanize.LWPCookieJar()
    opener=mechanize.build_opener(mechanize.HTTPCookieProcessor(cj))
    mechanize.install_opener(opener)

    #Create a browser
    browser=mechanize.Browser()

    #User-Agent (this is cheating, ok?)
    browser.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

    #Save cookies
    cj.save("/usr/local/django/recyclocity/recyclocity_static/cookies/cookie_jar", ignore_discard=True, ignore_expires=True)

    #Fill in form
    #browser.open('http://citymaps.phila.gov/portal/')
    #browser.select_form(name="form1")
    #browser.form['txtSearchAddress'] = address
    
    #Fill in form
    #browser.open('https://alpha.phila.gov/property/')
    #browser.open('http://www.lowermerion.org/cgi-bin/recycle2.plx/')
    browser.open('http://www.lowermerion.org/services/public-works-department/refuse-and-recycling/how-to-determine-your-recycling-collection-day')
    #browser.form = list(browser.forms())[0]
    #browser.form['askrecycle'] = address
    #browser.form['postcode'] = zip

    #Submit form
    #browser.submit()

    #Extract content
    content = browser.response().read()

    return content

