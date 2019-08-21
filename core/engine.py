# sessiyabot/core/engine
# - run chat commands and others
# Marakulin Andrey @annndruha
# 2019
from math import sin, cos, tan, acos, asin, atan, sinh, cosh, tanh, asinh, acosh, atanh
from math import sqrt, pow, exp, log, log10, log2
from math import factorial, degrees, radians, pi, e

from data import ru_dictionary as dict
from func import datetime_functions as dt
from func import database_functions as db

# Start notify or change notify time
def time(user):
    data = db.get_user(user.user_id)
    if (len(user.message.split(' ')) < 2):
        if data == None:
            ans = dict.db_ans['notify_doesnt_exist']
        else:
            user_id, examdate, notifytime, subscribe, tz, firstname, lastname = data
            if notifytime == None:
                ans = dict.db_ans['notify_doesnt_exist']
            else:
                local_time = dt.shift_time(notifytime, tz)
                str_user_time = dt.time_to_str(local_time)
                db.set_subscribe(user.user_id, True)
                ans = dict.db_ans['sub_back'] + str_user_time

    elif (dt.validate_time(user.message.split(' ')[1]) == False):
        ans = dict.db_ans['incorrect_time']
    else:
        str_user_time = user.message.split(' ')[1]
        new_user_time = dt.str_to_time(str_user_time)

        if data == None:
            db.add_user_with_time(user.user_id, new_user_time, True, user.first_name, user.last_name)
            ans = dict.db_ans['start_notify'] + str_user_time
        else:
            user_id, examdate, notifytime, subscribe, tz, firstname, lastname = data
            if notifytime == None:
                ans = dict.db_ans['sub_first'] + str_user_time
            elif subscribe == False:
                ans = dict.db_ans['sub_back'] + str_user_time
            else:
                ans = dict.db_ans['set_time'] + str_user_time
            time_for_db = dt.shift_time(new_user_time, -tz)
            db.update_user_time_and_sub(user.user_id, time_for_db, True)
    return ans

#Change or set exam date
def date(user):
    if (len(user.message.split(' ')) < 2):
        ans = dict.db_ans['incorrect_date']
    elif (dt.validate_date(user.message.split(' ')[1]) == False):
        ans = dict.db_ans['incorrect_date']
    else:
        str_user_date = user.message.split(' ')[1]
        new_user_date = dt.str_to_date(str_user_date)

        if (db.get_user(user.user_id) == None):
            db.add_user_with_date(user.user_id, new_user_date, user.first_name, user.last_name)
            ans = dict.db_ans['set_date'] + str_user_date
        else:
            db.set_examdate(user.user_id, new_user_date)
            ans = dict.db_ans['set_date'] + str_user_date
    return ans

#Change time zone
def tz(user):
    if (len(user.message.split(' ')) < 2):
        ans = dict.db_ans['incorrect_tz']
    elif (dt.validate_tz(user.message.split(' ')[1]) == False):
        ans = dict.db_ans['incorrect_tz']
    else:
        new_user_tz = int(user.message.split(' ')[1])
        data = db.get_user(user.user_id)
        if data == None:
            db.add_user_with_tz(user.user_id, new_user_tz, user.first_name, user.last_name)
            ans = dict.db_ans['set_tz'] + dict.tz_format(new_user_tz)
        else:
            user_id, examdate, notifytime, subscribe, tz, firstname, lastname = data
            tz_shift = new_user_tz - tz
            db.set_tz(user.user_id,new_user_tz)

            if notifytime is not None:
                new_time = dt.shift_time(notifytime, -tz_shift)
                db.set_notifytime(user.user_id,new_time)
                if examdate is not None:
                    new_examdate = dt.shift_date(examdate, -tz_shift, notifytime)
                    db.set_examdate(user.user_id, new_examdate)
            ans = dict.db_ans['set_tz'] + dict.tz_format(new_user_tz)
    return ans

# Stop notify message from user
def stop(user):
    data = db.get_user(user.user_id)
    if data == None:
        ans = dict.db_ans['no_sub']
    else:
        user_id, examdate, notifytime, subscribe, tz, firstname, lastname = data
        if (subscribe == False):
            ans = dict.db_ans['unfollow_yet']
        else:
            db.set_subscribe(user.user_id, False)
            ans = dict.db_ans['unfollow']
    return ans

# Sessiya mesage return days to exam
def sessiya_mesage(user):
    data = db.get_user(user.user_id)
    # Calculate days_to_exam and s = degree of confidence
    if data is not None:
        user_id, examdate, notifytime, subscribe, tz, firstname, lastname = data
        if examdate is not None:
            days_to_exam = (examdate - dt.date_now_obj()).days
            s = ''
        else:
            examdate = dt.str_to_date(dict.default_exam_date)
            days_to_exam = (examdate - dt.date_now_obj()).days
            s = 'ns_'
    else:
        user_id = user.user_id
        examdate = dt.str_to_date(dict.default_exam_date)
        days_to_exam = (examdate - dt.date_now_obj()).days
        s = 'ns_'

    # Forming message by call parametr
    if days_to_exam > 1:
        ans = dict.exam_message[s + 'time_until_exam'] + str(days_to_exam) + dict.numerals_days(days_to_exam) + '. ' + dict.exam_message['exam_date'] + dt.date_to_str(examdate)
    elif days_to_exam == 1:
        ans = dict.exam_message[s + 'exam_tomorrow']
    elif days_to_exam == 0:
        ans = dict.exam_message[s + 'exam_today']
    elif days_to_exam < 0:
        ans = dict.exam_message[s + 'ask_exam_past']
    return ans

#bookmarks bar
replace = {
    'i':'j',
    'факториал':'factorial',
    'чёртова дюжина':'13',
    'чертова дюжина':'13',
    'дюжина':'12',
    'возвести в степень':'**',
    'умножить на': '*',
    'разделить на':'/',
    'мнимое':'j',
    'сложить с':'+',
    'единица':'1',
    'едино':'1',
    'один':'1',
    'ноль':'0',
    'два':'2',
    'три':'3',
    'четыре':'4',
    'пять':'5',
    'шесть':'6',
    'восемь':'8',
    'семь':'7',
    'факт':'factorial',
    'девять':'9',
    'десять':'10',

    'умножить':'*',
    'плюс':'+',
    'минус':'-',
    'отнять':'-',
    'корень':'sqrt',
    'точка':'.',

    'в степени':'**',
    'разделить':'/',
    'прибавить':'+',

    'жды':'*',
    'на':'*',
    'ю':'*',

    '^':'**',
    ' ':''

    #'десять':'10',
    #'двадцать':'20',
    #'тридцать':'30',
    #'сорок':'40',
    #'пятьдесят':'50',
    #'шестьдесят':'60',
    #'семьдесят':'70',
    #'восемьдесят':'80',
    #'девяносто':'90',
    }

def validate_expression(message):
    for word in replace:
        if message.find(word) >= 0:
            message = message.replace(word, replace[word])
    #Проверить выражение
    return message

def calculator(message):#New thread + alert timer
    message = validate_expression(message)
    print('Вы ввели: ' + str(message.replace('**','^').replace('j','i')))
    try:
        response = str(eval(message))
        response = response.replace('j','i')
        response = response.replace('(','')
        response = response.replace(')','')
        #округлить?
        print('Ответ: ' + response)
        return response
    except:
        response = 'Не могу посчитать'
        print(response)
        return response


#print('start')
#while True:
#    print(calculate(input()))