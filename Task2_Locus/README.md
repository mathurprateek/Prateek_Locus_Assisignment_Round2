
# Auto Weather Reporter Script
### Scheduled to run everyday

#### *Python Version*:
This API runs on Python version 3.6 or above.

#### *Objective*:
This script automatically checks the predicted barometric pressure everyday.

Send an e-mail to the stakeholders if the pressure is predicted to fall below 995 Millibar during 6am to 6pm.

This script will internally call 'One Call API' from https://openweathermap.org/api to populate data.

*Service: Hourly forecast for 48 hours*

#### *Input*:
User need to give input for *latitude* and *longitude* values at the time of running the script.

#### *Output*:
If value of pressure falls below 995 Millibar, e-mail sent to the stakeholder.

#### ***NOTE***: 
PLEASE ENTER SENDER AND RECEIVER EMAIL-IDS AND PASSWORD AT LINE 63 OF THE SCRIPT.

#### *Data Flow*:

1. Input Flow 
 - User Input **>>** Script **>>** openweathermap.org/api
2. Output Flow 
 - openweathermap.org/api **>>** Script **>>** e-mail to User

## Dependencies

#### Python packages/libraries for builing API

1. import **requests** 
*The requests library is the standard for making HTTP requests in Python.*

2. import **smtplib**
*Defines an SMTP client session object that can be used to send mail to any Internet machine with the SMTP listener daemon.*

3. import **ssl**
*Secure Sockets Layer and is designed to create secure connection between client and server.*

4. from **datetime** import **datetime** as dt, **timedelta**
*The datetime module supplies classes for manipulating dates and times.*

5. from **timezonefinder** import **TimezoneFinder**
*Fast python package for finding the timezone of any point on earth*

6. import **pytz**
*This library allows accurate and cross platform timezone calculations using Python 2.4 or higher.*

7. import **schedule**
*Run Python functions periodically using a friendly syntax.*


## Instructions to run the Script

#### Using [PyCharm](https://www.jetbrains.com/pycharm/download/#section=windows) tool to create, test and run the Script.

1. [Install Dependencies](https://www.jetbrains.com/help/pycharm/installing-uninstalling-and-upgrading-packages.html#interpreter-settings) in PyCharm,
as mentioned in the earlier section

2. [Configure Virtual Environment](https://www.jetbrains.com/help/pycharm/creating-virtual-environment.html) in PyCharm.

3. Place "task2_locus.py" file under root folder.

4. [Run](https://www.jetbrains.com/help/pycharm/creating-and-running-your-first-python-project.html#run) the script task2_locus.py

 4.1 Enter the Latitude and Longitude values, as promted my script.

5. Script will run at 03:00 AM of latitude and longitude timezone.

 5.1 If value of pressure is less than 995 Millibar,
 *e-mail will be sent to the stakeholders.*
 
 5.2 If value of pressure is equal or more than 995 Millibar, *no action will be triggered by the script*

## Openweathermap API

`task2_locus` script internally calls openweathermap > one-call-api to fetch the data.

#### API:
- https://openweathermap.org/api/one-call-api

#### Get Hourly weather data prediction from the API

#### URL:

***Request:***

```http
GET  https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=current,minutely,alerts,daily&appid={API key}
```

| Quert Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `lat` | `float` | **Required**. Latitude Value  |
| `lon` | `float` | **Required**. Longitude Value  |
| `exclude` | `comma-delimited list (without spaces)` | **Optional**. Exclude some parts of the weather data from the API response.  |
| `appid` | `string` | **Required**. Unique API key  |


***Response: (200, Success)*** -- Success sample

{

"lat": 25.2048,

"lon": 55.2708,

"timezone": "Asia/Dubai",

"timezone_offset": 14400,

"hourly": [

{

"dt": 1624359600,

"temp": 313.21,

"feels_like": 317.81,

"pressure": 1000,

...

"description": "clear sky",

"icon": "01d"

} ],

"pop": 0

} ] }

## Logic for Code

- Prepare an environment with Python and relevant dependencies installed.
- User inputs Latitude and Longitude value.
- Identify the timezone for the coordinates supplied.
- Evaluate the Unix timestamp for 06:00 AM and 06:00 PM everyday.
- Evaluate the local datetime corresponding to 03:00 AM of target timezone.
- Call the API's Service (Hourly forecast for 48 hours) to retrieve the weather report.
- Loop over each hourly element and check for two conditions:
 - unix timestamp of element is between 06am and 06pm timestamps of the same day.
 - value of pressure is less than 995 Millibar.
- If any of above two conditions is False
 - No action triggered by script.
- If above two conditions are True
 - Store the value of Unix datetime (key) and pressure (value) in dictionary.
 - Send an alert e-mail to the stakeholders.
