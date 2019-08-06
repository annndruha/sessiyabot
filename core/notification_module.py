# Sessiya_bot: notification_module - Always run file for notify
# Маракулин Андрей @annndruha
# 2019
import time as bed

from vk_api import VkApi

from data import config
from data import datebase_functions as dbf
from data import dictionary as dict
from core import dt_func as dt

def write_notify_msg(user_id, message):
    vk = VkApi(token=config.notify_token)
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': dt.datetime_to_random_id()})

def notification_loop():
    while True:
        try:
            while True:
                try:
                    users = dbf.get_users_who_sub_at(dt.time_now_obj())
                except:
                    print('Notification module: Datebase unavailable')

                for user in users:
                    user_id, examdate, notifytime, subscribe, tz, firstname, lastname = user
                    days_to_exam = (examdate - dt.date_now_obj()).days

                    if days_to_exam > 1:
                        ans = dict.random_greeting() + '\n' + dict.exam_message['time_until_exam'] + ' ' + str(days_to_exam) + ' ' + dict.numerals_days(days_to_exam) + '\n' + dict.random_wish()
                    elif days_to_exam == 1:
                        ans = dict.exam_message['exam_tomorrow']
                    elif days_to_exam == 0:
                        ans = dict.exam_message['exam_today']
                    elif days_to_exam == -1:
                        ans = dict.exam_message['exam_in_past']
                    elif days_to_exam < -1:
                        dbf.change_subscribe(user_id, False)
                        ans = dict.exam_message['auto_unsubscribe']
                    write_notify_msg(user_id, ans)
                bed.sleep(10)
        except:
            print('Notification module: Unknown exception')
            bed.sleep(10)