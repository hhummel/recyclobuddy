#!/usr/bin/python3

import datetime, time
import MySQLdb
import os, sys

sys.path.append(os.path.dirname(__file__))
import recycle

#Set parameters
log_file = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'log/message.log'))

#time_gap is how close time has to be in seconds before action occurs
time_gap = 300
gap_seconds = int(time_gap % 60)
gap_minutes = int((time_gap - gap_seconds) / 60)

#Open output file
f = open(log_file, "a")
print ("RecycloBuddy refresh now!", file = f)

#Set up database connection
cur = recycle.get_database_dictionary()

#Refresh subscriber database
recycle.refresh_subscriber(cur)

#Refresh messages database.
recycle.refresh_messages(cur)

#Close the database connection
cur.close()

#Infinite loop
while True:
    #Get time
    current_time = datetime.datetime.now()
    print("Current time: " + str(current_time), file=f)

    #Fire messages for this time slice
    recycle.fire_messages(cur, time_gap, f)

    #Find how long the cycle took
    delta = datetime.datetime.now() - current_time
    run_time = delta.seconds + delta.microseconds/1000000
    sleep_time = time_gap - run_time

    print("Run time: %s seconds, Sleep time: %s seconds" % (run_time, sleep_time), file=f)

    #Flush buffer
    f.flush()

    if sleep_time < 1:
        raise Exception("Recyclobuddy failed:  Unable to send messages within time_gap: %s seconds.  Run time: %s seconds. Sleep time: %seconds" % (time_gap, run_time, sleep_time))

    #Sleep until next cycle
    time.sleep(sleep_time)
