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