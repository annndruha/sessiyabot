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
from data.class_user import User
from func import database_functions as db
from func import datetime_functions as dt
from func import chat_functions as chat

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
                for data in users:
                    user_id, examdate, notifytime, subscribe, tz, firstname, lastname = data
                    user = User(user_id, 'None', firstname, lastname)
                    ans = chat.sessiya_mesage(user, 'notify')
                    write_notify_msg(user_id, ans)
                    last_send_time = dt.time_now_obj()
            time.sleep(10)

        except psycopg2.Error as err:
            print(time.strftime("---[%Y-%m-%d %H:%M:%S] psycopg2.Error error (notify_loop), description:", time.localtime()))
            #traceback.print_tb(err.__traceback__)
            print('\t'+str(err.args))
            try:
                print(str(time.strftime("---[%Y-%m-%d %H:%M:%S] Try to recconnect database", time.localtime())))
                db.reconnect()
                print(str(time.strftime("---[%Y-%m-%d %H:%M:%S] Database connected successful", time.localtime())))
            except:
                print(str(time.strftime("---[%Y-%m-%d %H:%M:%S] Recconnect database failed", time.localtime())))
                time.sleep(10)
                print(str(time.strftime("---[%Y-%m-%d %H:%M:%S] NOTIFY MODULE RESTART", time.localtime())))
        except OSError as err:
            print(str(time.strftime("---[%Y-%m-%d %H:%M:%S] OSError (notify_loop), description:", time.localtime())))
            #traceback.print_tb(err.__traceback__)
            print('\t'+str(err.args))
            try:
                print(str(time.strftime("---[%Y-%m-%d %H:%M:%S] Try to recconnect VK...", time.localtime())))
                vk_reconnect()
                print(str(time.strftime("---[%Y-%m-%d %H:%M:%S] VK connected successful", time.localtime())))
            except:
                print(str(time.strftime("---[%Y-%m-%d %H:%M:%S] Recconnect VK failed", time.localtime())))
                time.sleep(10)
                print(str(time.strftime("---[%Y-%m-%d %H:%M:%S] NOTIFY MODULE RESTART", time.localtime())))
        except BaseException as err:
            print(str(time.strftime("---[%Y-%m-%d %H:%M:%S] Unknown Exception (notify_loop):", time.localtime())))
            traceback.print_tb(err.__traceback__)
            print('\t'+str(err.args))
            time.sleep(10)
            print(str(time.strftime("---[%Y-%m-%d %H:%M:%S] NOTIFY MODULE RESTART", time.localtime())))