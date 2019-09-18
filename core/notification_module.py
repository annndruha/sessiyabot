# sessiyabot/core/notification_module
# - Exam notify always run loop
# Marakulin Andrey @annndruha
# 2019
import time
import traceback

import psycopg2

from data import ru_dictionary as dict
from func import database_functions as db
from func import datetime_functions as dt
from func import vkontakte_functions as vk

def greeting(local_time):
    if local_time < dt.str_to_time('05:40'):
        ans = dict.other['night']
    elif local_time < dt.str_to_time('11:59'):
        ans = dict.other['morning']
    elif local_time < dt.str_to_time('18:00'):
        ans = dict.other['day']
    elif local_time <= dt.str_to_time('23:59'):
        ans = dict.other['evening']
    return ans

def notify_mesage(data):
    # Calculate days_to_exam and s = degree of confidence
    user_id, examdate, notifytime, subscribe, tz, firstname, lastname = data
    if examdate is not None:
        days_to_exam = (examdate - dt.date_now_obj()).days
        s = ''
    else:
        examdate = dt.str_to_date(dict.default_exam_date)
        days_to_exam = (examdate - dt.date_now_obj()).days
        s = 'ns_'

    local_time = dt.shift_time(notifytime,tz)
    # Forming message by call parametr
    if days_to_exam > 1:
        ans = greeting(local_time) + ', ' + firstname + '! ' + dict.exam_message[s + 'time_until_exam'] + str(days_to_exam) + dict.numerals_days(days_to_exam) + '. ' + dict.random_wish()
    elif days_to_exam == 1:
        ans = dict.exam_message[s + 'exam_tomorrow']
    elif days_to_exam == 0:
        ans = dict.exam_message[s + 'exam_today']
    elif days_to_exam == -1:
        ans = dict.exam_message['exam_in_past']
    elif days_to_exam < -1:
        db.set_subscribe(user_id, False)
        ans = dict.exam_message['auto_unsubscribe']
    return ans

#Main code
def notify_loop():
    print(str(time.strftime("===[%Y-%m-%d %H:%M:%S] NOTIFY MODULE START", time.gmtime())))
    last_send_time = -1
    while True:
        try:
            if (last_send_time != dt.time_now_obj()):
                last_send_time = -1
                users = db.get_users_who_sub_at(dt.time_now_obj())
                for data in users:
                    user_id, examdate, notifytime, subscribe, tz, firstname, lastname = data

                    ans = notify_mesage(data)
                    vk.write_notify_msg(data[0], ans)
                    last_send_time = dt.time_now_obj()
            time.sleep(10)

        except psycopg2.Error as err:
            print(time.strftime("---[%Y-%m-%d %H:%M:%S] psycopg2.Error error (notify_loop), description:", time.gmtime()))
            #traceback.print_tb(err.__traceback__)
            print(err.args[0])
            try:
                print(str(time.strftime("---[%Y-%m-%d %H:%M:%S] Try to recconnect database", time.gmtime())))
                db.reconnect()
                print(str(time.strftime("---[%Y-%m-%d %H:%M:%S] Database connected successful", time.gmtime())))
                time.sleep(2)
            except:
                print(str(time.strftime("---[%Y-%m-%d %H:%M:%S] Recconnect database failed", time.gmtime())))
                time.sleep(10)
            print(str(time.strftime("===[%Y-%m-%d %H:%M:%S] NOTIFY MODULE RESTART", time.gmtime())))
        except OSError as err:
            print(str(time.strftime("---[%Y-%m-%d %H:%M:%S] OSError (notify_loop), description:", time.gmtime())))
            #traceback.print_tb(err.__traceback__)
            print(err.args[0])
            try:
                print(str(time.strftime("---[%Y-%m-%d %H:%M:%S] Try to recconnect VK...", time.gmtime())))
                vk.reconnect()
                print(str(time.strftime("---[%Y-%m-%d %H:%M:%S] VK connected successful", time.gmtime())))
                time.sleep(2)
            except:
                print(str(time.strftime("---[%Y-%m-%d %H:%M:%S] Recconnect VK failed", time.gmtime())))
                time.sleep(10)
            print(str(time.strftime("===[%Y-%m-%d %H:%M:%S] NOTIFY MODULE RESTART", time.gmtime())))
        except BaseException as err:
            print(str(time.strftime("---[%Y-%m-%d %H:%M:%S] Unknown Exception (notify_loop):", time.gmtime())))
            traceback.print_tb(err.__traceback__)
            print(err.args[0])
            time.sleep(10)
            print(str(time.strftime("===[%Y-%m-%d %H:%M:%S] NOTIFY MODULE RESTART", time.gmtime())))
        except:
            print('---Something go wrong. (notify_loop)')