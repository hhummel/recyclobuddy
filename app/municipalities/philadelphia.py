#import mechanize
import requests
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
    '''Get trash zone/day number from city api'''
    import json, urllib

    #New Philadelphia API
    frags = {'first': 'https://api.phila.gov/ais/v1/addresses/',
        'last': '?gatekeeperKey=12070257c23a728f3c09f1d0d6c7d53b'}

    url = frags['first'] + urllib.quote(address) + frags['last']

    attempts = 0
    max_attempts = 5
    timeout = 2
    json_data = ""
    while (json_data=="" or attempts < max_attempts):
        try:
            r = requests.get(url, timeout=timeout)
            json_data = r.json()
            break
        except:
            attempts = attempts + 1

    #Check for a result, convert to day number.  Return nothing if there's an error
    if str(zip).strip() ==json_data['features'][0]['properties']['zip_code']:
        day = json_data['features'][0]['properties']['rubbish_recycle_day']
        day_number = schedule_helpers.get_day_number(day)
    else:
        return

    #Check that zip code matches that in query, to ensure the municipality is correct
    if str(zip).strip() ==json_data['features'][0]['properties']['zip_code']:
        return day_number, day_number
    else:
        return

