import datetime as dt
from pytz import timezone

import wikipedia
from  dictionary import days_cases
from  dictionary import exam_message
from  dictionary import random_not_found

import config
wikipedia.set_lang(config.wiki_language)

# DateTime class functions
def datetime_now_obj():
    return dt.datetime.now(timezone('Europe/Moscow'))

def datetime_to_str(datetime_object):
    return dt.datetime.strftime(datetime_object, '%d.%m.%Y %H:%M')

def str_to_datetime(string):#Set timezone automaticly
    return dt.datetime.strptime(string, '%d.%m.%Y %H:%M')

# Date class functions
def date_now_obj():
    return datetime_now_obj().date()

def date_to_str(date_obj):
    return dt.date.strftime(date_obj, '%d.%m.%Y')

def str_to_date(string):
    return dt.datetime.strptime(string, '%d.%m.%Y').date()

# Time class functions
def time_now_obj():
    return dt.time(datetime_now_obj().hour, datetime_now_obj().minute)

def time_to_str(time_obj):
    return dt.time.strftime(time_obj, '%H:%M')

def str_to_time(string):
    return dt.datetime.strptime(string, '%H:%M').time()

# Validate format functions
def validate_date(date_text):
    try:
        if date_text != datetime.strptime(date_text, "%d.%m.%Y").strftime('%d.%m.%Y'):
            raise ValueError
        return True
    except ValueError:
        return False

def validate_time(time_text):
    try:
        if time_text != datetime.strptime(time_text, "%H:%M").strftime('%H:%M'):
            raise ValueError
        return True
    except ValueError:
        return False

# Logs timestamp
def timestamp():
    return dt.datetime.strftime(datetime_now_obj(), '%d.%m.%Y %H:%M:%S')

def datetime_to_random_id():
    i = dt.datetime.strftime(datetime_now_obj(), '%y%m%d%H%M')
    return int(i)

# Chat functions
def numerals_days(n):
    if ((10 < n) and (n < 20)):
        return days_cases['genitive_many']
    else:
        n = n % 10
        if ((n == 0) or (n >= 5)):
            return days_cases['genitive_many']
        elif n == 1:
            return days_cases['nominative']
        elif ((n > 1) and (n < 5)):
            return days_cases['genitive']

def sessiya_mesage(user_id):
    first_exam = config.default_exam_date
    today = date_now_obj()

    try:
        users = open(config.users_filename)
        lines = users.read().splitlines()
        users.close()
    except:
        print("[{}] Engine: Sessiya message: File open error".format(timestamp()))

    for line in lines:
        if (line.find(str(user_id)) >= 0):
            user_line = line.split(' ')
            user_exam_date = str_to_date(user_line[1])
            days_to_exam = (user_exam_date - date_now_obj()).days

    if days_to_exam < -2:
        return exam_message['ask_exam_past']
    elif days_to_exam <= 0:
        return exam_message['sessiya_going']
    else:
        return exam_message['time_until_exam'] + str(days_to_exam) + ' ' + numerals_days(days_to_exam)

def find_in_wiki(wiki_request):
    try:
        n = 2
        exit = 0

        while ((n < 5) and (exit == 0)):
            exit = 1
            ans = str(wikipedia.summary(wiki_request, sentences=n, auto_suggest=True))
            if ((ans.rfind('(')) > (ans.rfind(')'))):
                n = n + 1
                exit = 0
            if len(ans) < 100:
                n = n + 1
                exit = 0
        if ans.find('=='):
            ans = ans[:(ans.find('==') - 1)]
    except:
        ans = random_not_found()
    return ans
