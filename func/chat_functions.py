# sessiyabot/func/chat_fuctions
# - analyze chat user commands
# Маракулин Андрей @annndruha
# 2019
import wikipedia

from data import dictionary as dict
from func import database_functions as db
from func import datetime_functions as dt

# Start notify or change notify time
def chat_time(user_id, message, user_first_name, user_last_name):
    try:
        if (len(message.split(' ')) < 2):
            if (db.get_user_notifytime(user_id) != None):
                db_user_time = db.get_user_notifytime(user_id)
                tz = db.get_user_tz(user_id)
                local_time = dt.shift_time(db_user_time, tz)
                str_user_time = dt.time_to_str(local_time)

                db.set_subscribe(user_id, True)
                ans = dict.db_ans['sub_first'] + str_user_time
            else:
                ans = dict.db_ans['notify_doesnt_exist']
        elif (dt.validate_time(message.split(' ')[1]) == False):
            ans = dict.db_ans['incorrect_time']
        else:
            str_user_time = message.split(' ')[1]
            new_user_time = dt.str_to_time(str_user_time)

            if (db.get_user_exist(user_id) == False):
                db.add_user(user_id)
                db.set_firstname(user_id, user_first_name)
                db.set_lastname(user_id, user_last_name)
                db.set_notifytime(user_id, new_user_time)
                db.set_subscribe(user_id, True)
                ans = dict.db_ans['start_notify'] + str_user_time
            else:
                if (db.get_user_notifytime(user_id) == None):
                    ans = dict.db_ans['sub_first'] + str_user_time
                elif (db.get_user_subscribe(user_id) == False):
                    ans = dict.db_ans['sub_back'] + str_user_time
                else:
                    ans = dict.db_ans['set_time'] + str_user_time
                tz = db.get_user_tz(user_id)
                time_for_db = dt.shift_time(new_user_time, -tz)
                db.set_notifytime(user_id,time_for_db)
                db.set_subscribe(user_id, True)
    except:
        print('Chat functions: Chat_time: Exception')
        ans = dict.db_ans['not_available']
    return ans

#Change or set exam date
def chat_date(user_id, message, user_first_name, user_last_name):
    try:
        if (len(message.split(' ')) < 2):
            ans = dict.db_ans['incorrect_date']
        elif (dt.validate_date(message.split(' ')[1]) == False):
            ans = dict.db_ans['incorrect_date']
        else:
            str_user_date = message.split(' ')[1]
            new_user_date = dt.str_to_date(str_user_date)

            if (db.get_user_exist(user_id) == False):
                db.add_user(user_id)
                db.set_firstname(user_id, user_first_name)
                db.set_lastname(user_id, user_last_name)
                db.set_examdate(user_id, new_user_date)
                ans = dict.db_ans['set_date'] + str_user_date
            else:
                db.set_examdate(user_id,new_user_date)
                ans = dict.db_ans['set_date'] + str_user_date
    except:
        print('Chat functions: Chat_date: Exception')
        ans = dict.db_ans['not_available']
    return ans

#Change time zone
def chat_tz(user_id, message, user_first_name, user_last_name):
    try:
        if (len(message.split(' ')) < 2):
            ans = dict.db_ans['incorrect_tz']
        elif (dt.validate_tz(message.split(' ')[1]) == False):
            ans = dict.db_ans['incorrect_tz']
        else:
            new_user_tz = int(message.split(' ')[1])

            if (db.get_user_exist(user_id) == False):
                db.add_user(user_id)
                db.set_firstname(user_id, user_first_name)
                db.set_lastname(user_id, user_last_name)
                db.set_tz(user_id, new_user_tz)
                ans = dict.db_ans['set_tz'] + dict.tz_format(new_user_tz)
            else:
                old_tz = db.get_user_tz(user_id)
                db.set_tz(user_id,new_user_tz)
                tz_shift = new_user_tz - old_tz

                if (db.get_user_notifytime(user_id) != None):
                    old_time = db.get_user_notifytime(user_id)
                    new_time = dt.shift_time(old_time, -tz_shift)
                    db.set_notifytime(user_id,new_time)

                ans = dict.db_ans['set_tz'] + dict.tz_format(new_user_tz)
    except:
        print('Chat functions: Chat_tz: Exception')
        ans = dict.db_ans['not_available']
    return ans

# Stop notify message from user
def chat_stop(user_id, message):
    try:
        if (db.get_user_notifytime(user_id) == None):
            ans = dict.db_ans['no_sub']
        elif (db.get_user_subscribe(user_id) == False):
            ans = dict.db_ans['unfollow_yet']
        else:
            db.set_subscribe(user_id, False)
            ans = dict.db_ans['unfollow']
    except:
        print('Chat functions:: Chat_stop: Exception')
        ans = dict.db_ans['not_available']
    return ans

def get_days_to_exam(user_id):
    if (db.get_user_examdate(user_id) != None):
        local_date = db.get_user_examdate(user_id)
    else:
        local_date = dt.str_to_date(dict.default_exam_date)
    examdate = dt.shift_date(local_date, db.get_user_tz(user_id))
    days_to_exam = (examdate - dt.date_now_obj()).days
    return days_to_exam

def chat_sessiya_mesage(user_id):
    try:
        if (db.get_user_examdate(user_id) != None):
            s = ''
        else:
            s = 'ns_'
        days_to_exam = get_days_to_exam(user_id)

        if days_to_exam > 1:
            ans = dict.exam_message[s + 'time_until_exam'] + str(days_to_exam) + dict.numerals_days(days_to_exam) + '.'
        elif days_to_exam == 1:
            ans = dict.exam_message[s + 'exam_tomorrow']
        elif days_to_exam == 0:
            ans = dict.exam_message[s + 'exam_today']
        elif days_to_exam < 0:
            ans = dict.exam_message[s + 'ask_exam_past']
    except:
        print('Chat functions:: Sessiya_message: Exception')
        ans = dict.db_ans['forget']
    return ans

def chat_find_in_wiki(user_id, message):
    try:
        wikipedia.set_lang(dict.wiki_language)
        n = 2
        max_n = 5
        exit = 0

        while ((n < max_n) and (exit == 0)):
            exit = 1
            ans = str(wikipedia.summary(message, sentences=n, auto_suggest=True))
            if ((ans.rfind('(')) > (ans.rfind(')'))):
                n = n + 1
                exit = 0
            if len(ans) < 100:
                n = n + 1
                exit = 0
        if ans.find('\n\n'):
            ans = ans[:(ans.find('\n\n'))]
    except:
        ans = dict.random_not_found()
    return ans