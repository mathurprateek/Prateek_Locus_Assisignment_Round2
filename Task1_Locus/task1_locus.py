"""
Objective: Show the atmospheric pressure at 4am as per the coordinate's timezone for the past 3 days.
           This API will be called with inputs.
           This API will call 'One Call API' from https://openweathermap.org/api to populate data.
Input:  Latitude and longitude values for which the atmospheric pressure has to be retrieved.
        User Inputs for Latitude and longitude comes are read from Query Parameters.
Output: JSON format data for past 3 day's atmospheric pressure
        Data: Human Readable Date and corresponding pressure value
"""

import requests
from flask import Flask, jsonify, render_template
from flask_restful import Api, Resource, reqparse, abort
from datetime import datetime as dt, timedelta
from timezonefinder import TimezoneFinder
import pytz

app = Flask(__name__)  # Flask application
api = Api(app)  # Flask  RESTful API wrapper

req_param = reqparse.RequestParser()  # retrieve parsed values from request
req_param.add_argument("lat", type=float, required=True, help="Please enter/check 'Latitude' value")  # latitude value
req_param.add_argument("lon", type=float, required=True, help="Please enter/check 'Longitude' value")  # longitude value


# Renders HTML page for user to input values
@app.route("/")
def index():
    return render_template('index_weather_task1.html')


# abort the execution if latitude or longitude values are invalid
def lat_lon_invalid(lat, lon):
    # if both latitude or longitude values are invalid
    if (-90 > lat or 90 < lat) and (-180 > lon or 180 < lon):
        abort(404, message=f"Invalid Latitude {lat} and Longitude {lon} value entered,"
                           f" valid Latitude range -90 to 90 decimal degrees,"
                           f" valid Longitude range -180 to 180 decimal degrees")
    # if only latitude value is invalid
    if -90 > lat or 90 < lat:
        abort(404, message=f"Invalid Latitude {lat} value entered, valid values range -90 to 90 decimal degrees")
    # if only longitude value is invalid
    if -180 > lon or 180 < lon:
        abort(404, message=f"Invalid Latitude {lon} value entered, valid values range -180 to 180 decimal degrees")


# creating class resource, extending flask_restful's Resource for API method execution
class AtmPrs(Resource):
    def get(self):  # runs when API is called with GET method request
        arg = req_param.parse_args()  # fetching request parsed values
        if (-90 <= arg["lat"] <= 90) and (-180 <= arg["lon"] <= 180):  # validating latitude and longitude values
            lat, lon = arg["lat"], arg["lon"]
        else:
            lat_lon_invalid(arg["lat"], arg["lon"])
        try:
            tzf_str = TimezoneFinder().timezone_at(lng=lon, lat=lat)  # identifying timezone as per coordinates passed
            tz = pytz.timezone(tzf_str)  # timezone object for identified timezone
            dt_tz = dt.now(tz)  # current time in target timezone
            # setting target timezone's 04 AM datetime
            tz_datetime = dt(dt_tz.year, dt_tz.month, dt_tz.day, 4, tzinfo=tz)
            # UTC offset delta
            utc_dst_delta = dt_tz.utcoffset().total_seconds() - tz_datetime.utcoffset().total_seconds()
            unix_datetime_dict = {}  # dictionary to store unix datetime
            datetime_dict = {}  # dictionary to store human readable datetime

            def last_three_days_unix_time_four_am(today_tz_datetime):  # function to add last 3 day's to unix dictionary
                for i in range(1, 4):
                    datetime_dict[str(today_tz_datetime - timedelta(days=i))[0:19]] = ""
                    unix_datetime_dict[int((today_tz_datetime -
                                            timedelta(days=i, seconds=utc_dst_delta)).timestamp())] = ''
            last_three_days_unix_time_four_am(tz_datetime)
            for k in unix_datetime_dict.keys():  # looping over unix timestamps stored
                res = requests.get(
                    f'https://api.openweathermap.org/data/2.5/onecall/timemachine?lat={lat}&lon={lon}&dt={k}'
                    f'&appid=78385f931961ae9b80060c70d2c7bf6f')  # API calling URL with input values
                unix_datetime_dict[k] = str(res.json()['current']['pressure']) + ' ' + 'Millibar'
            for k, v in zip(datetime_dict.keys(), unix_datetime_dict.values()):
                datetime_dict[k] = v  # setting values in human readable dictionary
        except ValueError as ve:
            return {"Caught an Value Error": ve}
        except KeyError as ke:
            return {"Caught an KeyError": ke}
        except Exception as exc:
            return {"Got an Exception": exc}
        return jsonify({"Atmospheric pressure at 4am for the past 3 days": datetime_dict,
                       "timezone": tzf_str})  # returning human-readable datetime and corresponding pressure values


api.add_resource(AtmPrs, '/AtmPrs')  # Resource setting and endpoint for this API


if __name__ == "__main__":  # API run/main calling method
    app.run(debug=True, host="localhost", port=1111)  # debug True for logging, running API on http://localhost:1111
