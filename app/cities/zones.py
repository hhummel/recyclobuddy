
#Get the day number from the day text
def get_day_number(day_text):
    day = day_text.strip().upper()
    if (day == "MON" or day == "MONDAY"):
        return 1
    if (day == "TUESDAY" or day == "TUE" or day == "TUES"):
        return 2
    if (day == "WEDNESDAY" or day == "WED"):
        return 3
    if (day == "THURSDAY" or day == "THU" or day == "THUR" or day == "THURS"):
        return 4
    if (day == "FRIDAY" or day == "FRI"):
        return 5
    if (day == "SATURDAY" or day == "SAT"):
        return 6
    if (day == "SUNDAY" or day == "SUN"):
        return 7
    return 0

