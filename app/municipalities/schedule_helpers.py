import datetime

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

#Get the day for service for municipalities with weekly schedules
def get_simple_day(day, holiday_weeks, pickups, shift):
    '''Return days until next pickup'''
    #Validate shift
    sh = shift.upper()
    if sh not in ["UP", "DOWN", "SKIP", "SKIP_DOWN", "INNER"]:
        raise ValueError("Illegal shift in get_simple_day shift: " + shift)

    this_week, next_week, following_week = holiday_weeks 

    #Test for illegal input values
    if day not in range(1, 8):
        raise ValueError("get_simple_day illegal value day: ", day)
    if this_week not in range(0, 8):
        raise ValueError("get_simple_day illegal value this_week: ", this_week)
    if next_week not in range(0, 8):
        raise ValueError("get_simple_day illegal value next_week: ", next_week)
    if following_week not in range(0, 8):
        raise ValueError("get_simple_day illegal value following_week: ", following_week)
    if len(pickups) not in range(1, 8) or not all(isinstance(i, int) for i in pickups) or min(pickups) not in range(1, 8) or max(pickups) not in range(1, 8):
        raise ValueError("get_simple_day illegal value pickups: ", pickups)
    if sh == "INNER" and 3 in pickups:
        raise ValueError("Cannot have Wed pickup in INNER logic")

    #For a normal week with remaining pickup shift doesn't matter
    if this_week == 0:
        #Return remaining pick this week if any
        trial = get_sublist(day, pickups, "GE")
        if trial:
            return trial[0] - day

    #UP means shift pickup on holiday forward, leave other days the same.
    if sh == "UP":
        #Holiday this week with remaining pickup
        if this_week > 0:
            #Return pick this week if any >= to day and < holiday
            trial = get_sublist(day, get_sublist(this_week, pickups, "LT"), "GE")
            #Return pickups >= to day and > holiday
            retrial = get_sublist(day, get_sublist(this_week, pickups, "GT"), "GE")
            #Pickup before holiday unaffected by the shift
            if trial:
                return trial[0] - day
            #Pickup on day of holiday shifted forward by a day so test if it's past
            if this_week in pickups and this_week - day - 1 >= 0:
                return this_week - day - 1
            #Pickup on days after holiday not affected
            if retrial:
                return retrial[0] - day

        #No remaining pickup, next week is normal
        if next_week == 0:
            return pickups[0] + 7 - day

        #No remaining pickup, next week is a holiday
        trial = get_sublist(next_week, pickups, "LT")
        retrial = get_sublist(next_week, pickups, "GE")
        #Pickup before the holiday?
        if trial:
            return trial[0] + 7 - day
        #Pickup on day of holiday shifted forward by a day
        if next_week in pickups:
            return next_week +7 - day - 1
        #Pickup after holiday, so not affected
        return retrial[0] + 7 - day
       
    #DOWN means shift pickups from holiday on one day later.
    if sh == "DOWN":
        #Holiday this week with remaining pickup
        if this_week > 0:
            #Find shifted pickups
            shifted = [inc_if(i, this_week, "ADD") for i in pickups]
            trial = get_sublist(day, shifted, "GE")
            if trial:
                return trial[0] - day 

        #No remaining pickup, next week is normal
        if next_week == 0:
            return pickups[0] + 7 - day

        #No remaining pickup, next week is a holiday
        shifted = [inc_if(i, next_week, "ADD") for i in pickups]
        return shifted[0] + 7 - day

    #SKIP means drop this pickup on a holiday week
    if sh == "SKIP":
        #Holiday this week with remaining pickup
        if this_week > 0:
            #Return pick this week if any >= to day and < holiday
            trial = get_sublist(day, get_sublist(this_week, pickups, "LT"), "GE")
            #Return pickups >= to day and > holiday
            retrial = get_sublist(day, get_sublist(this_week, pickups, "GT"), "GE")
            #Pickup unaffected by the shift
            if trial:
                return trial[0] - day
            #Pickup after the shift that works taking into account the "DOWN" shift
            if retrial:
                return retrial[0] - day

        #No remaining pickup, next week is normal
        if next_week == 0:
            return pickups[0] + 7 - day

        #No remaining pickup, next week is a holiday
        trial = get_sublist(next_week, pickups, "LT")
        retrial = get_sublist(next_week, pickups, "GT")
        #Pickup before the holiday?
        if trial:
            return trial[0] + 7 - day
        #Pickup affected by holiday, so apply the shift
        if retrial:
           return retrial[0] + 7 - day

        #Failed to find a date next week, so try following week
        if following_week == 0:
            return pickups[0] + 7 - day

        trial = get_sublist(following_week, pickups, "LT")
        retrial = get_sublist(following_week, pickups, "GT")
        #Pickup before the holiday?
        if trial:
            return trial[0] + 14 - day
        #Pickup affected by holiday, so apply the shift
        if retrial:
            return retrial[0] + 14 - day

        #Failed to find pickup in 3 weeks, so raise an exception
        raise ValueError('Failed to find pickup date in SKIP logic')

    #SKIP_DOWN means skip pickup on a holiday week, unless it would also be skipped the next week.  If so do the pick up one day later.
    if sh == "SKIP_DOWN":

        #If this week is normal and so is next week, use normal logic
        if this_week == 0 and next_week == 0:
            return pickups[0] + 7 - day

        #If this week is a holiday and next week is normal, use the SKIP logic
        if this_week > 0 and next_week == 0:        
            shifted = [i for i in pickups if i != this_week]
            #Return pick this week if any >= to day and < holiday
            trial = get_sublist(day, shifted, "GE")
            if trial:
                return trial[0] - day
            else:
                return pickups[0] + 7 - day

        #If this week is a holiday and so is next week, use DOWN logic this week if there would not be a pickup next week
        if this_week > 0 and next_week > 0:
            #SKIP shift for this week
            shifted = [i for i in pickups if i != this_week]
            #SKIP shift for next week
            second_shifted = [i for i in pickups if i != next_week]
            #DOWN shift for this week
            down_shifted = [inc_if(i, this_week, "ADD") for i in pickups]

            #Pickups left under SKIP shift this week 
            trial = get_sublist(day, shifted, "GE")
            #Pickups left under DOWN shift this week
            retrial =  get_sublist(day, down_shifted, "GE")

            #Is there a SKIP logic pickup this week?
            if trial:
                return trial[0] - day
            #Is there a pickup next week? Then the SKIP logic applies so the first pick up next week obtains
            if second_shifted:
                return second_shifted[0] + 7 - day
            #There's no pickup next week, so check if there's one left this week under DOWN logic
            if retrial:
                return retrial[0] - day
            #The next pickup is the following week, which should be a normal week
            if following_week == 0:
                return pickups[0] + 14 - day
            #If it is a holiday week, raise an error
            raise ValueError("Cannot have three holiday weeks in a row in SKIP_DOWN logic: " + str(this_week) + " " + str(next_week) + " " + str(following_week)) 

        #If this week is a normal week and next week is a holiday week. We know there isn't a pickup this week, so it's either next week or the week after.
        if this_week == 0 and next_week > 0:
            #SKIP shift for next week
            shifted = [i for i in pickups if i != next_week]
            #SKIP shift for following week
            second_shifted = [i for i in pickups if i != following_week]
            #DOWN shift for this next_week
            down_shifted = [inc_if(i, next_week, "ADD") for i in pickups]

            if shifted:
                return shifted[0] + 7 - day
            if second_shifted:
                return second_shifted[0] + 14 - day
            return down_shifted[0] + 7 - day

    #INNER means shift toward middle of the week.  Cannot have Wed as a pickup
    if sh == "INNER":
        #If holiday is on Wed, pickups are not affected so see if there's one that works
        if this_week == 3:
            trial = get_sublist(day, pickups, "GE")
            if trial:
                return trial[0] - day

        #Pickups before & after Wed
        before = get_sublist(3, pickups, "LT")
        after = get_sublist(3, pickups, "GT")

        #Holiday this week with remaining pickup
        if this_week > 0:
            #Make a shifted pickup list
            shifted = [inc_if(d, this_week, "ADD") for d in before] + [inc_if(d, this_week, "SUB") for d in after]

            #See if one works
            trial = get_sublist(day, shifted, "GE")
            if trial:
                return trial[0] - day
            
        #No remaining pickup, next week is normal
        if next_week == 0:
            return pickups[0] + 7 - day

        #No remaining pickup, next week is a holiday.  Make a shifted pickup list and return the first pickup
        shifted = [inc_if(d, next_week, "ADD") for d in before] + [inc_if(d, next_week, "SUB") for d in after]
        return shifted[0] + 7 - day

#Find the schedule where period is the frequency of service, (1 for weekly, 2 for every other week), and holiday shift logic, ("UP", "DOWN", "LM")
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
        if day == 1:
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

def set_simple_schedule(municipality, service, date, last_date, total_weeks, holidays, zone, shift, cur):
    '''Set schedule for municipalities where zone contains all the required information, (does not also require days information)'''
  
    #Loop over weeks
    for weeks in range (1, total_weeks):
        for day in range (1, 8):
            date = date + datetime.timedelta(days=1)
        
            #Check if date is in range
            if date>last_date:
               return

            #Check for holiday week on Mondays
            if day == 1:
                #Capture date
                monday = date

                #Check if this week is a holiday
                this_week = holiday_week(date, holidays)

                #Check if next week is a holiday
                next_week = holiday_week(date + datetime.timedelta(days=7), holidays)
                
                #Check if following week is a holiday
                following_week = holiday_week(date + datetime.timedelta(days=14), holidays)
                
                holiday_weeks = (this_week, next_week, following_week)
                
            #Get pickup day information from zone.  Zone should start with "_".  Convert remaining elements to integers. 
            if zone[0] == '_':
                pickups = [int(pickup) for pickup in list(zone)[1:]]
            else:
                raise ValueError("Zone must begin with underscore: " + zone)
            days_to_pickup = get_simple_day(day, holiday_weeks, pickups, shift)
            #next_day = monday + datetime.timedelta(days=days_to_pickup)
            next_day = date + datetime.timedelta(days=days_to_pickup)

            #Insert record into app_schedule table
            set_record(cur, municipality, service, date.strftime("%Y-%m-%d"), zone, day, this_week, next_day.strftime("%Y-%m-%d"), str(days_to_pickup))

def get_sublist(x, list_, compare):
    '''Return sorted list of elements in list_ <=, <, >=, > than x'''
    com = compare.upper()
    if com not in ["LE", "LT", "GE", "GT"]:
        raise ValueError("Illegal comparator: " + compare)
    tail = sorted(list_)
    result = []
    
    while tail:
        head, tail = tail[0], tail[1:]
        if (com == "LT" and head < x) or (com == "LE" and head <= x) or (com == "GT" and head > x) or (com == "GE" and head >= x):
            result.append(head)

    return result

def inc_if(x, val, shift):
    sh = shift.upper()
    if sh not in ["ADD", "SUB"]:
        raise ValueError("inc_if encountered illegal shift: " + sh)
    if sh == "ADD" and x >= val:
        return x + 1
    if sh == "SUB" and x <= val:
        return x - 1
    return x

def zone_combinations(days, min_number, max_number):
    import itertools

    result = []
    for l in range(min_number, max_number+1):
        for subset in itertools.combinations(days, l):
            ls_ = [str(element) for element in subset]

            result.append("_" + ''.join(ls_))

    return result 
