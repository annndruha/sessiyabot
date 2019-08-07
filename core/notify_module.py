# Sessiya_bot: notification_module - Always run file for notify
# Маракулин Андрей @annndruha
# 2019
import time as bed

from vk_api import VkApi

from data import config
from data import dictionary as dict

from func import datebase_functions as db
from func import datetime_functions as dt
from func import chat_functions as chf

def write_notify_msg(user_id, message):
    vk = VkApi(token=config.access_token)
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': dt.datetime_to_random_id()})

def notify_loop():
    print('Notify module start')
    while True:
        try:
            last_send_time = -1
            while True:
                if (last_send_time != dt.time_now_obj()):
                    last_send_time = -1

                    users = db.get_users_who_sub_at(dt.time_now_obj())
                    for user in users:
                        user_id, examdate, notifytime, subscribe, tz, firstname, lastname = user
                        days_to_exam = chf.get_days_to_exam(user_id)

                        if days_to_exam > 1:
                            if (firstname!=None):
                                ans = dict.random_greeting()+', '+ firstname + '! ' + chf.chat_sessiya_mesage(user_id) + ' ' + dict.random_wish()
                            else:
                                ans = dict.random_greeting()+'! ' + chf.chat_sessiya_mesage(user_id) + ' ' + dict.random_wish()
                        elif days_to_exam == 1:
                            ans = dict.exam_message['exam_tomorrow']
                        elif days_to_exam == 0:
                            ans = dict.exam_message['exam_today']
                        elif days_to_exam == -1:
                            ans = dict.exam_message['exam_in_past']
                        elif days_to_exam <-1:
                            db.set_subscribe(user_id, False)
                            ans = dict.exam_message['auto_unsubscribe']

                        write_notify_msg(user_id, ans)
                        last_send_time = dt.time_now_obj()
                bed.sleep(10)
        except:
            print('Notification module: Unknown exception')
            bed.sleep(10)