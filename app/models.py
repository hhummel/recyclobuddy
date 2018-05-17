from django.db import models

# Create your models here.
from django.db import models
from django.forms import ModelForm

#Choices
PREFIX_CHOICES = (
    ('Mr.', 'Mr.'),
    ('Mrs.', 'Mrs'),
    ('Ms.', 'Ms'),
    ('Dr.', 'Dr'),
    ('Prof.', 'Prof'),
)

SUFFIX_CHOICES = (
    ('', 'None'),
    (', PhD', 'PhD'),
    (', MD', 'MD'),
    (', DO', 'DO'),
    (', DDM', 'DDM'),
    (', Esq.', 'Esq'),
    (', Jr.', 'Jr'),
    (', Sr.', 'Sr'),
    (', II', 'II'),
    (', III', 'III'),
    (', IV', 'IV'),
    (', V', 'V'),
)

STATE_CHOICES = (
    ('PA', 'Pennsylvania'),
    ('AL', 'Alabama'),
    ('AK', 'Alaska'),
    ('AR', 'Arkansas'),
    ('CA', 'California'),
    ('CO', 'Colorado'),
    ('CT', 'Connecticut'),
    ('DC', 'District of Columbia'),
    ('DE', 'Delaware'),
    ('FL', 'Florida'),
    ('GA', 'Georgia'),
    ('HI', 'Hawaii'),
    ('ID', 'Idaho'),
    ('IL', 'Illinois'),
    ('IN', 'Indiana'),
    ('IA', 'Iowa'),
    ('KS', 'Kansas'),
    ('KY', 'Kentucky'),
    ('LA', 'Louisiana'),
    ('ME', 'Maine'),
    ('MD', 'Maryland'),
    ('MA', 'Massachusetts'),
    ('MI', 'Michigan'),
    ('MN', 'Minnesota'),
    ('MS', 'Mississippi'),
    ('MO', 'Missouri'),
    ('MT', 'Montana'),
    ('NE', 'Nebraska'),
    ('NV', 'Nevada'),
    ('NH', 'New Hampshire'),
    ('NJ', 'New Jersey'),
    ('NM', 'New Mexico'),
    ('NY', 'New York'),
    ('NC', 'North Carolina'),
    ('ND', 'North Dakota'),
    ('OH', 'Ohio'),
    ('OK', 'Oklahoma'),
    ('OR', 'Oregon'),
    ('RI', 'Rhode Island'),
    ('SC', 'South Dakota'),
    ('TN', 'Tennessee'),
    ('TX', 'Texas'),
    ('UT', 'Utah'),
    ('VT', 'Vermont'),
    ('VA', 'Virginia'),
    ('WA', 'Washington'),
    ('WV', 'West Virginia'),
    ('WI', 'Wisconsin'),
    ('WY', 'Wyoming'),
)

DAY_CHOICES = (
    ('Mon', 'Monday'),
    ('Tue', 'Tuesday'),
    ('Wed', 'Wednesday'),
    ('Thu', 'Thursday'),
    ('Fri', 'Friday'),
    ('Sat', 'Saturday'),
    ('Sun', 'Sunday'),
)

CARRIER_CHOICES = (
    ('VER', 'Verizon Wireless'),
    ('ATT', 'AT&T Mobility'),
    ('SPR', 'Sprint Corporation'),
    ('TMO', 'T-Mobile US'),
    ('USC', 'US Cellular'),
    ('VRG', 'Virgin Mobile'),
    ('GOO', 'Google Voice'),
    ('CRK', 'Cricket Wireless'),
)

ALERT_CHOICES = (
    ('0', 'Day of Pickup'),
    ('1', 'Day Before Pickup'),
)

TERMS_CHOICES = (
    ('0', 'Disagree'),
    ('1', 'Agree'),
)

ALERT_TIMES = (
    ('5:00:00', '5:00 AM'),
    ('5:10:00', '5:10 AM'),
    ('5:20:00', '5:20 AM'),
    ('5:30:00', '5:30 AM'),
    ('5:40:00', '5:40 AM'),
    ('5:50:00', '5:50 AM'),
    ('6:00:00', '6:00 AM'),
    ('6:10:00', '6:10 AM'),
    ('6:20:00', '6:20 AM'),
    ('6:30:00', '6:30 AM'),
    ('6:40:00', '6:40 AM'),
    ('6:50:00', '6:50 AM'),
    ('7:00:00', '7:00 AM'),
    ('7:10:00', '7:10 AM'),
    ('7:20:00', '7:20 AM'),
    ('7:30:00', '7:30 AM'),
    ('7:40:00', '7:40 AM'),
    ('7:50:00', '7:50 AM'),
    ('8:00:00', '8:00 AM'),
    ('8:10:00', '8:10 AM'),
    ('8:20:00', '8:20 AM'),
    ('8:30:00', '8:30 AM'),
    ('8:40:00', '8:40 AM'),
    ('8:50:00', '8:50 AM'),
    ('9:00:00', '9:00 AM'),
    ('15:00:00', '3:00 PM'),
    ('15:10:00', '3:10 PM'),
    ('15:20:00', '3:20 PM'),
    ('15:30:00', '3:30 PM'),
    ('15:40:00', '3:40 PM'),
    ('15:50:00', '3:50 PM'),
    ('16:00:00', '4:00 PM'),
    ('16:10:00', '4:10 PM'),
    ('16:20:00', '4:20 PM'),
    ('16:30:00', '4:30 PM'),
    ('16:40:00', '4:40 PM'),
    ('16:50:00', '4:50 PM'),
    ('17:00:00', '5:00 PM'),
    ('17:10:00', '5:10 PM'),
    ('17:20:00', '5:20 PM'),
    ('17:30:00', '5:30 PM'),
    ('17:40:00', '5:40 PM'),
    ('17:50:00', '5:50 PM'),
    ('18:00:00', '6:00 PM'),
    ('18:10:00', '6:10 PM'),
    ('18:20:00', '6:20 PM'),
    ('18:30:00', '6:30 PM'),
    ('18:40:00', '6:40 PM'),
    ('18:50:00', '6:50 PM'),
    ('19:00:00', '7:00 PM'),
    ('19:10:00', '7:10 PM'),
    ('19:20:00', '7:20 PM'),
    ('19:30:00', '7:30 PM'),
    ('19:40:00', '7:40 PM'),
    ('19:50:00', '7:50 PM'),
    ('20:00:00', '8:00 PM'),
    ('20:10:00', '8:10 PM'),
    ('20:20:00', '8:20 PM'),
    ('20:30:00', '8:30 PM'),
    ('20:40:00', '8:40 PM'),
    ('20:50:00', '8:50 PM'),
    ('21:00:00', '9:00 PM'),
    ('21:10:00', '9:10 PM'),
    ('21:20:00', '9:20 PM'),
    ('21:30:00', '9:30 PM'),
    ('21:40:00', '9:40 PM'),
    ('21:50:00', '9:50 PM'),
    ('22:00:00', '10:00 PM'),
    ('22:10:00', '10:10 PM'),
    ('22:20:00', '10:20 PM'),
    ('22:30:00', '10:30 PM'),
    ('22:40:00', '10:40 PM'),
    ('22:50:00', '10:50 PM'),
    ('23:00:00', '11:00 PM'),
)

SERVICE_CHOICES = (
    ('TRASH', 'Trash'),
    ('RECYCLE', 'Recycling'),
    ('YARD', 'Yard Waste'),
    ('XMAS', 'Christmas Trees'),
    ('HAZ', 'Hazardous Waste'),
)

MUNICIPAL_CHOICES = (
    ('PHILADELPHIA', 'Philadelphia, PA'),
    ('LOWER_MERION', 'Lower Merion Township, PA'),
    ('NARBERTH', 'Narberth, PA'),
    ('RADNOR', ', Radnor Township, PA'),
    ('HAVERFORD', ', Haverford Township, PA'),
    ('WILLISTOWN', 'Willistown Township, PA'),
    ('EASTTOWN', ', Easttown Township, PA'),
    ('MALVERN', ', Malvern, PA'),
    ('PITTSBURGH', ', Pittsburgh, PA'),
    ('TREDYFFRIN', 'Tredyffrin Township, PA'),
    ('NEW_YORK', 'New York, NY'),
    ('LOS_ANGELES', 'Los Angeles, CA'),
    ('CHICAGO', 'Chicago, IL'),
    ('HOUSTON', 'Houston, TX'),
    ('PHOENIX', 'Phoenix, AZ'),
    ('SAN_ANTONIO', 'San Antonio, TX'),
    ('SAN_DIEGO', 'San Diego, CA'),
    ('DALLAS', 'Dallas, TX'),
    ('SAN_JOSE', 'San Jose, CA'),
    ('AUSTIN', 'Austin, TX'),
    ('INDIANAPOLIS', 'Indianapolis, IN'),
    ('JACKSONVILLE', 'Jacksonville, FL'),
    ('SAN_FRANCISCO', 'San Francisco, CA'),
    ('COLUMBUS', 'Columbus, OH'),
    ('CHARLOTTE', 'Charlotte, NC'),
    ('FORT_WORTH', 'Fort Worth, TX'),
    ('DETROIT', 'Detroit, MI'),
    ('EL_PASO', 'El Paso, TX'),
    ('MEMPHIS', 'Memphis, TN'),
    ('SEATTLE', 'Seattle, WA'),
    ('DENVER', 'Denver, CO'),
    ('DC', 'Washington, DC'),
    ('BOSTON', 'Boston, MA'),
    ('NASHVILLE', 'Nashville, TN'),
    ('BALTIMORE', 'Baltimore, MD'),
    ('NEWTON', 'Newton, MA'),
    ('BROOKLINE', 'Brooline, MA'),
    ('CAMBRIDGE', 'Cambridge, MA'),
    ('NAPERVILLE', 'Naperville, IL'),
    ('WHITE_PLAINS', 'White Plains, NY'),
    ('NEW_HAVEN', 'New Haven, CT'),
    ('STAMFORD', 'Stamform, CT'),
    ('PRINCETON', 'Princeton, NJ'),
)

CURRENT_CHOICES = (
    ('LOWER_MERION', 'Lower Merion Township, PA'),
    ('PHILADELPHIA', 'Philadelphia, PA'),
)

HOLIDAY_CHOICES = (
    ('NEW_YEARS', 'New Years Day'),
    ('MLK', 'Martin Luther King'),
    ('PULASKI', 'Pulaski Day'),
    ('WASHINGTON', 'Washington Birthday'),
    ('GOOD_FRI', 'Good Friday'),
    ('MEMORIAL', 'Memorial Day'),
    ('FOURTH', 'Independence Day'),
    ('LABOR', 'Labor Day'),
    ('COLUMBUS', 'Columbus Day'),
    ('VETERANS', 'Veterans Day'),
    ('THANKS', 'Thanksgiving'),
    ('XMAS', 'Christmas'),
)

# Create your models here.

#Contact information.  Note create is the creation time of the contact object in UTC
class Contacts(models.Model):
    index_key = models.AutoField(primary_key=True)
    creation = models.DateTimeField(auto_now_add=True, blank=True)
    prefix = models.CharField(max_length=5, choices=PREFIX_CHOICES)
    first_name = models.CharField(max_length=35)
    middle_name = models.CharField(max_length=35, null=True)
    last_name = models.CharField(max_length=35)
    suffix = models.CharField(max_length=5, choices=SUFFIX_CHOICES)
    address = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2, choices=STATE_CHOICES)
    zip = models.CharField(max_length=5, default='00000')
    municipality = models.CharField(max_length=25, choices=MUNICIPAL_CHOICES)
    email = models.EmailField(max_length=100)
    mobile = models.CharField(max_length=10, null=True)
    carrier = models.CharField(max_length=3, choices=CARRIER_CHOICES)
    recycle_zone = models.CharField(max_length=10)
    trash_zone = models.CharField(max_length=10)
    yard_zone = models.CharField(max_length=10)
    recycle_day = models.IntegerField(max_length=1)
    trash_day = models.IntegerField(max_length=1)
    yard_day = models.IntegerField(max_length=1)
    alert_time = models.TimeField(null=True)
    alert_day = models.IntegerField(max_length=1, null=True)
    email_alert = models.BooleanField(default=True)
    sms_alert = models.BooleanField(default=True)
    request = models.BooleanField(default=False)
    subscribe = models.BooleanField(default=False)
    terms = models.BooleanField(default=False)

#Schedule information.
class Schedule(models.Model):
    index_key = models.AutoField(primary_key=True)
    municipality = models.CharField(max_length=25, choices=MUNICIPAL_CHOICES)
    service = models.CharField(max_length=10, choices=SERVICE_CHOICES)
    date = models.DateField(null=False)
    emergency_date = models.DateField(null=True)
    zone = models.CharField(max_length=10, null=True)
    zone2 = models.CharField(max_length=10, null=True)
    day = models.IntegerField(max_length=1, null=True)
    day2 = models.IntegerField(max_length=1, null=True)
    holiday = models.IntegerField(null=False)
    next_date = models.DateField(null=False)
    days_to_pickup = models.IntegerField(null=False)
    emergency = models.BooleanField(default=False)

#Holidays observed by municipality
class Holiday_list(models.Model):
    index_key = models.AutoField(primary_key=True)
    municipality = models.CharField(max_length=25, choices=MUNICIPAL_CHOICES)
    name = models.CharField(max_length=20, choices=HOLIDAY_CHOICES)

#Holiday observed dates
class Holidays(models.Model):
    index_key = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20, choices=HOLIDAY_CHOICES)
    date = models.DateField(null=False)

#Initial message
class Initial_Message(models.Model):
    index_key = models.AutoField(primary_key=True)
    message_0 = models.CharField(max_length=100)
    message_1 = models.CharField(max_length=100)
    message_2 = models.CharField(max_length=100)
