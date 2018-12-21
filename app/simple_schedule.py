import datetime, MySQLdb
from recycle import get_database
from municipalities.schedule_helpers import get_holidays, set_simple_schedule, zone_combinations

#Set up limits for scheduling
total_weeks = 3000
start_date = "2014-08-10"
stop_date = "2025-12-31"
date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
last_date=datetime.datetime.strptime(stop_date, "%Y-%m-%d")

#Set up database
cur=get_database()

#Set schedule for municipalities with weekly pickups

#New York City
municipality = "NEW_YORK"
holidays = get_holidays(municipality, start_date, stop_date, cur)
days = [1, 2, 3, 4, 5, 6]

service = "TRASH"
shift = "DOWN"
zones = zone_combinations(days, 2, 6)
for zone in zones:
    set_simple_schedule(municipality, service, date, last_date, total_weeks, holidays, zone, shift, cur)

service = "RECYCLE"
shift = "SKIP_DOWN"
zones = zone_combinations(days, 1, 1)
for zone in zones:
    set_simple_schedule(municipality, service, date, last_date, total_weeks, holidays, zone, shift, cur)

#Washington, DC
municipality = "DC"
holidays = get_holidays(municipality, start_date, stop_date, cur)
days = [1, 2, 3, 4, 5]

service = "TRASH"
shift = "DOWN"
zones = zone_combinations(days, 1, 2)
for zone in zones:
    set_simple_schedule(municipality, service, date, last_date, total_weeks, holidays, zone, shift, cur)

service = "RECYCLE"
shift = "DOWN"
zones = zone_combinations(days, 1, 1)
for zone in zones:
    set_simple_schedule(municipality, service, date, last_date, total_weeks, holidays, zone, shift, cur)

#Philadelphia test version
municipality = "PHILADELPHIA"
holidays = get_holidays(municipality, start_date, stop_date, cur)
days = [1, 2, 3, 4, 5]

#Write to test version of database
municipality = "PHILLY"

service = "TRASH"
shift = "DOWN"
zones = zone_combinations(days, 1, 1)
for zone in zones:
    set_simple_schedule(municipality, service, date, last_date, total_weeks, holidays, zone, shift, cur)

service = "RECYCLE"
shift = "DOWN"
zones = zone_combinations(days, 1, 1)
for zone in zones:
    set_simple_schedule(municipality, service, date, last_date, total_weeks, holidays, zone, shift, cur)






