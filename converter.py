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

def nitrogen_descriptive(number):
    if number >= 0 and number <= 63:
        desc = "Low"
    elif number >= 64 and number <= 127:
        desc = "Medium"
    elif number >= 128 and number <= 191:
        desc = "High"
    elif number >= 192 and number <= 255:
        desc = "Very High"
    return desc

def phosphorous_descriptive(number):
    if number >= 0 and number <= 51:
        desc = "Low"
    elif number >= 52 and number <= 102:
        desc = "Moderately Low"
    elif number >= 103 and number <= 153:
        desc = "Moderately High"
    elif number >= 154 and number <= 204:
        desc = "High"
    elif number >= 205 and number <= 255:
        desc = "Very High"
    return desc

def potassium_descriptive(number):
    if number >= 0 and number <= 51:
        desc = "Low"
    elif number >= 52 and number <= 102:
        desc = "Sufficient"
    elif number >= 103 and number <= 153:
        desc = "Sufficient+"
    elif number >= 154 and number <= 204:
        desc = "Sufficient++"
    elif number >= 205 and number <= 255:
        desc = "Sufficient+++"
    return desc