# Sessiya_bot: notification_module - Always run file for notify
# Маракулин Андрей @annndruha
# 2019
import time as bed
from vk_api import VkApi

import config
import engine
import dictionary as dict
from datebase_functions import change_flag

def write_notify_msg(user_id, message):
    vk = VkApi(token=config.notify_token)
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': engine.datetime_to_random_id()})

def notification_module():
    print(f'[{engine.timestamp()}] Notification module: Start')
    while True:
        try:
            last_send_time = -1
            while True:
                try:
                    users = open(config.users_file)
                    lines = users.read().splitlines()
                    users.close()
                except:
                    print(f'[{engine.timestamp()}] Notification module: File open error')

                if (last_send_time != engine.time_now_obj()):
                    last_send_time = -1

                    for line in lines:
                        user_line = line.split(' ')

                        user_id = user_line[0]
                        user_exam_date = engine.str_to_date(user_line[1])
                        user_notify_time = engine.str_to_time(user_line[2])
                        user_subscribe = user_line[3]

                        days_to_exam = (user_exam_date - engine.date_now_obj()).days

                        if ((user_subscribe == 'y') and (user_notify_time == engine.time_now_obj())):
                            if days_to_exam > 1:
                                ans = f'{dict.random_greeting()}\n{engine.sessiya_mesage(user_id)}\n{dict.random_wish()}'
                            elif days_to_exam == 1:
                                ans = dict.exam_message['exam_tomorrow']
                            elif days_to_exam == 0:
                                ans = dict.exam_message['exam_today']
                            elif days_to_exam == -1:
                                ans = dict.exam_message['exam_in_past']
                            elif days_to_exam < -1:
                                change_flag(user_id)
                                ans = dict.exam_message['auto_unsubscribe']
                                print(f'[{engine.timestamp()}] Notification module: {str(user_id)} - Auto unsubscribe')

                            write_notify_msg(user_id, ans)
                            print(f'[{engine.timestamp()}] Notification module: Sent a message to {str(user_id)}')
                            last_send_time = engine.time_now_obj()
                bed.sleep(10)
        except:
            print(f'[{engine.timestamp()}] Notification module: Unknown exception')
            bed.sleep(10)