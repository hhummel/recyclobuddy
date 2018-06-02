from datetime import datetime, timedelta, date, time
from recycle import get_database_dictionary, get_database_connections

encoding = {0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9',
    10: 'a', 11: 'b', 12: 'c', 13: 'd', 14: 'e', 15: 'f', 16: 'g', 17: 'h', 18: 'i', 19: 'j',
    20: 'k', 21: 'l', 22: 'm', 23: 'm', 24: 'o', 25: 'p', 26: 'q', 27: 'r', 28: 's', 29: 't',
    30: 'u', 31: 'v', 32: 'w', 33: 'x', 34: 'y', 35: 'z', 36: 'A', 37: 'B', 38: 'C', 39: 'D',
    40: 'E', 41: 'F', 42: 'G', 43: 'H', 44: 'I', 45: 'J', 46: 'K', 47: 'L', 48: 'M', 49: 'N',
    50: 'O', 51: 'P', 52: 'Q', 53: 'R', 54: 'S', 55: 'T', 56: 'U', 57: 'V', 58: 'W', 59: 'X',
    60: 'Y', 61: 'Z'
}

def send_message(message, start_time, increment=30, query="select * from subscribers where subscribe=1"):
    '''Insert 'message' into combined_messages starting with 'start_time' string 'hh:mm' and incrementing each message by 'increment' seconds'''
    dict_cur = get_database_dictionary()
    dict_cur.execute(query)
    start = [int(i) for i in start_time.split(":")]
    base_query = "insert into combined_messages (email, mobile, carrier, alert_time, email_alert, sms_alert, message) values('{}', {}, '{}', '{}', {}, {}, '{}')"
    rows = dict_cur.fetchall()

    #Make a datetime so utilities work
    right_now = datetime.now()
    time = right_now.replace(hour=start[0], minute=start[1])
    for row in rows:
        query = base_query.format(row['email'], row['mobile'], row['carrier'], time.strftime("%X"), row['email_alert'], row['sms_alert'], message)
        dict_cur.execute(query)
        time = time + timedelta(seconds=increment)
    dict_cur.close()

def sponsor_message(sponsor, message, date, query="select * from subscribers where subscribe=1", link="w8d.io/"):
    '''Insert 'message' into sponsors table for date 'date' using url coding'''
    cur, dict_cur, con = get_database_connections()
    dict_cur.execute(query)
    base_query = "insert into sponsors (email, mobile, date, sponsor_message) values('{}', {}, '{}', '{}')"
    rows = dict_cur.fetchall()

    for row in rows:
        sponsored = message
        if link:
            #Ignore collisions ???
            code = get_code(sponsor, row['email'], row['mobile'])
            sponsored = "{} {}/{}".format(sponsored, link, code)
        query =  base_query.format(row['email'], row['mobile'], date, sponsored)
        dict_cur.execute(query)
    con.commit()
    dict_cur.close()
    con.close()
        
def get_code(sponsor, email, mobile, nudge=""):
    number_codes = []
    for k in [1, 2, 3, 5]:
        number_codes.append(sum([(i % 10 + 1)** k * ord(j) for i, j in enumerate(list(sponsor + email + str(mobile) + str(nudge)))]) % len(encoding))
    return "".join([encoding[i] for i in number_codes])

 #Set up import of information from mysite package in parallel directory
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
    from mysite.passwords import MYSQL_NAME, MYSQL_USER, MYSQL_PASSWORD

    db=MySQLdb.connect(host="localhost", db=MYSQL_NAME, user=MYSQL_USER , passwd=MYSQL_PASSWORD)
    cur=db.cursor()
