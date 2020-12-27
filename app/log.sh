#!/bin/bash
echo -e "IP address\tTime (UTC)\tURL\t\tSending URL"
echo -e "--------------\t--------------\t--------------\t--------------"
cat /var/log/nginx/access.log|grep /app/|grep -v static|grep -v "/app/ HTTP"|grep -v favicon|grep -v 70.91.3.134|grep -v bot.htm|cut -d" " -f1,4,7,11|sed 's/\[.*2019://g'|sed 's/https:\/\/recyclobuddy.com//g'|sed 's/ /\t/g'|sed 's/"//g'|sed 's/_[0-9]\{13\}//g'

