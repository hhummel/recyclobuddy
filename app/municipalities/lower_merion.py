import urllib
import requests

import re
import datetime
import MySQLdb
from address import AddressParser, address

import schedule_helpers

#Lower Merion subroutines

################################################################################################################################################################################
#   Zone and day LM specific
################################################################################################################################################################################


#Find LM recycling day and zone
def get_recycling_zone(address, zip):

    params = {'askrecycle': address, 'postcode': zip}
    headers = {'user-agent': 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11'}
    attempts = 0
    max_attempts = 5
    timeout = 2
    content = ""
    while (content=="" or attempts < max_attempts):
        try:
            session = requests.Session()
            s = session.post('http://lmt-web.lowermerion.org/cgi-bin/recycle2.plx/', data=params, headers=headers, timeout=timeout)
            content = s.text
            break
        except requests.exceptions.ReadTimeout:
            attempts = attempts + 1
    
    #Use pattern match to extract recycle day
    m=re.search('every other <b> (Monday|Tuesday|Wednesday|Thursday|Friday)</b>.+Zone ([AB][1-4])', content)

    if m:
        day, zone = m.groups()
        #Convert day to number
        day_number = schedule_helpers.get_day_number(day)
        return day_number, zone
    else:
        #Failed to match a vaild address and zip combination in Lower Merion.
        return

#Find LM trash day and zone
def get_trash_zone(address, zip):

    params = {'askzone': address, 'postcode': zip}
    headers = {'user-agent': 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11'}
    attempts = 0
    max_attempts = 5
    timeout = 2
    content = ""
    while (content=="" or attempts < max_attempts):
        try:
            session = requests.Session()
            s = session.post('http://lmt-web.lowermerion.org/cgi-bin/refuse2.plx/', data=params, headers=headers, timeout=timeout)
            content = s.text
            break
        except requests.exceptions.ReadTimeout:
            attempts = attempts + 1

    #Use pattern match to extract fields
    m=re.search('<b>(Monday|Tuesday|Wednesday|Thursday|Friday)</b>', content)
    if m:
        day, =m.groups()
        #Convert day to number
        day_number = schedule_helpers.get_day_number(day)
    else:
        #Failed
        return

    m=re.search('<b>Zone ([1-4])</b>', content)
    if m:
        zone,=m.groups()
    else:
        #Failed
        return                
        
    #Match for both day and zone        
    return day_number, zone

################################################################################################################################################################################
#   Schedule LM specific
################################################################################################################################################################################
#Find the schedule where period is the frequncy of service, (1 for weekly, 2 for every other week), and holiday shift logic, ("LM" for Lower Merion's unique system).
def set_schedule(municipality, service, period, date, last_date, total_weeks, holidays, shift, zone_days, cur):

  #Set up zone letters
  if period==2:
    zone_letters = ("A", "B")
  else:
    zone_letters = ("A",)

  #Loop over weeks
  for weeks in range (1, total_weeks):
    #Figure out if it's an A or B week if period is 2, (all A's if period is 1)
    if weeks%period==1:
        week_label="B"
    else:
        week_label="A"
        
    for day in range (1, 8):
        date = date + datetime.timedelta(days=1)
        
        #Check if date is in range
        if date>last_date:
            return

        #Check for holiday week on Mondays
        if day ==1:
            #Capture date
            monday=date

            #Check if this week is a holiday
            this_week=schedule_helpers.holiday_week(date, holidays)

            #Check if next week is a holiday
            next_week=schedule_helpers.holiday_week(date + datetime.timedelta(days=7), holidays)

            #Check if following week is a holiday
            following_week=schedule_helpers.holiday_week(date + datetime.timedelta(days=14), holidays)
        #Loop over zones and days
        for letter in zone_letters:
            for tuple in zone_days:
                #Get raw zone number and corresponding day of week
                raw_number, number = tuple
                
                #If period is 2, is this an on week or off week?
                if week_label != letter:
                    #Not a recycling week, so find recycle day next week.  Only occurs if period=2.
                    recycle_day = get_day(next_week, number, shift)
                    days_ahead = 7 + recycle_day -1
                    
                else:
                    #It is a recycling week.
                    recycle_day = get_day(this_week, number, shift)

                    #Is the day past?
                    if day<=recycle_day:
                        #Still good
                        days_ahead = recycle_day -1
                    else:
                        if period==2:
                            #Day past, so find day 2 weeks ahead
                            recycle_day = get_day(following_week, number, shift)
                            days_ahead = 14 + recycle_day -1
                        elif period==1:
                            #Day past, so find day 1 week ahead
                            recycle_day = get_day(next_week, number, shift)
                            days_ahead = 7 + recycle_day -1
                        else:
                            exit("Error, period must be 1 or 2")
                            
                #next_day is the next pickup day for this zone            
                next_day = monday + datetime.timedelta(days=days_ahead)

                #days_to_pickup is the days between date and next_day
                days_to_pickup = next_day - date

                #Strip out the number of days
                number_days = days_to_pickup.days

                #Make zone string using official (raw) zone number
                if period==2:
                    zone_str=letter+str(raw_number)
                else:
                    zone_str=str(raw_number)
        
                #Insert record into app_schedule table
                schedule_helpers.set_record(cur, municipality, service, date.strftime("%Y-%m-%d"), zone_str, raw_number, this_week, next_day.strftime("%Y-%m-%d"), str(days_to_pickup))



