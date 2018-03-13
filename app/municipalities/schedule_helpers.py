#import urllib, urllib2
#import re
import datetime
#import MySQLdb
#from address import AddressParser, address

########################################################################################################################################################################
#  Subroutines independent of municipality
########################################################################################################################################################################

#Get the day number from the day text
def get_day_number(day_text):
	if (day_text == "Monday" or day_text=="Mon" or day_text == "MONDAY" or day_text=="MON"):
		return 1
	if (day_text == "Tuesday" or day_text == "Tue" or day_text == "TUESDAY" or day_text == "TUE"):
		return 2
	if (day_text == "Wednesday" or  day_text == "Wed" or day_text == "WEDNESDAY" or  day_text == "WED"):
		return 3
	if (day_text == "Thursday" or  day_text == "Thu" or day_text == "THURSDAY" or  day_text == "THU"):
		return 4
	if (day_text == "Friday" or day_text == "Fri" or day_text == "FRIDAY" or day_text == "FRI"):
		return 5
	if (day_text == "Saturday" or day_text == "Sat" or day_text == "SATURDAY" or day_text == "SAT"):
		return 6
	if (day_text == "Sunday" or  day_text == "Sun" or day_text == "SUNDAY" or  day_text == "SUN"):
		return 7
	return 0


#Read out holidays from database
def get_holidays(municipality, start_date, stop_date, cur):

    #Execute query
    cur.execute("select date from app_holiday_list as l inner join app_holidays as h on l.name=h.name where municipality=%s and date>=%s and date<=%s order by date", (municipality, start_date, stop_date))

    holiday_list=[]
    rows = cur.fetchall()
    for row in rows:
    	holiday_list.append(row[0].strftime("%Y-%m-%d"))

    return holiday_list

#Write record into database
def set_record(cur, municipality, service, date, zone, day, holiday, next_date, days_to_pickup):
		cur.execute( 'insert into app_schedule (municipality, service, date, zone, day, holiday, next_date, days_to_pickup) values(%s, %s, %s, %s, %s, %s, %s, %s)', 
				(municipality, service, date, zone, day, holiday, next_date, days_to_pickup) )

#Return 0 if not a holiday week, otherwise return day of week of the holiday
def holiday_week(date, holidays):
    #Check if this week is a holiday week
    for holiday in holidays:
	    	
	#Make a datetime object
	holiday_date=datetime.datetime.strptime(holiday, "%Y-%m-%d")

	#Find difference between holiday_date and date
	date_diff = holiday_date - date

	if date_diff.days >= 0 and date_diff.days < 5:
	    #Holiday week! Figure out day of week for holiday and then break
	    holiday_day_of_week = 1+date_diff.days
	    break
	else:
	    #Normal week, set holiday day of week to 0
	    holiday_day_of_week = 0

    return holiday_day_of_week

#Get the day for service  for municipalities using UP or DOWN or LM (Lower Merion) holiday logic 
def get_day(holiday, normal_day, zone_number, shift):
    #Pick up next day if holiday
    if shift=="DOWN":
    	if holiday==0 or normal_day<holiday:
	    return normal_day
    	else:
	    return normal_day+1
    #Pick up preceding day if holiday
    elif shift=="UP":
    	if holiday==0 or normal_day>holiday:
	    return normal_day
    	else:
	    return normal_day-1
    #Use LM holiday map
    elif shift=="LM":
    	if holiday==0:
	    return normal_day
	#Shift back if begining of the week
    	if zone_number<3:
	    if holiday<=zone_number:
	    	return zone_number+1
	    else:
	    	return zone_number
	#Shift up if end of week
    	else:
	    if holiday>zone_number:
	    	return zone_number
	    else:
	    	return zone_number+1
    #Error if not "UP" or "DOWN" or "LM"
    else:
	message = "Error in get_day shift = " + shift
	exit(message)

#Find the schedule where period is the frequncy of service, (1 for weekly, 2 for every other week), and holiday shift logic, ("UP", "DOWN", "LM")
def set_schedule(municipality, service, period, date, last_date, total_weeks, holidays, shift, normal_days, zone_days, cur):

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
	    this_week=holiday_week(date, holidays)

	    #Check if next week is a holiday
	    next_week=holiday_week(date + datetime.timedelta(days=7), holidays)

	    #Check if following week is a holiday
	    following_week=holiday_week(date + datetime.timedelta(days=14), holidays)

   	#Loop over zones and days
	for letter in zone_letters:
	    for normal_day in normal_days:
		for zone_day in zone_days:
		
		    #If period is 2, is this an on week or off week?
	            if week_label != letter:
		        #Not a recycling week, so find recycle day next week.  Only occurs if period=2.
		        recycle_day = get_day(next_week, normal_day, zone_day, shift)
		        days_ahead = 7 + recycle_day -1
		    
		    else:
		        #It is a recycling week.
		        recycle_day = get_day(this_week, normal_day, zone_day, shift)

		        #Is the day past?
		        if day<=recycle_day:
			    #Still good
		            days_ahead = recycle_day -1
		        else:
			    if period==2:
			        #Day past, so find day 2 weeks ahead
		                recycle_day = get_day(following_week, normal_day, zone_day, shift)
		                days_ahead = 14 + recycle_day -1
			    elif period==1:
			        #Day past, so find day 1 week ahead
		                recycle_day = get_day(next_week, normal_day, zone_day, shift)
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
		        zone_str=letter+str(zone_day)
		    else:
		        zone_str=str(zone_day)
	
		    #Insert record into app_schedule table
		    set_record(cur, municipality, service, date.strftime("%Y-%m-%d"), zone_str, normal_day, this_week, next_day.strftime("%Y-%m-%d"), str(days_to_pickup))

