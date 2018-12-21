import datetime
import MySQLdb

from recycle import get_database
from municipalities.schedule_helpers import get_holidays, set_schedule

total_weeks=3000
start_date="2014-08-10"
stop_date="2025-12-31"
date=datetime.datetime.strptime(start_date, "%Y-%m-%d")
last_date=datetime.datetime.strptime(stop_date, "%Y-%m-%d")

#########################################################################################################################################
# Start up
#########################################################################################################################################

#Set up database
cur=get_database()
#########################################################################################################################################
#Lower Merion:  Warning!  Don't rerun program without clearing database or there will be redundant entries
#########################################################################################################################################
municipality="LOWER_MERION"

#Get holidays
holidays=get_holidays(municipality, start_date, stop_date, cur)

#Set up list of normal day and zone days for LM.  LM uses 5 zones on normal weeks and 4 zones holiday weeks.
normal_days=[1, 2, 3, 4, 5]
zone_days=[1, 2, 3, 4]

#Find recycling schedule, (period=2)
service="RECYCLE"
period=2
set_schedule(municipality, service, period, date, last_date, total_weeks, holidays, "LM", normal_days, zone_days, cur)

#Find trash schedule, (period=1)
service="TRASH"
period=1
set_schedule(municipality, service, period, date, last_date, total_weeks, holidays, "LM", normal_days, zone_days, cur)

#Find yard schedule, (period=1)
service="YARD"
period=1
set_schedule(municipality, service, period, date, last_date, total_weeks, holidays, "LM", normal_days, zone_days, cur)

#########################################################################################################################################
#Philadelphia:  Warning!  Don't rerun program without clearing database or there will be redundant entries
#########################################################################################################################################
municipality="PHILADELPHIA"

#Get holidays
holidays=get_holidays(municipality, start_date, stop_date, cur)

#Set up list of normal day and zone days for Philadelphia.  Philadelphia uses 5 zones, and shifts down by one on holidays.
normal_days=[1, 2, 3, 4, 5]
zone_days=[1, 2, 3, 4, 5]

#Find recycling schedule, (period=1)
service="RECYCLE"
period=1
set_schedule(municipality, service, period, date, last_date, total_weeks, holidays, "DOWN", normal_days, zone_days, cur)

#Find recycling schedule, (period=1)
service="TRASH"
period=1
set_schedule(municipality, service, period, date, last_date, total_weeks, holidays, "DOWN", normal_days, zone_days, cur)

#Find recycling schedule, (period=1)
service="YARD"
period=1
set_schedule(municipality, service, period, date, last_date, total_weeks, holidays, "DOWN", normal_days, zone_days, cur)
