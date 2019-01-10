from __future__ import print_function
import urllib
import re
import datetime
import MySQLdb
from time import sleep
import sys, os
sys.path.append(os.path.dirname(__file__))

import municipalities.lower_merion
import municipalities.philadelphia
from cities.cities import Cities
from cities.dc import DC
from cities.nyc import NYC

########################################################################################################################################################################
#  Subroutines independent of municipality
########################################################################################################################################################################

#Get day text from day number
def get_day_text(day_number):
        if day_number == 1:
                return "Monday"
        if day_number == 2:
                return "Tuesday"
        if day_number == 3:
                return "Wednesday"
        if day_number == 4:
                return "Thursday"
        if day_number == 5:
                return "Friday"
        if day_number == 6:
                return "Saturday"
        if day_number == 7:
                return "Sunday"

#Compose confirmatory message to subscribers
def confirm_subscription(masked_key, first_name, last_name, alert_day, alert_time, email_alert, sms_alert):
        #What kind of alert?
        if email_alert == True and sms_alert == True:
                alert_message="text and email"
        elif email_alert == True and sms_alert == False:
                alert_message="email"
        elif email_alert == False and sms_alert == True:
                alert_message="text"
        else:
                #If no match, then failed
                return

        #What day?
        if alert_day==0:
                day_message="on pickup day"
        else:
                day_message="the day before pickup day"
        
        message = "Please click or visit https://recyclobuddy.com/app/confirm_" + masked_key + " to confirm that "        
        message = message + first_name + " "+ last_name + " wants " + alert_message + " alerts sent " + day_message + " at " + str(alert_time) + "." 

        return message

#Set up database connection
def get_database():
    #Set up import of information from mysite package in parallel directory
    import sys, os
    sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
    from mysite.passwords import MYSQL_HOST, MYSQL_PORT, MYSQL_NAME, MYSQL_USER, MYSQL_PASSWORD

    db=MySQLdb.connect(host=MYSQL_HOST, port=MYSQL_PORT, db=MYSQL_NAME, user=MYSQL_USER , passwd=MYSQL_PASSWORD)
    cur=db.cursor()
    return cur

#Set up database connection with dictionary cursor
def get_database_dictionary():
    #Set up import of information from mysite package in parallel directory
    import sys, os
    sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
    from mysite.passwords import MYSQL_HOST, MYSQL_PORT, MYSQL_NAME, MYSQL_USER, MYSQL_PASSWORD

    db=MySQLdb.connect(host=MYSQL_HOST, port=MYSQL_PORT, db=MYSQL_NAME, user=MYSQL_USER, passwd=MYSQL_PASSWORD)
    cur=db.cursor(MySQLdb.cursors.DictCursor)
    return cur

#Set up database connection with dictionary cursor
def get_database_connections():
    #Set up import of information from mysite package in parallel directory
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
    from mysite.passwords import MYSQL_HOST, MYSQL_PORT, MYSQL_NAME, MYSQL_USER, MYSQL_PASSWORD

    db = MySQLdb.connect(host=MYSQL_HOST, port=MYSQL_PORT, db=MYSQL_NAME, user=MYSQL_USER, passwd=MYSQL_PASSWORD)
    cur = db.cursor()
    dict_cur=db.cursor(MySQLdb.cursors.DictCursor)
    return cur, dict_cur, db

#Make a dictionary of abbreviations from database table
def get_dictionary(key):
    query = "select name, abbreviation from abbreviations where type='%s'" % (key)
    cur = get_database_dictionary()
    cur.execute(query)
    dict = {row['name'].title(): row['abbreviation'].title() for row in cur.fetchall()}
    cur.close()
    return dict

STREETS = get_dictionary("street")
DIRECTIONS = get_dictionary("direction")

#Make re pattern for matching addresses
def make_pattern():
    street_pattern = "|".join(STREETS.keys())
    direction_pattern = r"\s|".join(DIRECTIONS.keys()) + r"\s"
    pattern = r'^([0-9]+[a-zA-Z]?)\s(' + direction_pattern + r')?([a-zA-Z0-9][a-zA-Z0-9\s]*?)\s(' + street_pattern + r')$'
    return pattern

PATTERN = make_pattern()

def parse_address(address_string, municipality):
    '''Read in user form for address and return USPS format in title case. Return empty string on failed match'''
    from re import match, sub

    #Strip out periods, apostrophes and multiple spaces.  Remove leading and trailing white space. Put in upper case
    address = address_string.strip()
    address = sub('\.', '', address)
    address = sub("'", "", address)
    address = address.title()
    cleaned = " ".join(address.split())

    #Try to match the pattern. In DC skip the parser, use theirs
    if (municipality == "DC"):
        return 0, address
    else:
        match_object = match(PATTERN, cleaned)
    if match_object:
        try:
            house_number = match_object[1]
            direction = match_object[2]
            street_name = match_object[3]
            street = match_object[4]
        except TypeError:
            house_number = match_object.group(1)
            direction = match_object.group(2)
            street_name = match_object.group(3)
            street = match_object.group(4)

        if direction:
            return 0, "%s %s %s %s" %(house_number.strip(), DIRECTIONS[direction.strip()], street_name.strip(), STREETS[street.strip()])
        else:
            return 0, "%s %s %s" %(house_number.strip(), street_name.strip(), STREETS[street.strip()])

    else:
        return 1, "Sorry, we need street identifier like St, Rd or Ave.  Please fill in more of the street address but no apartment number (if any)."

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

#Make a url key from primary key and permutation key
def convert(n):
    #Set up import of information from mysite package in parallel directory
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
    from mysite.passwords import PERM_KEY

    l = len(PERM_KEY)
    if n < 0 or l < 2:
        return ''
    if n < l:
        return PERM_KEY[n]
    values = []
    while n > 0:
        res = n % l
        values.append(PERM_KEY[res])
        n = (n - res) // l
    return ''.join(values[::-1])

#Refresh subscriber database.  Requires dictionary cursor.
def refresh_subscriber(dict_cur):
    #Query contacts table for subscribers
    dict_cur.execute('''select index_key, prefix, first_name, middle_name, last_name, suffix, address, address2, city, state, zip, municipality, a.email, a.mobile, carrier, 
                recycle_zone, trash_zone, yard_zone, recycle_day, trash_day, yard_day, alert_time, alert_day, email_alert, sms_alert, subscribe, creation 
                        from app_contacts as a inner join ( select email, mobile, max(creation) as max_creation from app_contacts group by email, mobile) as b
                                on a.email=b.email and a.mobile=b.mobile and a.creation=max_creation''') 

    #Loop over results
    rows = dict_cur.fetchall()
    for row in rows:
        result = row
        key = convert(row["index_key"])

        #insert row into subscriber table with email and mobile as primary keys
        dict_cur.execute('''insert into subscribers (prefix, first_name, middle_name, last_name, suffix, address, address2, city, state, zip, municipality, email, mobile, carrier, 
                recycle_zone, trash_zone, yard_zone, recycle_day, trash_day, yard_day, alert_time, alert_day, email_alert, sms_alert, subscribe, creation, market_key)
                        values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                                on duplicate key update 
                                        prefix=values(prefix), 
                                        first_name=values(first_name), 
                                        middle_name=values(middle_name), 
                                        last_name=values(last_name), 
                                        suffix=values(suffix), 
                                        address=values(address), 
                                        address2=values(address2), 
                                        city=values(city), 
                                        state=values(state), 
                                        zip=values(zip), 
                                        municipality=values(municipality), 
                                        carrier=values(carrier), 
                                        recycle_zone=values(recycle_zone), 
                                        trash_zone=values(trash_zone), 
                                        yard_zone=values(yard_zone), 
                                        recycle_day=values(recycle_day), 
                                        trash_day=values(trash_day), 
                                        yard_day=values(yard_day), 
                                        alert_time=values(alert_time), 
                                        alert_day=values(alert_day), 
                                        email_alert=values(email_alert), 
                                        sms_alert=values(sms_alert), 
                                        subscribe=values(subscribe),
                                        creation=values(creation),
                                        market_key=values(market_key); ''', 
                        (row["prefix"], row["first_name"], row["middle_name"], row["last_name"], row["suffix"], row["address"], row["address2"], row["city"], row["state"], row["zip"], row["municipality"], 
                                row["email"],row["mobile"], row["carrier"], row["recycle_zone"], row["trash_zone"], row["yard_zone"], row["recycle_day"], 
                                        row["trash_day"], row["yard_day"], row["alert_time"], row["alert_day"], row["email_alert"], row["sms_alert"], row["subscribe"], row["creation"], key) )

#Insert results into the messages table
def insert_messages(dict_cur):
    #Loop over results
    rows = dict_cur.fetchall()
    for row in rows:
        result = row

        #insert row into messages table with email, mobile and service as primary keys
        dict_cur.execute('''insert into messages (prefix, first_name, middle_name, last_name, suffix, address, address2, city, state, zip, municipality, email, mobile, carrier, 
                service, alert_time, alert_day, email_alert, sms_alert) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s); ''', 
                        (row["prefix"], row["first_name"], row["middle_name"], row["last_name"], row["suffix"], row["address"], row["address2"], row["city"], row["state"], row["zip"], row["municipality"], 
                                row["email"],row["mobile"], row["carrier"], row["service"], row["alert_time"], row["alert_day"], row["email_alert"], row["sms_alert"]) )

#Get the services
def get_services(email, mobile, dict_cur):
    #Create list for services
    services=[]

    #Query messages table for services with this email and mobile.  Primary keys are email, moblie and service.
    dict_cur.execute('select service from messages where email=%s and mobile=%s', (email, mobile)) 

    #Make a list of the services
    rows = dict_cur.fetchall()
    for row in rows:
        services.append(row["service"])

    return services

#Translate services into nicer form
def translate_service(service):
    if service=="RECYCLE":
        return "recycle"
    elif service=="TRASH":
        return "trash"
    elif service=="YARD":
        return "leaf"
    elif service=="XMAS":
        return "Xmas Tree"
    elif service=="HAZ":
        return "haz waste"
    else:
        return

#Compose the message
def compose_message(prefix, first_name, middle_name, last_name, suffix, address, address2, city, state, zip, municipality, alert_day, services, sponsor_message): 
    #Get length of services list.  Return null if error.
    if services:
        length_services=len(services)
        if length_services == 0 or length_services > 5:
            return

    #Get today or tomorrow.  Return null if error.
    if alert_day == 0:
        tag="Today: "
    elif alert_day == 1:
        tag="Tomorrow: "
    else:
        return

    #Compose the message
    if length_services == 1:
        message = tag + translate_service(services[0]) + ' | '
    elif length_services==2:
        message = tag + translate_service(services[0]) + ' & ' + translate_service(services[1]) + ' | '
    elif length_services==3:
        message = tag + translate_service(services[0]) + ', ' + translate_service(services[1]) + ' & ' + translate_service(services[2]) + ' | '
    elif length_services==4:
        message = tag + translate_service(services[0]) + ', ' + translate_services(service[1]) + ', ' + translate_service(services[2]) + ' & ' + translate_service(services[3]) + ' | '
    else:
        message = tag + translate_services(service[0]) + ', ' + translate_services(service[1]) + ', ' + translate_services(service[2]) + ', ' + translate_service(services[3]) + ' & ' + translate_services(service[4]) + ' | '

    return message + sponsor_message

#Compose sponsor message
def compose_sponsor(email, mobile, dict_cur):
    #Set up import of information from mysite package in parallel directory
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
    from mysite.passwords import BASE_URL, OPT_OUT

    #Check for sponsor message for this email, mobile and date
    dict_cur.execute('select sponsor_message, campaign from sponsors where email=%s and mobile=%s and date<=date(convert_tz(now(), "GMT", "US/Eastern")) and date(convert_tz(now(), "GMT", "US/Eastern"))<date_add(date, interval 7 day)', (email, mobile)) 
    
    #There should only be 1 result at most. If there is a sponsor message and campaign, build the url and market key.  If there is a message but no campaign, don't append any url.
    #If there isn't any sponsor information at all, append the default url and market key.
    row = dict_cur.fetchone()
    if row:
        if row["campaign"]:
            sponsor_message = row["sponsor_message"] + " " + BASE_URL + "/" + row["campaign"]
        else:
            return row["sponsor_message"]
    else:
        sponsor_message = OPT_OUT

    #Get market_key for this email, mobile
    dict_cur.execute('select market_key from subscribers where email=%s and mobile=%s', (email, mobile)) 
    
    #There should only be 1 result at most
    row = dict_cur.fetchone()
    if row:
        key = row["market_key"]
        sponsor_message = sponsor_message + "/" + key

    return sponsor_message

#Compose special message
def compose_special(email, mobile, dict_cur):
    #Check for emergency messages for this municipality, date and zone
    date=datetime.date.today()
    #Query messages table for services with this email and mobile.  Primary keys are email, moblie and service.
    dict_cur.execute('select service from messages where email=%s and mobile=%s', (email, mobile)) 


#Insert combined message
def insert_combined_messages(email, mobile, carrier, alert_time, email_alert, sms_alert, subject, message, dict_cur): 
    dict_cur.execute('insert into combined_messages (email, mobile, carrier, alert_time, email_alert, sms_alert, subject, message) values (%s, %s, %s, %s, %s, %s, %s, %s); ', 
                (email, mobile, carrier, alert_time, email_alert, sms_alert, subject, message) )

#Compose broadcast message 
def broadcast_message(dict_cur, selected_municipality, start, run_time, subject, inserted_message, use_key, campaign=None):
    '''Skip broadcast message if there is already a message queue for that subscriber'''

    #Set up import of information from mysite package in parallel directory
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
    from mysite.passwords import BASE_URL, OPT_OUT

    if use_key:
        dict_cur.execute('''insert ignore into combined_messages (email, mobile, carrier, alert_time, email_alert, sms_alert, subject, message) 
            select email, mobile, carrier, time(date_add(%s, interval floor(%s*rand()) second)), email_alert, sms_alert, %s, concat(%s, " ", %s, "/", %s, "/", market_key) from subscribers
            where subscribe=1 and market_key is not null and municipality=%s''', (start, run_time, subject, inserted_message, BASE_URL, campaign, selected_municipality)) 
    else:
        dict_cur.execute('''insert ignore into combined_messages (email, mobile, carrier, alert_time, email_alert, sms_alert, subject, message) 
            select email, mobile, carrier, time(date_add(%s, interval floor(%s*rand()) second)), email_alert, sms_alert, %s, concat (%s, " ", %s) from subscribers
            where subscribe=1 and municipality=%s''', (start, run_time, subject, inserted_message, OPT_OUT, selected_municipality)) 

#Refresh messages database.  Requires dictionary cursor.
def refresh_messages(dict_cur):
    #Set up import of information from mysite package in parallel directory
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
    from mysite.passwords import SUBJECT_ALERT, SUBJECT_BROADCAST

    #First: Gather all the messages for the day in the messages table

    #Clear the messages table
    dict_cur.execute('delete from messages')

    #Query find recycling
    dict_cur.execute('''select prefix, first_name, middle_name, last_name, suffix, address, address2, city, state, zip, s1.municipality, email, mobile, carrier, 
                service, alert_time, alert_day, email_alert, sms_alert 
                        from subscribers as s1 inner join app_schedule as s2 on recycle_zone=zone and recycle_day=day and s1.municipality=s2.municipality 
                                        where days_to_pickup=alert_day and date=date(convert_tz(now(), "GMT", "US/Eastern")) and service="RECYCLE" and subscribe=True''') 
    insert_messages(dict_cur)
    
    #Query find trash
    dict_cur.execute('''select prefix, first_name, middle_name, last_name, suffix, address, address2, city, state, zip, s1.municipality, email, mobile, carrier, 
                service, alert_time, alert_day, email_alert, sms_alert 
                        from subscribers as s1 inner join app_schedule as s2 on trash_zone=zone and trash_day=day and s1.municipality=s2.municipality 
                                        where days_to_pickup=alert_day and date=date(convert_tz(now(), "GMT", "US/Eastern")) and service="TRASH" and subscribe=True''') 
    insert_messages(dict_cur)
    
    #Query find YARD
    dict_cur.execute('''select prefix, first_name, middle_name, last_name, suffix, address, address2, city, state, zip, s1.municipality, email, mobile, carrier, 
                service, alert_time, alert_day, email_alert, sms_alert 
                        from subscribers as s1 inner join app_schedule as s2 on yard_zone=zone and yard_day=day and s1.municipality=s2.municipality 
                                        where days_to_pickup=alert_day and date=date(convert_tz(now(), "GMT", "US/Eastern")) and service="YARD" and subscribe=True''') 
    insert_messages(dict_cur)

    #Second:  Combine the messages together in the combined_messages table and compose the message
    
    #Clear the messages table
    dict_cur.execute('delete from combined_messages')

    #Query find everything but service from messages
    dict_cur.execute('''select prefix, first_name, middle_name, last_name, suffix, address, address2, city, state, zip, municipality, email, mobile, carrier, alert_time, alert_day, email_alert, sms_alert 
                        from messages group by email, mobile''') 
    
    #Loop over results
    rows = dict_cur.fetchall()
    for row in rows:
        result = row
        #Get the services
        services=get_services(row["email"], row["mobile"], dict_cur)

        #Get the sponsor message
        sponsor_message=compose_sponsor(row["email"], row["mobile"], dict_cur)

        #Compose the message
        message=compose_message(row["prefix"], row["first_name"], row["middle_name"], row["last_name"], row["suffix"], 
                        row["address"], row["address2"], row["city"], row["state"], row["zip"], row["municipality"], row["alert_day"], services, sponsor_message) 
        
        #Insert combined message
        if message:
                insert_combined_messages(row["email"], row["mobile"], row["carrier"], row["alert_time"], row["email_alert"], row["sms_alert"], SUBJECT_ALERT, message, dict_cur) 
        else:
                print ("Failed to find message\n")

    #Insert broadcast messages
    dict_cur.execute('''select municipality, start, run_time, use_key, message, campaign from broadcast where date(start)=date(convert_tz(now(), "GMT", "US/Eastern"))''')
    rows = dict_cur.fetchall()
    for row in rows:
        broadcast_message(dict_cur, row['municipality'], row['start'], row['run_time'], SUBJECT_BROADCAST, row['message'], row['use_key'], row['campaign'])

#Make an sms address            
def make_sms_address(carrier, mobile):
   if carrier=="VER":
        return mobile+"@vtext.com"
   elif carrier=="ATT":
        return mobile+"@txt.att.net"
   elif carrier=="SPR":
        return mobile+"@messaging.sprintpcs.com"
   elif carrier=="TMO":
        return mobile+"@tmomail.net"
   elif carrier=="USC":
        return mobile+"@email.uscc.net"
   elif carrier=="VRG":
        return mobile+"@vmobl.com"
   elif carrier=="GOO":
        return mobile+"@msg.fi.google.com"
   elif carrier=="CRK":
        return "1" + mobile + "@mms.cricketwireless.net"
   else:
        return

#Write logfile message
def write_log_message(status, iteration, f, address, message):
    if status=="attempt":
        if f:
            print ("Sending to " + address + " message: " + message, file=f)
        else:
            print ("Sending to " + address + " message: " + message)

    elif status=="success":
        if f:
            print ("Success sending to " + address + " message: " + message, file=f)
        else:
            print ("Success sending to " + address + " message: " + message)

    elif status=="connect_success":
        if f:
            print ("Success connecting to " + address + " message: " + message, file=f)
        else:
            print ("Success connecting to " + address + " message: " + message)

    elif status=="login_success":
        if f:
            print ("Success logging in to " + address + " message: " + message, file=f)
        else:
            print ("Success logging in to " + address + " message: " + message)

    elif status=="quit_success":
        if f:
            print ("Success quitting " + address + " message: " + message, file=f)
        else:
            print ("Success quitting " + address + " message: " + message)

    elif status=="failure":
        if f:
            print ("Failed attempt sending to " + address + " message: " + message, file=f)
        else:
            print ("Failed attempt sending to " + address + " message: " + message)

    elif status=="connect_failure":
        if f:
            print ("Failed attempt connecting to " + address + " message: " + message, file=f)
        else:
            print ("Failed attempt connecting to " + address + " message: " + message)

    elif status=="disconnect_failure":
        if f:
            print ("Server disconnected sending to " + address + " message: " + message, file=f)
        else:
            print ("Server disconnected sending to " + address + " message: " + message)

    elif status=="login_failure":
        if f:
            print ("Failed attempt logging into " + address + " message: " + message, file=f)
        else:
            print ("Failed attempt logging into " + address + " message: " + message)

    elif status=="quit_failure":
        if f:
            print ("Failed quitting " + address + " message: " + message, file=f)
        else:
            print ("Failed quitting " + address + " message: " + message)

    else:
        if f:
            print ("Error in write_log_message: Encountered illegal status: " + status, file=f)
        else:
            print ("Error in write_log_message: Encountered illegal status: " + status)

#Fire messages from combined+messages table with alert_time close enough to time_gap
def fire_messages(dict_cur, time_gap, f):
    import smtplib, time
    import email.mime.text
    #Date header information from blog.magiksys.net/generate-and-send-mail-with-python-tutorial
    import email.utils

    #Set up import of information from mysite package in parallel directory
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
    from mysite.passwords import EMAIL_SERVER, EMAIL_PORT, EMAIL_USER, EMAIL_PASSWORD, EMAIL_SENDER, STRIP

    time_str = str(time_gap)
    TZ = "US/Eastern"
    local = 'time(convert_tz(curtime(), "GMT", "%s"))' % (TZ) 
    add = 'addtime(alert_time, %s)' % (time_str)
    #Find messages in range
    query = 'select email, mobile, carrier, alert_time, email_alert, sms_alert, subject, message from combined_messages where alert_time < %s and %s <= %s'% (local, local, add)
    dict_cur.execute(query)

    #Send email and/or sms text message
    rows = dict_cur.fetchall()
    
    message_count = 0
    
    #If any rows are returned, set up email connection.  See stackoverflow.com/questions/984526/correct-way-of-handling-exceptions-in-python
    if rows:
        #Try to connect to host up to 5 times
        for i in range (1, 6):
            try:
                server=smtplib.SMTP(EMAIL_SERVER, EMAIL_PORT)
                #Insert this for AWS
                server.starttls()
                #Print success message and break out of loop
                write_log_message("connect_success", i, f, EMAIL_SERVER, str(EMAIL_PORT))
                break

            except (smtplib.socket.gaierror, smtplib.socket.error, smtplib.socket.herror):
                #Print failure message
                write_log_message("connect_failure", i, f, EMAIL_SERVER, str(EMAIL_PORT))
                time.sleep(2)

        #Try to login to host up to 5 times
        for i in range (1, 6):
            try:
                server.login(EMAIL_USER, EMAIL_PASSWORD)
                #Print success message and break out of loop
                write_log_message("login_success", i, f, EMAIL_USER, EMAIL_PASSWORD)
                message_count += 1
                break

            except smtplib.SMTPAuthenticationError:
                #Print failure message
                write_log_message("login_failure", i, f, EMAIL_USER, EMAIL_PASSWORD)
                time.sleep(2)

        #Send the messages to the server
        for row in rows:
            #Send email
            if row["email_alert"]==True:
                msg=email.mime.text.MIMEText(row['message'])
                msg["Subject"] = row["subject"]
                msg["From"] = EMAIL_SENDER
                msg["To"] = row["email"]
     
                #Include date to conform to spam filter requirements.  Date header information from blog.magiksys.net/generate-and-send-mail-with-python-tutorial
                utc_from_epoch=time.time()
                msg["Date"] = email.utils.formatdate(utc_from_epoch, localtime=True)
                
                #Write attempt message
                #write_log_message("attempt", 0, f, row["email"], row["message"])

                #Try to send message 5 times, with 2 second pause
                for i in range (1, 6):
                    try:
                        server.sendmail(EMAIL_SENDER, [row["email"]], msg.as_string())
                        #Print success message and break out of loop
                        write_log_message("success", i, f, row["email"], row["message"])
                        message_count += 1
                        break

                    except smtplib.SMTPServerDisconnected:
                        #Server disconnected during sending while sending list
                        write_log_message("disconnect_failure", i, f, row["email"], row["message"])

                    except Exception:
                        #Print failure message
                        write_log_message("failure", i, f, row["email"], row["message"])
                        time.sleep(5)
        
            #Send sms
            if row["sms_alert"]==True:
                sms_address=make_sms_address(row["carrier"], row["mobile"])
                if sms_address:
                    #Strip out non-essential decoration of url
                    msg=email.mime.text.MIMEText(row['message'].replace(STRIP, ""))
                     
                    msg["From"] = EMAIL_SENDER
                    msg["To"] = sms_address
                
                    #Write attempt message
                    #write_log_message("attempt", 0, f, sms_address, row["message"])

                    #Try to send message 5 times, with 2 second pause
                    for i in range (1, 6):
                        try:
                            server.sendmail(EMAIL_SENDER, sms_address, msg.as_string())
                            write_log_message("success", i, f, sms_address, row["message"])
                            break

                        except smtplib.SMTPServerDisconnected:
                            #Server disconnected during sending while sending list
                            write_log_message("disconnect_failure", i, f, row["email"], row["message"])

                        except Exception:
                            write_log_message("failure", i, f, sms_address, row["message"])
                            time.sleep(5)

        #Close connection
        try:
            server.quit()
            write_log_message("quit_success", i, f, EMAIL_USER, EMAIL_PASSWORD)
        except Exception:
            write_log_message("quit_failure", i, f, EMAIL_USER, EMAIL_PASSWORD)

    return message_count

#Cancel service
def cancel_subscription(email, mobile):

    #Set up database connection
    dict_cur=get_database_dictionary()

    #Tells if any records found
    success=False

    #Look for records that match.  First from contacts.
    dict_cur.execute('select count(*) as count from app_contacts where email = %s and mobile = %s', (email, mobile) )
    rows = dict_cur.fetchall()
    if rows:
        success=True
        dict_cur.execute('update app_contacts set subscribe=False where email = %s and mobile = %s', (email, mobile) )
    
    #Next from subscribers.
    dict_cur.execute('select count(*) as count from subscribers where email = %s and mobile = %s', (email, mobile) )
    rows = dict_cur.fetchall()
    if rows:
        success=True
        dict_cur.execute('update subscribers set subscribe=False where email = %s and mobile = %s', (email, mobile) )
    
    #Next from messages.
    dict_cur.execute('select count(*) as count from messages where email = %s and mobile = %s', (email, mobile) )
    rows = dict_cur.fetchall()
    if rows:
        success=True
        dict_cur.execute('delete from messages where email = %s and mobile = %s', (email, mobile) )
    
    #Finally from combined_messages.
    dict_cur.execute('select count(*) as count from combined_messages where email = %s and mobile = %s', (email, mobile) )
    rows = dict_cur.fetchall()
    if rows:
        success=True
        dict_cur.execute('delete from combined_messages where email = %s and mobile = %s', (email, mobile) )

    #Close the database connection
    dict_cur.close()

    #Return result
    return success
                
#Do lookup from schedules table and returns an array of up to 3 messages
def get_initial_message(municipality, zone_dict):
    from app.models import Schedule

    #Make query for next next recycling, trash and yard pick up for this zone and day. If yard doesn't exist, there's no independent schedule for it so use trash
    recycle = Schedule.objects.get(date=datetime.date.today(), municipality=municipality, service="RECYCLE", zone=zone_dict["recycle_zone"], day=zone_dict["recycle_day"])
    trash = Schedule.objects.get(date=datetime.date.today(), municipality=municipality, service="TRASH", zone=zone_dict["trash_zone"], day=zone_dict["trash_day"])
    try:
        yard = Schedule.objects.get(date=datetime.date.today(), municipality=municipality, service="YARD", zone=zone_dict["yard_zone"], day=zone_dict["yard_day"])
    except Schedule.DoesNotExist:
        yard = trash

    #Make sorted array of days to pick up
    r=int(recycle.days_to_pickup)
    t=int(trash.days_to_pickup)
    y=int(yard.days_to_pickup)
    sorted=[r, t, y]
    sorted.sort()

    #Make array to hold messages
    messages=[]

    #Loop over days_to_pickup
    previous=-1
    for day in sorted:
        #Ignore repeated days
        if day==previous:
            continue

        #Reset previous
        previous=day

        #Make array for services
        services=[]
        
        #See what services are on this day
        if t == day:
            services.append("trash")
            this_date = trash.next_date
        
        if r == day:
            services.append("recycling")
            this_date = recycle.next_date

        if y == day:
            services.append("leaf")
            this_date = yard.next_date

        #Make tag for message
        if day==0:
            tag = " day is today!"
        elif day==1:
            tag = " day is tomorrow!"
        else:
            #Make tag with formated date string
            tag = " day is " +  this_date.strftime("%A %e %B") + "."
        
        #Make the message
        l=len(services)

        if l==0:
            #Error, so return null
            return

        elif l==1:
            message="Your next " + services[0] + tag
        elif l==2:
            message="Your next " + services[0] + " and " + services[1] + tag
        elif l==3:
            message="Your next " + services[0] + ",  " + services[1] + " and " + services[2] + tag

        #Append message to array
        messages.append(message)

    #If there are fewer than 3 nessages, add blanks
    if len(messages)<3:
        messages.append("")
    if len(messages)<3:
        messages.append("")

    #Return the result
    return messages

#Copy result into contacts table
def insert_contact(municipality, parsed_address, zip, zone_dict):
    from app.models import Contacts

    #Create a Contacts object and save
    z=Contacts()
    z.address=parsed_address
    z.zip=zip
    z.recycle_zone=zone_dict["recycle_zone"]
    z.recycle_day=zone_dict["recycle_day"]
    z.trash_zone=zone_dict["trash_zone"]
    z.trash_day=zone_dict["trash_day"]
    z.yard_zone=zone_dict["trash_zone"]
    z.yard_day=zone_dict["trash_day"]
    z.municipality=municipality
    z.save()
            
    #Return the primary key to access this record later in session.  stackoverflow.com/questions/732952/get-primary-key-after-saving-a-modelform-in-django
    primary_key = z.pk
    return primary_key

    #return day, zone

#Copy message into initial_message table
def insert_initial_message(primary_key, messages):
    from app.models import Initial_Message

    #Create an Initial_Message object
    z=Initial_Message()
    z.pk=primary_key

    if messages[0]:
        z.message_0 = messages[0]

    if messages[1]:
        z.message_1 = messages[1]

    if messages[2]:
        z.message_2 = messages[2]
    
    z.save()
            
    return

#Get message from initial_message table
def select_initial_message(primary_key):
    from app.models import Initial_Message

    #Get Initial_Message object with pk
    z=Initial_Message.objects.get(pk=primary_key)

    #Extract the messages
    messages=[]

    if z.message_0:
        messages.append(z.message_0)
    else:
        messages.append("")

    if z.message_1:
        messages.append(z.message_1)
    else:
        messages.append("")

    if z.message_2:
        messages.append(z.message_2)
    else:
        messages.append("")

    return messages

#################################################################################################################################################################################
#All municipalities - Zone look up
#################################################################################################################################################################################
#Look up zone and day information from municipality
def get_zones(municipality, address, zip):
    #Lower Merion look up
    if municipality=="LOWER_MERION":
        #Get recycling zone
        result = municipalities.lower_merion.get_recycling_zone(address, zip)

        #Assign zone and day values if it worked.
        if result:
            recycle_day_number, recycle_zone = result
            trash_day_number =  recycle_day_number
            yard_day_number =  recycle_day_number
            trash_zone = recycle_zone[1]
            yard_zone = trash_zone
        else:
            return

    #Philadelphia look up    
    elif municipality=="PHILADELPHIA":
        #Get recycling zone
        result = municipalities.philadelphia.get_trash_zone(address, zip)

        #Test if it worked
        if result:
            trash_day_number, trash_zone = result
        else:
            return

        #In Philadelphia trash day is recycling day and yard day
        if trash_day_number and trash_zone:
            recycle_zone=trash_zone
            recycle_day_number=trash_day_number
            yard_zone=trash_zone
            yard_day_number=trash_day_number

    #New York City look up    
    elif municipality=="NEW_YORK":
        #Get recycling zone
        c = Cities()
        browser = c.get_browser()
        nyc = NYC(browser)
        result = nyc.get_zone(address, zip)
        c.close_browser()

        #Test if it worked
        if result and len(result) == 3:
            success, (trash_zone, recycle_zone), elapsed_time = result
        else:
            return

        #In NY zones and days are the same
        if trash_zone and recycle_zone:
            week_day = datetime.datetime.today().weekday() + 1
            yard_zone=trash_zone
            trash_day_number = week_day
            yard_day_number = week_day
            recycle_day_number = week_day

    #Washington, DC look up    
    elif municipality=="DC":
        #Get recycling zone
        c = Cities()
        browser = c.get_browser()
        dc = DC(browser)
        result = dc.get_zone(address, zip)
        c.close_browser()

        #Test if it worked
        if result and len(result) == 3:
            success, (trash_zone, recycle_zone), elapsed_time = result
        else:
            return

        #In NY zones and days are the same
        if trash_zone and recycle_zone:
            week_day = datetime.datetime.today().weekday() + 1
            yard_zone=trash_zone
            trash_day_number = week_day
            yard_day_number = week_day
            recycle_day_number = week_day

    #Other municipalities go here
    else:
        return
        
    #Return dictionary of results if defined, else null
    if 1==1 or recycle_zone and trash_zone and recycle_day_number and trash_day_number:
        zone_dict={
            'recycle_zone': recycle_zone,
            'recycle_day': recycle_day_number,
            'trash_zone': trash_zone,
            'trash_day': trash_day_number,
            'yard_zone': yard_zone,
            'yard_day': yard_day_number,
        }
        return zone_dict
    else:
        return

