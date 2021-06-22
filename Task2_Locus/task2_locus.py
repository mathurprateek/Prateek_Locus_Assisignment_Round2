"""
Objective: this script automatically check the predicted barometric pressure everyday
           and send an email if the pressure is predicted to fall below 995 Millibar during 6am to 6pm.
API used: This script will call 'One Call API' from https://openweathermap.org/api to populate data.
Service used: Hourly forecast for 48 hours.
Input: User need to give input for latitude and longitude values at the time of running the script.
Time: Job will run at target timezone's 03:00 AM.
NOTE: PLEASE ENTER SENDER AND RECEIVER EMAIL-IDS AND PASSWORD AT LINE 63 FOR THE SCRIPT TO RUN SUCCESSFULLY.
"""

import requests
import pytz
import smtplib
import ssl
import schedule
from timezonefinder import TimezoneFinder
from datetime import datetime as dt, timedelta, timezone


lat = float(input("please enter value for Latitude: "))  # latitude
lon = float(input("please enter value for Longitude: "))  # longitude
tzf_str = TimezoneFinder().timezone_at(lng=lon, lat=lat)
tz = pytz.timezone(tzf_str)  # timezone
curr_dt = dt.now(tz)  # current date in the timezone
start_local_dt = dt(curr_dt.year, curr_dt.month, curr_dt.day, 6, tzinfo=tz)
end_local_dt = dt(curr_dt.year, curr_dt.month, curr_dt.day, 18, tzinfo=tz)

# calculating UTC offset value
utc_dst_offset = curr_dt.utcoffset().total_seconds() - start_local_dt.utcoffset().total_seconds()

# start time 6 AM in timezone
unx_start_target_dt = (start_local_dt - timedelta(seconds=utc_dst_offset)).timestamp()

# end time 6 PM in timezone
unx_end_target_dt = (end_local_dt - timedelta(seconds=utc_dst_offset)).timestamp()

# schedule time calculated to run script
# in local timezone from target timezone
# for e.g. target timezone (Dubai @ 03:00 AM) = Indian timezone (04:30 AM)
dt1 = dt(curr_dt.year, curr_dt.month, curr_dt.day, 3, tzinfo=tz)
dt1_dst = dt1 - timedelta(seconds=utc_dst_offset)
dt1_dst_utc = dt1_dst.astimezone(pytz.utc)
dt1_dst_utc_to_local_tz = dt1_dst_utc.astimezone(dt.now(timezone.utc).astimezone().tzinfo)

# passing latitude and longitude value to the URL
# Retrieving hourly forecast data
res = requests.get(f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}'
                   f'&exclude=current,minutely,alerts,daily&appid=78385f931961ae9b80060c70d2c7bf6f')

# Dictionary for saving unix timestamps (key) and respective pressure (value)
op = {}

# reading all hourly json response to check if pressure fall below 995 Millibar between 6am-6pm
for e in res.json()["hourly"]:
    if unx_start_target_dt <= float(e["dt"]) <= unx_end_target_dt:
        # if pressure fall below 995 Millibar, store value for unix time and pressure value in dictionary
        if e["pressure"] < 995:
            op[e["dt"]] = e["pressure"]

smtp_server, port = "smtp.gmail.com", 587

# please enter correct email-ids and password for script to run
sender_email, receiver_email = 'sender@gmail.com', 'receiver@gmail.com'
password_sender_email = "passwordOfSenderEmailId"

message = """\
From: {}
To: {}
Subject: Alert! pressure might fall below 995 Millibar

Unix Timestamp and Pressure Value
Displayed in Dictionary below
{} 

""".format(sender_email, receiver_email, op)

context = ssl.create_default_context()


def auto_press_chk_and_mail():
    if len(op) > 0:
        with smtplib.SMTP(smtp_server, port) as server:
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            server.login(sender_email, password_sender_email)
            server.sendmail(sender_email, receiver_email, message)


# job will run everyday as per target timezone's 03:00 AM to local timezone on which script is deployed
# make sure local timezone is ahead of target timezone
hh = dt1_dst_utc_to_local_tz.hour
mm = dt1_dst_utc_to_local_tz.minute

if hh < 10 and mm < 10:
    hh = "0" + str(hh)
    mm = "0" + str(mm)
elif hh < 10:
    hh = "0" + str(hh)
elif mm < 10:
    mm = "0" + str(mm)
else:
    pass

tm = str(hh) + ":" + str(mm)
schedule.every().day.at(tm).do(auto_press_chk_and_mail)


while True:
    schedule.run_pending()
