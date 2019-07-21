import time as bed
import engine
import config

from dictionary import exam_message
from dictionary import random_greeting
from dictionary import random_wish
from datebase_functions import change_flag

import vk_api
vk = vk_api.VkApi(token="ce15c65b20b72f10b0e456c7a8a20bc618f5c23f98076e10416a4820dac8c30bb256c9fa0169fc91f685f")

def write_notify_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message, "random_id": engine.datetime_to_random_id()})

def notification_module():
    print("[{}] Notification module: Start".format(engine.timestamp()))
    while True:
        try:
            last_send_time = -1
            while True:
                try:
                    users = open(config.users_filename)
                    lines = users.read().splitlines()
                    users.close()
                except:
                    print("[{}] Notification module: File open error".format(engine.timestamp()))

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
                                ans = '{}\n{}\n{}'.format(random_greeting(), engine.sessiya_mesage(user_id), random_wish())
                            elif days_to_exam == 1:
                                ans = exam_message['exam_tomorrow']
                            elif days_to_exam == 0:
                                ans = exam_message['exam_today']
                            elif days_to_exam == -1:
                                ans = exam_message['exam_in_past']
                            elif days_to_exam <-1:
                                change_flag(user_id)
                                ans = exam_message['auto_unsubscribe']
                                print("[{}] Notification module: {} - Auto unsubscribe".format(engine.timestamp(), str(user_id)))

                            write_notify_msg(user_id, ans)
                            print("[{}] Notification module: Sent a message to {}".format(engine.timestamp(), str(user_id)))
                            last_send_time = engine.time_now_obj()
                bed.sleep(10)
        except:
            print("[{}] Notification module: Unknown exception".format(engine.timestamp()))
            bed.sleep(10)