
################################################################################################################################################################################
#   Zone and day LM specific
################################################################################################################################################################################

from dataclasses import dataclass
import datetime
import json
import logging
import requests

from municipalities import schedule_helpers

logger = logging.getLogger(__name__)

def get_zone_items(address) -> list[dict]:
    """Get tokaen and then zone information from matching addresses from LM API"""
    token_url = "https://www.lowermerion.org/Home/GetToken"
    token_headers = {
        "Accept": "application/json",
        "User-Agent": "recyclobuddy",
        "Content-Type": "application/json",
    }
    x = requests.post(token_url, headers=token_headers)
    if x.status_code != 200:
        logger.error("Failed to get LM token")
        return
    response_dict = json.loads(x.text)
    token = response_dict.get("Token")
    
    search_url = "https://flex.visioninternet.com/api/FeFlexComponent/Get"
    search_headers = {
        "Accept": "application/json",
        "User-Agent": "recyclobuddy",
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    payload = {"pageSize":20,"pageNumber":1,"sortOptions":[],"searchText": address,"searchFields":["Address"],"searchOperator":"OR","searchSeparator":",","Data":{"componentGuid":"f05e2a62-e807-4f30-b450-c2c48770ba5c","listUniqueName":"VHWQOE27X21B7R8"},"filterOptions":[]}
    y = requests.post(search_url, headers=search_headers, json=payload)
    if y.status_code != 200:
        return

    y_dict = json.loads(y.text)
    records = y_dict.get("records")
    if not records:
        return
    items = records.get("items")
    return items


@dataclass
class ZoneItem:
    """Class for relevant itms returned from LM address search"""
    collection_day: int
    holiday_zone: str
    address: str


def get_zone_from_items(items, address, zip):
    """Attempt to match zip as well as address. Return a list of zone information and addresses"""
    zip_string = f"({zip})"

    match_address = [item for item in items if address in item.get("Address")]
    match_zip = [item for item in match_address if zip_string in item.get("Address")]

    if match_zip:
        match_elements = match_zip
    elif match_address:
        match_elements = match_address
    else:
        return []

    return [ZoneItem(
        collection_day=schedule_helpers.get_day_number(match_element.get("Collection")), 
        holiday_zone=match_element.get("HolZone"),
        address=match_element.get("Address")
    ) for match_element in match_elements]


def get_zone(address, zip) -> list[ZoneItem]:
    """Get a list of ZoneItems, log if none found or multiple items are found"""
    items = get_zone_items(address)
    if not items:
        logger.warning(f"Failed to locate LM zone information for address: {address} and zip: {zip}")
    if len(items) > 1:
        logger.error(f"Returned multiple zones for address: {address}. Should be unique: {items}")
    return get_zone_from_items(items, address, zip)

def get_trash_zone(address, zip):
    """Return tuple of collection_day and holiday zone"""
    zone_items = get_zone(address, zip)
    if not zone_items or len(zone_items) != 1:
        return None
    zone_item = zone_items[0]
    return zone_item.collection_day, zone_item.holiday_zone


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
                    recycle_day = schedule_helpers.get_day(next_week, number, shift)
                    days_ahead = 7 + recycle_day -1
                    
                else:
                    #It is a recycling week.
                    recycle_day = schedule_helpers.get_day(this_week, number, shift)

                    #Is the day past?
                    if day<=recycle_day:
                        #Still good
                        days_ahead = recycle_day -1
                    else:
                        if period==2:
                            #Day past, so find day 2 weeks ahead
                            recycle_day = schedule_helpers.get_day(following_week, number, shift)
                            days_ahead = 14 + recycle_day -1
                        elif period==1:
                            #Day past, so find day 1 week ahead
                            recycle_day = schedule_helpers.get_day(next_week, number, shift)
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
