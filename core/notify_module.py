# sessiyabot/core/notification_module
# - Exam notify always run file
# Маракулин Андрей @annndruha
# 2019
import time
import traceback

from vk_api import VkApi
import psycopg2

from data import config
from data import dictionary as dict
from func import database_functions as db
from func import datetime_functions as dt
from func import chat_functions as chf

def write_notify_msg(user_id, message):
    vk = VkApi(token=config.access_token)
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': dt.datetime_to_random_id()})

def notify_loop():
    last_send_time = -1
    while True:
        try:
            if (last_send_time != dt.time_now_obj()):
                last_send_time = -1
                users = db.get_users_who_sub_at(dt.time_now_obj())
                for user in users:
                    user_id, examdate, notifytime, subscribe, tz, firstname, lastname = user
                    #greeting(notifytime)
                    days_to_exam = chf.get_days_to_exam(user_id)
                    
                    if days_to_exam > 1:
                        ans = dict.random_greeting() + ', ' + firstname + '! ' + chf.chat_sessiya_mesage(user_id) + ' ' + dict.random_wish()
                    elif days_to_exam == 1:
                        ans = dict.exam_message['exam_tomorrow']
                    elif days_to_exam == 0:
                        ans = dict.exam_message['exam_today']
                    elif days_to_exam == -1:
                        ans = dict.exam_message['exam_in_past']
                    elif days_to_exam < -1:
                        db.set_subscribe(user_id, False)
                        ans = dict.exam_message['auto_unsubscribe']
                    
                    write_notify_msg(user_id, ans)
                    last_send_time = dt.time_now_obj()
            time.sleep(10)
        except psycopg2.Error as err:
            print(time.strftime("---[%Y-%m-%d %H:%M:%S] psycopg2.Error, description:", time.localtime()))
            traceback.print_tb(err.__traceback__)
            print(str(err.args))
            try:
                print(str(time.strftime("---[%Y-%m-%d %H:%M:%S] Try to recconnect database", time.localtime())))
                db.reconnect()
                print(str(time.strftime("---[%Y-%m-%d %H:%M:%S] Database connected successful", time.localtime())))
            except:
                print(str(time.strftime("---[%Y-%m-%d %H:%M:%S] Recconnect database failed", time.localtime())))
                time.sleep(10)
                print('-------------------------\tNOTIFY MODULE REBOOT\t------------------------')
        except BaseException as err:
            print(str(time.strftime("---[%Y-%m-%d %H:%M:%S] BaseException in notify_module, way:", time.localtime())))
            traceback.print_tb(err.__traceback__)
            print(str(err.args))
            time.sleep(10)
            print('-------------------------\tNOTIFY MODULE REBOOT\t------------------------')