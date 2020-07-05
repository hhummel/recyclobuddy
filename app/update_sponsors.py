from sys import argv
from recycle import get_database_connections

if len(argv) != 4:
    print("Must take 3 arguments: path to referrals.txt, date and message")
    sys.exit()

file = argv[1]
date = argv[2]
message = argv[3]

cur, dict_cur, db = get_database_connections()

print ("referral file path; %s date: %s message: %s" % (file, date, message))

f = open(file, "r")
for line in f:
    (first, last) = line.strip().title().split(" ")
    query = "select email, mobile from subscribers where first_name='%s' and last_name='%s'" % (first, last)
    dict_cur.execute(query)
    rows = dict_cur.fetchall()
    if rows:
        print("Match succeeded for %s %s\n"% (first, last)) 
        for row in rows:
            update = "update sponsors set sponsor_message='%s' where email='%s' and mobile='%s' and date='%s'" % (message, row['email'], row['mobile'], date)
            dict_cur.execute(update)
            db.commit()
    else:
        print("No match for %s %s\n\n"% (first, last)) 
f.close()
