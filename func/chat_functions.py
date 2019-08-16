# sessiyabot/func/chat_fuctions
# - analyze chat user commands
# Маракулин Андрей @annndruha
# 2019
from data import dictionary as dict
from func import database_functions as db
from func import datetime_functions as dt

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

def sessiya_mesage(user, param):
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
    if param == 'chat':
        if days_to_exam > 1:
            ans = dict.exam_message[s + 'time_until_exam'] + str(days_to_exam) + dict.numerals_days(days_to_exam) + '. ' + dict.exam_message['exam_date']+ dt.date_to_str(examdate)
        elif days_to_exam == 1:
            ans = dict.exam_message[s + 'exam_tomorrow']
        elif days_to_exam == 0:
            ans = dict.exam_message[s + 'exam_today']
        elif days_to_exam < 0:
            ans = dict.exam_message[s + 'ask_exam_past']

    elif param == 'notify':
        if days_to_exam > 1:
            ans = dict.random_greeting() + ', ' + firstname + '! ' + dict.exam_message[s + 'time_until_exam'] + str(days_to_exam) + dict.numerals_days(days_to_exam) + '. ' + dict.random_wish()
        elif days_to_exam == 1:
            ans = dict.exam_message['exam_tomorrow']
        elif days_to_exam == 0:
            ans = dict.exam_message['exam_today']
        elif days_to_exam == -1:
            ans = dict.exam_message['exam_in_past']
        elif days_to_exam < -1:
            db.set_subscribe(user_id, False)
            ans = dict.exam_message['auto_unsubscribe']

    return ans