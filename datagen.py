import requests
import urllib.parse
import pprint
import time
import datetime

def history_weather(latitude, longitude, scope):
    start_days, end_days = scope
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

import pandas as pd
import random

def data_gen(temp_range, humidity_range, rainfall_range, csv_name):
    temp_data = []
    humid_data = []
    rainfall_data = []
    for b in range(100):
        rain_fall = round(random.uniform(rainfall_range[0], rainfall_range[1]), 2)
        temperature = round(random.uniform(humidity_range[0], humidity_range[1]), 6)
        humidity = round(random.uniform(temp_range[0], temp_range[1]), 6)
        rainfall_data.append(rain_fall)
        temp_data.append(humidity)
        humid_data.append(temperature)

    new_dataf = pd.DataFrame({'temperature':temp_data,
                              'humidity':humid_data,
                              'rainfall':rainfall_data})
    new_dataf.to_csv(f'{csv_name}_data.csv')
    print(f'{csv_name}_data.csv has been saved.')


lat = "14.998"
lon = "121.953"

#Sitaw Scope
scopes = ((27, 21), (20, 14), (13, 7), (6, 0))

temp_range = [(27, 32), (27, 31), (22, 35), (20, 35), (22, 26), (24, 35), (23, 27)]
humidity_range = [(65, 75), (55, 65), (70, 80), (55, 65), (55, 65), (80, 90), (65, 75)]
crops = ["sili", "tomato", "okra", "kalabasa", "sitaw", "talbos ng kamote", "talong"]

rainfall_range = [(66, 83), (63, 105), (53, 113), (81, 121), (76.6, 136.6), (62.5, 125), (83, 125)]

for index in range(len(temp_range)):
    data_gen(temp_range[index], humidity_range[index], rainfall_range[index], crops[index])
    print(f"{crops[index]}.csv is already saved.")
    print("")
#data_gen(lat, lon, scopes, "chili")