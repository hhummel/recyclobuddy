#!/usr/bin/python

import datetime, time
import MySQLdb
#from django.utils import timezone
#from django.core.mail import send_mail

import recycle

#Set parameters

#time_gap is how close time has to be in seconds before action occurs
time_gap=300

#Open output file
f=open("/usr/local/django/recyclocity/log/message.log", "a")
print >>f, "RecycloBuddy (re)starting now!"

#Create cycle_counter
cycle_counter=0

#Infinite loop
while True:
    #Get time
    current_time = datetime.datetime.now()
    print >>f, "Current time: " + str(current_time)

    #Refresh time is when to run updates.  Has today's date but preset time.
    lower_time=current_time.replace(hour=00, minute=00)
    upper_time=current_time.replace(hour=00, minute=time_gap/60+01)

    #Set up database connection
    cur=recycle.get_database_dictionary()

    #Check to see if time is in range for refresh
    if cycle_counter==0 or (lower_time < current_time and current_time<=upper_time):
	cycle_counter+=1

	#print str(lower_time) + " " + str(upper_time) + " " + str(current_time)
 
    	#Refresh subscriber database
    	recycle.refresh_subscriber(cur)

    	#Refresh messages database.
    	recycle.refresh_messages(cur)

	print  >>f, "Refresh at " + str(current_time)
	
    #Fire messages for this time slice
    recycle.fire_messages(cur, time_gap, f)

    #Close the database connection
    cur.close()

    #Flush buffer
    f.flush()

    #Sleep until next cycle
    time.sleep(time_gap)
