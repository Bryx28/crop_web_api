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
