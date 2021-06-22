
# Show Atmospheric pressure
### At 4am for the past 3 days from the day of running the API

#### *Python Version*:
This API runs on Python version 3.6 or above.

#### *Objective*:
Display the atmospheric pressure at 4am for the past 3 days
as per the timezone of input latitude and longitude.

*Task1_locus API* will internally call 'One Call API' from https://openweathermap.org/api to populate data.

*Service: Historical weather data for the previous 5 days*

#### *Input*:
**Latitude** and **longitude** values for which the atmospheric pressure has to be retrieved.

User Inputs for Latitude and Longitude are read as *Query Parameters* (can be done in two ways)
- via HTML rendered page when API loads.
- values can be directly passed in the URL.

#### *Output*:
JSON format data for past 3 day's atmospheric pressure.

Human Readable datetime with corresponding pressure value, along with timezone information.


#### *Data Flow*:

1. Input Flow 
- User Input **>>** Task1_locus API **>>** openweathermap.org/api
2. Output Flow 
- openweathermap.org/api **>>** Task1_locus API **>>** Output to User 

## Dependencies

#### Python packages/libraries for builing API

1. import **requests**
*The requests library is the standard for making HTTP requests in Python.*

2. from **flask** import **Flask, jsonify, render_template**
*Micro web framework written in Python*

3. from **flask_restful** import **Api, Resource, reqparse**
*Flask-RESTful is an extension for Flask that adds support for building REST APIs.*

4. from **datetime** import **datetime** as dt, **timedelta**
*The datetime module supplies classes for manipulating dates and times.*

5. from **timezonefinder** import **TimezoneFinder**
*Fast python package for finding the timezone of any point on earth*

6. import **pytz**
*This library allows accurate and cross platform timezone calculations using Python 2.4 or higher.*


## Instructions to run the API

#### Using [PyCharm](https://www.jetbrains.com/pycharm/download/#section=windows) tool to create, test and run the API.

1. [Install Dependencies](https://www.jetbrains.com/help/pycharm/installing-uninstalling-and-upgrading-packages.html#interpreter-settings) in PyCharm,
as mentioned in the earlier section

2. [Configure Virtual Environment](https://www.jetbrains.com/help/pycharm/creating-virtual-environment.html) in PyCharm.

3. Place "task1_locus.py" file under root folder.

4. Create a folder "templates", under root folder.

4.1 Place HTML file 'index_weather_task1.html' here.

5. [Run](https://www.jetbrains.com/help/pycharm/creating-and-running-your-first-python-project.html#run) the API task1_locus.py.

5.1 API will run on http://127.0.0.3:1111/

5.2 Launch an Internet Browser and hit http://127.0.0.3:1111/ from search bar.

5.3 Enter the value for Latitude and Longitude, click submit.

6. Output will be displayed  
- Past 3 days at 4:00 AM and corresponding Pressure
- Timezone information

*Install JSON plug-in to the Internet Browser for better [view](https://chrome.google.com/webstore/detail/json-formatter/bcjindcccaagfpapjjmafapmmgkkhgoa?hl=en).*

## task1_locus API Reference

#### Current Hosting:
- Host => 127.0.0.3
- Port => 1111

#### Index Page:

***Request:***

Once the API is running

```http
  GET /
```

Currently configured to run on http://127.0.0.3:1111/.

***Response:***
- HTML page is rendered for user inputs.


#### Get atmospheric pressure 

***Request:***

At 4:00 AM, for past 3 days.

```http
  GET /AtmPrs?lat={lat}&lon={lon}
```

| Quert Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `lat` | `float` | **Required**. Latitude Value  |
| `lon` | `float` | **Required**. Longitude Value  |

*Example:*
```http
  GET /AtmPrs?lat=25.2048&lon=55.2708
```

***Response: (200, success)***

{

"Atmospheric pressure at 4am for the past 3 days": {

"2021-06-19 04:00:00": "998 Millibar",

"2021-06-20 04:00:00": "999 Millibar",

"2021-06-21 04:00:00": "1000 Millibar"

}, "timezone": "Asia/Dubai" }

***Response: (400, Bad Request)*** -- If missed to enter value or added incorrect type of *Latitude*

{

"message": {

"lat": "Please enter/check 'Latitude' value"

} }

***Response: (400, Bad Request)*** -- If missed to enter value or added incorrect type of *Longitude*

{ 

"message": {

"lon": "Please enter/check 'Longitude' value"

} }

***Response: (400, Bad Request)*** -- If type is correct but not a real *Latitude* or *Longitude* value.

{

"Status Code": 400,

"ValueError": "Invalid Latitude or Longitude value"

}
  
## Openweathermap API

`task1_locus` API internally calls openweathermap > one-call-api to fetch the data.

#### API:
- https://openweathermap.org/api/one-call-api


#### Get atmospheric pressure from API

#### URL:

***Request:***

```http
  GET https://api.openweathermap.org/data/2.5/onecall/timemachine?lat={lat}&lon={lon}&dt={k}&appid={appid}
```


| Quert Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `lat` | `float` | **Required**. Latitude Value  |
| `lon` | `float` | **Required**. Longitude Value  |
| `dt` | `Unix time, UTC time zone` | **Required**. Datetime from the previous days  |
| `appid` | `string` | **Required**. Unique API key  |


***Response: (200, Success)*** -- Success sample

{

"lat": 25.2048,

"lon": 55.2708,

"timezone": "Asia/Dubai",

"timezone_offset": 14400,

"current": {

"dt": 1624268123,

...

"feels_like": 315.1,

"pressure": 1000,

"humidity": 13,

...

}

***Response: (400, Bad Request)*** -- if unix time passed is older than 5 days

{

"cod": "400",

"message": "requested time is out of allowed range of 5 days back"

}

## Logic for Code

- Prepare a running Python + flask_restful API with dependencies.
- Render a HTML page for taking user inputs (Latitude & Longitude).
- User inputs are passed as Query Parameters to the URL.
- Query Parameters are intercepted with RequestParser to fetch values of Latitude & Longitude.
- Identify the coordinate's timezone with TimezoneFinder.
- Set target time to 04 AM Datetime.
- Calculate the UTC offset and find Unix timestamps to be passed to the openweathermap API URL.
- Call API for a day each to retrieve the Pressure as per the timestamp.
- Store the Unix timestamp as key and pressure values in 'unix_datetime_dict' dictionary.
- Pass the pressure values to human-readable 'datetime_dict' dictionary as per the respective unix timestamps.
- Return the human-readable 'datetime_dict' dictionary and timezone value as JSON output.
