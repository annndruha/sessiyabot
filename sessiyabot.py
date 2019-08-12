# sessiyabot
# - Chat bot vk.com for students
# Маракулин Андрей @annndruha
# 2019
import time
import traceback

from threading import Thread

from core import chat_module
from core import notify_module

while True:
    try:
        Thread_chat = Thread(target=chat_module.longpull_loop)
        #Thread_notification = Thread(target=notify_module.notify_loop)

        Thread_chat.start()
        print('-------------------------\tCHAT MODULE START\t------------------------')
        #Thread_notification.start()
        #print('-------------------------\tNOTIFY MODULE START\t------------------------')

        print('=========================\tBOT START SUCCSESSFULLY\t========================')
        Thread_chat.join()
        #Thread_notification.join()
    except BaseException as err:
        print(str(time.strftime("---[%Y-%m-%d %H:%M:%S] BaseException in sessiyabot, way:", time.localtime())))
        traceback.print_tb(err.__traceback__)
        print(err.args)
        time.sleep(10)
        print('-------------------------\tBOT REBOOT\t------------------------')