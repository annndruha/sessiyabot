import time as bed
import engine
import config
from Sessiya_bot import write_msg
from dictionary import notify_message
from dictionary import random_greeting
from dictionary import random_wish
from datebase_functions import change_flag

def notification_module():
    print("[" + engine.datetime_now() + "] Notification module: Start")
    while True:
        try:
            last_send_time = -1
            while True:
                try:
                    users = open(config.users_filename)
                    lines = users.read().splitlines()
                    users.close()
                except:
                    print("[{}] Notification module: File open error".format(engine.datetime_now()))

                if (last_send_time != engine.time_now()):
                    last_send_time = -1

                    for line in lines:
                        user_line = line.split(' ')

                        user_id = user_line[0]
                        user_exam_date = engine.str_to_date(user_line[1])
                        user_notify_time = engine.str_to_time(user_line[2])
                        user_subscribe = user_line[3]

                        days_to_exam = (user_exam_date - engine.date_now()).days

                        if ((user_subscribe == 'y') and (user_notify_time == engine.time_now())):
                            if days_to_exam > 1:
                                ans = '{}\n{}\n{} &#128214;'.format(random_greeting(), engine.sessiya_mesage(user_id), random_wish())
                            elif days_to_exam == 1:
                                ans = notify_message['exam_tomorrow']
                            elif days_to_exam == 0:
                                ans = notify_message['exam_today']
                            elif days_to_exam == -1:
                                ans = notify_message['exam_in_past']
                            elif days_to_exam <-1:
                                change_flag(user_id)
                                ans = notify_message['auto_unsubscribe']
                                print("[{}] Notification module: {} - Auto unsubscribe".format(engine.datetime_now(), str(user_id)))

                            write_msg(user_id, ans)
                            print("[{}] Notification module: Sent a message to {}".format(engine.datetime_now(), str(user_id)))
                            last_send_time = engine.time_now()
                bed.sleep(10)
        except:
            print("[{}] Notification module: Unknown exception".format(engine.datetime_now()))
            bed.sleep(5)