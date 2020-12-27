# Generated by Django 2.1.2 on 2019-01-04 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contacts',
            fields=[
                ('index_key', models.AutoField(primary_key=True, serialize=False)),
                ('creation', models.DateTimeField(auto_now_add=True)),
                ('prefix', models.CharField(choices=[('Mr.', 'Mr.'), ('Mrs.', 'Mrs'), ('Ms.', 'Ms'), ('Dr.', 'Dr'), ('Prof.', 'Prof')], max_length=5)),
                ('first_name', models.CharField(max_length=35)),
                ('middle_name', models.CharField(max_length=35, null=True)),
                ('last_name', models.CharField(max_length=35)),
                ('suffix', models.CharField(choices=[('', 'None'), (', PhD', 'PhD'), (', MD', 'MD'), (', DO', 'DO'), (', DDM', 'DDM'), (', Esq.', 'Esq'), (', Jr.', 'Jr'), (', Sr.', 'Sr'), (', II', 'II'), (', III', 'III'), (', IV', 'IV'), (', V', 'V')], max_length=5)),
                ('address', models.CharField(max_length=100)),
                ('address2', models.CharField(max_length=100, null=True)),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(choices=[('PA', 'Pennsylvania'), ('AL', 'Alabama'), ('AK', 'Alaska'), ('AR', 'Arkansas'), ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DC', 'District of Columbia'), ('DE', 'Delaware'), ('FL', 'Florida'), ('GA', 'Georgia'), ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('RI', 'Rhode Island'), ('SC', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming')], max_length=2)),
                ('zip', models.CharField(default='00000', max_length=5)),
                ('municipality', models.CharField(choices=[('PHILADELPHIA', 'Philadelphia, PA'), ('LOWER_MERION', 'Lower Merion Township, PA'), ('NARBERTH', 'Narberth, PA'), ('RADNOR', ', Radnor Township, PA'), ('HAVERFORD', ', Haverford Township, PA'), ('WILLISTOWN', 'Willistown Township, PA'), ('EASTTOWN', ', Easttown Township, PA'), ('MALVERN', ', Malvern, PA'), ('PITTSBURGH', ', Pittsburgh, PA'), ('TREDYFFRIN', 'Tredyffrin Township, PA'), ('NEW_YORK', 'New York, NY'), ('LOS_ANGELES', 'Los Angeles, CA'), ('CHICAGO', 'Chicago, IL'), ('HOUSTON', 'Houston, TX'), ('PHOENIX', 'Phoenix, AZ'), ('SAN_ANTONIO', 'San Antonio, TX'), ('SAN_DIEGO', 'San Diego, CA'), ('DALLAS', 'Dallas, TX'), ('SAN_JOSE', 'San Jose, CA'), ('AUSTIN', 'Austin, TX'), ('INDIANAPOLIS', 'Indianapolis, IN'), ('JACKSONVILLE', 'Jacksonville, FL'), ('SAN_FRANCISCO', 'San Francisco, CA'), ('COLUMBUS', 'Columbus, OH'), ('CHARLOTTE', 'Charlotte, NC'), ('FORT_WORTH', 'Fort Worth, TX'), ('DETROIT', 'Detroit, MI'), ('EL_PASO', 'El Paso, TX'), ('MEMPHIS', 'Memphis, TN'), ('SEATTLE', 'Seattle, WA'), ('DENVER', 'Denver, CO'), ('DC', 'Washington, DC'), ('BOSTON', 'Boston, MA'), ('NASHVILLE', 'Nashville, TN'), ('BALTIMORE', 'Baltimore, MD'), ('NEWTON', 'Newton, MA'), ('BROOKLINE', 'Brooline, MA'), ('CAMBRIDGE', 'Cambridge, MA'), ('NAPERVILLE', 'Naperville, IL'), ('WHITE_PLAINS', 'White Plains, NY'), ('NEW_HAVEN', 'New Haven, CT'), ('STAMFORD', 'Stamform, CT'), ('PRINCETON', 'Princeton, NJ')], max_length=25)),
                ('email', models.EmailField(max_length=100)),
                ('mobile', models.CharField(max_length=10, null=True)),
                ('carrier', models.CharField(choices=[('VER', 'Verizon Wireless'), ('ATT', 'AT&T Mobility'), ('SPR', 'Sprint Corporation'), ('TMO', 'T-Mobile US'), ('USC', 'US Cellular'), ('VRG', 'Virgin Mobile'), ('GOO', 'Google Voice'), ('CRK', 'Cricket Wireless')], max_length=3)),
                ('recycle_zone', models.CharField(max_length=10)),
                ('trash_zone', models.CharField(max_length=10)),
                ('yard_zone', models.CharField(max_length=10)),
                ('recycle_day', models.IntegerField(max_length=1)),
                ('trash_day', models.IntegerField(max_length=1)),
                ('yard_day', models.IntegerField(max_length=1)),
                ('alert_time', models.TimeField(null=True)),
                ('alert_day', models.IntegerField(max_length=1, null=True)),
                ('email_alert', models.BooleanField(default=True)),
                ('sms_alert', models.BooleanField(default=True)),
                ('request', models.BooleanField(default=False)),
                ('subscribe', models.BooleanField(default=False)),
                ('terms', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Holiday_list',
            fields=[
                ('index_key', models.AutoField(primary_key=True, serialize=False)),
                ('municipality', models.CharField(choices=[('PHILADELPHIA', 'Philadelphia, PA'), ('LOWER_MERION', 'Lower Merion Township, PA'), ('NARBERTH', 'Narberth, PA'), ('RADNOR', ', Radnor Township, PA'), ('HAVERFORD', ', Haverford Township, PA'), ('WILLISTOWN', 'Willistown Township, PA'), ('EASTTOWN', ', Easttown Township, PA'), ('MALVERN', ', Malvern, PA'), ('PITTSBURGH', ', Pittsburgh, PA'), ('TREDYFFRIN', 'Tredyffrin Township, PA'), ('NEW_YORK', 'New York, NY'), ('LOS_ANGELES', 'Los Angeles, CA'), ('CHICAGO', 'Chicago, IL'), ('HOUSTON', 'Houston, TX'), ('PHOENIX', 'Phoenix, AZ'), ('SAN_ANTONIO', 'San Antonio, TX'), ('SAN_DIEGO', 'San Diego, CA'), ('DALLAS', 'Dallas, TX'), ('SAN_JOSE', 'San Jose, CA'), ('AUSTIN', 'Austin, TX'), ('INDIANAPOLIS', 'Indianapolis, IN'), ('JACKSONVILLE', 'Jacksonville, FL'), ('SAN_FRANCISCO', 'San Francisco, CA'), ('COLUMBUS', 'Columbus, OH'), ('CHARLOTTE', 'Charlotte, NC'), ('FORT_WORTH', 'Fort Worth, TX'), ('DETROIT', 'Detroit, MI'), ('EL_PASO', 'El Paso, TX'), ('MEMPHIS', 'Memphis, TN'), ('SEATTLE', 'Seattle, WA'), ('DENVER', 'Denver, CO'), ('DC', 'Washington, DC'), ('BOSTON', 'Boston, MA'), ('NASHVILLE', 'Nashville, TN'), ('BALTIMORE', 'Baltimore, MD'), ('NEWTON', 'Newton, MA'), ('BROOKLINE', 'Brooline, MA'), ('CAMBRIDGE', 'Cambridge, MA'), ('NAPERVILLE', 'Naperville, IL'), ('WHITE_PLAINS', 'White Plains, NY'), ('NEW_HAVEN', 'New Haven, CT'), ('STAMFORD', 'Stamform, CT'), ('PRINCETON', 'Princeton, NJ')], max_length=25)),
                ('name', models.CharField(choices=[('NEW_YEARS', 'New Years Day'), ('MLK', 'Martin Luther King'), ('PULASKI', 'Pulaski Day'), ('WASHINGTON', 'Washington Birthday'), ('GOOD_FRI', 'Good Friday'), ('MEMORIAL', 'Memorial Day'), ('FOURTH', 'Independence Day'), ('LABOR', 'Labor Day'), ('COLUMBUS', 'Columbus Day'), ('VETERANS', 'Veterans Day'), ('THANKS', 'Thanksgiving'), ('XMAS', 'Christmas')], max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Holidays',
            fields=[
                ('index_key', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(choices=[('NEW_YEARS', 'New Years Day'), ('MLK', 'Martin Luther King'), ('PULASKI', 'Pulaski Day'), ('WASHINGTON', 'Washington Birthday'), ('GOOD_FRI', 'Good Friday'), ('MEMORIAL', 'Memorial Day'), ('FOURTH', 'Independence Day'), ('LABOR', 'Labor Day'), ('COLUMBUS', 'Columbus Day'), ('VETERANS', 'Veterans Day'), ('THANKS', 'Thanksgiving'), ('XMAS', 'Christmas')], max_length=20)),
                ('date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Initial_Message',
            fields=[
                ('index_key', models.AutoField(primary_key=True, serialize=False)),
                ('message_0', models.CharField(max_length=100)),
                ('message_1', models.CharField(max_length=100)),
                ('message_2', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('index_key', models.AutoField(primary_key=True, serialize=False)),
                ('municipality', models.CharField(choices=[('PHILADELPHIA', 'Philadelphia, PA'), ('LOWER_MERION', 'Lower Merion Township, PA'), ('NARBERTH', 'Narberth, PA'), ('RADNOR', ', Radnor Township, PA'), ('HAVERFORD', ', Haverford Township, PA'), ('WILLISTOWN', 'Willistown Township, PA'), ('EASTTOWN', ', Easttown Township, PA'), ('MALVERN', ', Malvern, PA'), ('PITTSBURGH', ', Pittsburgh, PA'), ('TREDYFFRIN', 'Tredyffrin Township, PA'), ('NEW_YORK', 'New York, NY'), ('LOS_ANGELES', 'Los Angeles, CA'), ('CHICAGO', 'Chicago, IL'), ('HOUSTON', 'Houston, TX'), ('PHOENIX', 'Phoenix, AZ'), ('SAN_ANTONIO', 'San Antonio, TX'), ('SAN_DIEGO', 'San Diego, CA'), ('DALLAS', 'Dallas, TX'), ('SAN_JOSE', 'San Jose, CA'), ('AUSTIN', 'Austin, TX'), ('INDIANAPOLIS', 'Indianapolis, IN'), ('JACKSONVILLE', 'Jacksonville, FL'), ('SAN_FRANCISCO', 'San Francisco, CA'), ('COLUMBUS', 'Columbus, OH'), ('CHARLOTTE', 'Charlotte, NC'), ('FORT_WORTH', 'Fort Worth, TX'), ('DETROIT', 'Detroit, MI'), ('EL_PASO', 'El Paso, TX'), ('MEMPHIS', 'Memphis, TN'), ('SEATTLE', 'Seattle, WA'), ('DENVER', 'Denver, CO'), ('DC', 'Washington, DC'), ('BOSTON', 'Boston, MA'), ('NASHVILLE', 'Nashville, TN'), ('BALTIMORE', 'Baltimore, MD'), ('NEWTON', 'Newton, MA'), ('BROOKLINE', 'Brooline, MA'), ('CAMBRIDGE', 'Cambridge, MA'), ('NAPERVILLE', 'Naperville, IL'), ('WHITE_PLAINS', 'White Plains, NY'), ('NEW_HAVEN', 'New Haven, CT'), ('STAMFORD', 'Stamform, CT'), ('PRINCETON', 'Princeton, NJ')], max_length=25)),
                ('service', models.CharField(choices=[('TRASH', 'Trash'), ('RECYCLE', 'Recycling'), ('YARD', 'Yard Waste'), ('XMAS', 'Christmas Trees'), ('HAZ', 'Hazardous Waste')], max_length=10)),
                ('date', models.DateField()),
                ('emergency_date', models.DateField(null=True)),
                ('zone', models.CharField(max_length=10, null=True)),
                ('zone2', models.CharField(max_length=10, null=True)),
                ('day', models.IntegerField(max_length=1, null=True)),
                ('day2', models.IntegerField(max_length=1, null=True)),
                ('holiday', models.IntegerField()),
                ('next_date', models.DateField()),
                ('days_to_pickup', models.IntegerField()),
                ('emergency', models.BooleanField(default=False)),
            ],
        ),
    ]
