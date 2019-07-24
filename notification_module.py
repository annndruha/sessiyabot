# Sessiya_bot: notification_module - Always run file for notify
# Маракулин Андрей @annndruha
# 2019
import time as bed

from vk_api import VkApi

import config
import dictionary as dict
import engine
import datebase_functions as dbf

def write_notify_msg(user_id, message):
    vk = VkApi(token=config.notify_token)
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': engine.datetime_to_random_id()})

def notification_loop():
    print('Notification module: Start')
    while True:
        try:
            last_send_time = -1
            while True:
                try:
                    lines = dbf.get_lines()
                except:
                    print('Notification module: File open error')

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
                                ans = dict.random_greeting() + '\n'+ dict.exam_message['time_until_exam'] +' '+ str(days_to_exam) + ' ' + dict.numerals_days(days_to_exam) + '\n'+ dict.random_wish()
                            elif days_to_exam == 1:
                                ans = dict.exam_message['exam_tomorrow']
                            elif days_to_exam == 0:
                                ans = dict.exam_message['exam_today']
                            elif days_to_exam == -1:
                                ans = dict.exam_message['exam_in_past']
                            elif days_to_exam < -1:
                                dbf.change_flag(user_id)
                                ans = dict.exam_message['auto_unsubscribe']
                                print(f'Notification module: {str(user_id)} - Auto unsubscribe')

                            write_notify_msg(user_id, ans)
                            print(f'Notification module: Sent a message to {str(user_id)}')
                            last_send_time = engine.time_now_obj()
                bed.sleep(10)
        except:
            print('Notification module: Unknown exception')
            bed.sleep(10)