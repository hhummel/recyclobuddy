#!/usr/bin/python3

import datetime, time
import MySQLdb
import os

import recycle

#Set parameters
log_file = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'log/message.log'))

#time_gap is how close time has to be in seconds before action occurs
time_gap = 300
gap_seconds = int(time_gap % 60)
gap_minutes = int((time_gap - gap_seconds) / 60)

#Open output file
f = open(log_file, "a")
print ("RecycloBuddy (re)starting now!", file = f)

#Create cycle_counter
cycle_counter = 0

#Get start time
current_time = datetime.datetime.now()
lower_time = current_time
upper_time = current_time.replace(hour=00, minute=gap_minutes, second=gap_seconds)

#Infinite loop
while True:
    #Get time
    current_time = datetime.datetime.now()
    print("Current time: " + str(current_time), file=f)

    #Set up database connection
    cur=recycle.get_database_dictionary()

    #Check to see if time is in range for refresh
    if cycle_counter == 0 or (lower_time < current_time and current_time <= upper_time):
        cycle_counter += 1

        #Refresh subscriber database
        recycle.refresh_subscriber(cur)

        #Refresh messages database.
        recycle.refresh_messages(cur)

        print("Refresh at " + str(datetime.datetime.now()), file=f)
        
    #Refresh time is when to run updates.  Has today's date but preset time.
    lower_time = upper_time
    upper_time = upper_time + datetime.timedelta(seconds=time_gap)

    #Fire messages for this time slice
    recycle.fire_messages(cur, time_gap, f)

    #Close the database connection
    cur.close()

    #Flush buffer
    f.flush()

    #Find how long the cycle took
    delta = datetime.datetime.now() - current_time
    sleep_time = time_gap - delta.seconds - delta.microseconds/1000000
    if sleep_time < 0:
        raise Exception("Recyclobuddy failed:  Unable to send messages within time_gap")

    #Sleep until next cycle
    time.sleep(sleep_time)
