import requests
import urllib.parse
import pprint
import time
import datetime
"""
main_api = "https://history.openweathermap.org/data/2.5/history/city?"

lat = "14.74"
long = "121.15"
units = "metric"
type_time = "hour"
end = str(int(time.time()))
start_date = datetime.datetime.now() - datetime.timedelta(30)
start = str(int(start_date.timestamp()))
url = main_api + urllib.parse.urlencode({'lat': lat,
                                         'lon': long,
                                         'units': units,
                                         'type': type_time, 
                                         'start': start,
                                         'end': end,
                                         'appid': api_key})
print(url)
"""
#https://api.openweathermap.org/data/2.5/weather?lat=35&lon=139&appid={API key}
#http://history.openweathermap.org/data/2.5/history/city?lat={lat}&lon={lon}&type=hour&start={start}&end={end}&appid={API key}

#response = requests.get(url)
#printer = pprint.PrettyPrinter(indent=4)
#printer.pprint(response.json()['list'])

def history_weather(latitude, longitude, scope):
    start_days, end_days = scope
    print(end_days, start_days)
    main_api = "https://history.openweathermap.org/data/2.5/history/city?"
    api_key = "d65ba15079b293faced6eb2e7895685d"
    lat = latitude
    lon = longitude
    units = "metric"
    type_time = "hour"
    end_date = datetime.datetime.now() - datetime.timedelta(end_days)
    end = str(int(end_date.timestamp()))
    start_date = datetime.datetime.now() - datetime.timedelta(start_days)
    start = str(int(start_date.timestamp()))

    url = main_api + urllib.parse.urlencode({'lat': lat,
                                         'lon': lon,
                                         'units': units,
                                         'type': type_time, 
                                         'start': start,
                                         'end': end,
                                         'appid': api_key})

    response = requests.get(url)
    printer = pprint.PrettyPrinter(indent=4)
    rains = []
    for a in response.json()['list']:
        if 'rain' in a:
            rains.append(a['rain']['1h'])
    return rains

rain_list = []
scopes = ((27, 21), (20, 14), (13, 7), (6, 0))

for scope in scopes:
    rain_list.append(history_weather("14.74", "121.25", scope))
rainfall = 0
for a in rain_list:
    print(sum(a))
    rainfall += sum(a)
print(rainfall)

def current_weather(latitude, longitude):
    main_api = "https://pro.openweathermap.org/data/2.5/weather?"
    api_key = "d65ba15079b293faced6eb2e7895685d"
    lat = latitude
    lon = longitude
    units = "metric"

    url = main_api + urllib.parse.urlencode({'lat': lat,
                                         'lon': lon,
                                         'units': units,
                                         'appid': api_key})

    response = requests.get(url)
    printer = pprint.PrettyPrinter(indent=4)
    temp = response.json()['main']['temp']
    humidity = response.json()['main']['humidity']

    return temp, humidity

#temp, humidity = current_weather("14.74", "121.25")
#print(f"Temperature: {temp}")
#print(f"Humidity: {humidity}")