import requests
from decouple import config
import urllib.parse

def date_to_words(month, day):
    months = ["January", "February", "March",
              "April", "May", "June",
              "July", "August", "September",
              "October", "November", "December"]
    word_month = months[month-1]
    if day <= 9:
        str_day = "0" + str(day)
    else:
        str_day = str(day)
    return word_month, str_day

def number_formatting(time):
    if time <= 9:
        str_num = "0" + str(time)
    else:
        str_num = str(time)
    return str_num

def crop_counter(crop_list, crop_dict):
    for x in crop_list:
        for crop in crop_dict:
            if x == crop:
                crop_dict[crop] += 1
    
    return crop_dict

def nitrogen_descriptive(number):
    if number >= 0 and number <= 107:
        desc = "Low"
    elif number >= 107 and number <= 214:
        desc = "Medium"
    elif number >= 214 and number <= 249:
        desc = "High"
    elif number >= 250 and number <= 255:
        desc = "Very High"
    return desc

def phosphorous_descriptive(number):
    if number >= 0 and number <= 75:
        desc = "Low"
    elif number >= 76 and number <= 113:
        desc = "Moderately Low"
    elif number >= 114 and number <= 150:
        desc = "Moderately High"
    elif number >= 151 and number <= 250:
        desc = "High"
    elif number >= 251 and number <= 255:
        desc = "Very High"
    return desc

def potassium_descriptive(number):
    if number >= 0 and number <= 75:
        desc = "Low"
    elif number >= 76 and number <= 113:
        desc = "Sufficient"
    elif number >= 114 and number <= 150:
        desc = "Sufficient+"
    elif number >= 151 and number <= 250:
        desc = "Sufficient++"
    elif number >= 251 and number <= 255:
        desc = "Sufficient+++"
    return desc

def current_weather(latitude, longitude):
    main_api = "https://pro.openweathermap.org/data/2.5/weather?"
    api_key = config('API_KEY')
    lat = latitude
    lon = longitude
    units = "metric"

    url = main_api + urllib.parse.urlencode({'lat': lat,
                                         'lon': lon,
                                         'units': units,
                                         'appid': api_key})

    response = requests.get(url)
    temp = response.json()['main']['temp']
    humidity = response.json()['main']['humidity']

    return temp, humidity

def history_weather(latitude, longitude, start, end):
    main_api = "https://history.openweathermap.org/data/2.5/history/city?"
    api_key = config('API_KEY')
    lat = latitude
    lon = longitude
    units = "metric"
    type_time = "hour"

    url = main_api + urllib.parse.urlencode({'lat': lat,
                                         'lon': lon,
                                         'units': units,
                                         'type': type_time, 
                                         'start': start,
                                         'end': end,
                                         'appid': api_key})

    response = requests.get(url)
    rains = []
    for a in response.json()['list']:
        if 'rain' in a:
            rains.append(a['rain']['1h'])
    return rains

def recommended_crops(results):
    categories = ['apple', 'banana', 'blackgram', 'chickpea', 'coconut', 'coffee',
       'cotton', 'grapes', 'jute', 'kalabasa', 'kamatis', 'kidneybeans',
       'lentil', 'maize', 'mango', 'mothbeans', 'mungbean', 'muskmelon',
       'okra', 'orange', 'papaya', 'pigeonpeas', 'pomegranate', 'rice',
       'sili', 'sitaw', 'talbos ng kamote', 'talong', 'watermelon']

    probability_crops = dict(zip(categories, [x for x in results[0]]))

    crop_list = sorted(probability_crops.items(), key=lambda x:x[1])

    recommended = ""
    for a in range(len(categories)):
        crop = crop_list[(-a-1)]
        recommended += crop[0]
        if a == 2:
            break
        recommended += ","

    return recommended


