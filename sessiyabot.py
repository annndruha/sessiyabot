# sessiyabot
# - Chat bot vk.com for students
# Marakulin Andrey @annndruha
# 2019
import time
import traceback

import psycopg2

from func import vkontakte_functions as vk
from core import keybords as kb
from core import analyzer

print(str(time.strftime("===[%Y-%m-%d %H:%M:%S] CHAT BOT START", time.localtime())))
while True:
    try:
        for event in vk.longpoll.listen():
            if (event.type == vk.VkEventType.MESSAGE_NEW and event.to_me):
                vk_user = vk.user_get(event.user_id)
                first_name = (vk_user[0])['first_name']
                last_name = (vk_user[0])['last_name']
                user = vk.User(event.user_id, event.text, first_name, last_name)

                try:
                    kb.keyboard_browser(user, event.payload)
                except AttributeError:
                    analyzer.message_analyzer(user)

    except psycopg2.Error as err:
        print(time.strftime("---[%Y-%m-%d %H:%M:%S] Database Error (longpull_loop), description:", time.localtime()))
        #traceback.print_tb(err.__traceback__)
        print(err.args[0])
        try:
            print(str(time.strftime("---[%Y-%m-%d %H:%M:%S] Try to recconnect database...", time.localtime())))
            db.reconnect()
            print(str(time.strftime("---[%Y-%m-%d %H:%M:%S] Database connected successful", time.localtime())))
            time.sleep(2)
        except:
            print(str(time.strftime("---[%Y-%m-%d %H:%M:%S] Recconnect database failed", time.localtime())))
            time.sleep(3)
        print(str(time.strftime("---[%Y-%m-%d %H:%M:%S] CHAT BOT RESTART", time.localtime())))
    except OSError as err:
        print(str(time.strftime("---[%Y-%m-%d %H:%M:%S] OSError (longpull_loop), description:", time.localtime())))
        #traceback.print_tb(err.__traceback__)
        print(err.args[0])
        try:
            print(str(time.strftime("---[%Y-%m-%d %H:%M:%S] Try to recconnect VK...", time.localtime())))
            vk_reconnect()
            print(str(time.strftime("---[%Y-%m-%d %H:%M:%S] VK connected successful", time.localtime())))
            time.sleep(2)
        except:
            print(str(time.strftime("---[%Y-%m-%d %H:%M:%S] Recconnect VK failed", time.localtime())))
            time.sleep(3)
        print(str(time.strftime("---[%Y-%m-%d %H:%M:%S] CHAT BOT RESTART", time.localtime())))
    except BaseException as err:
        print(str(time.strftime("---[%Y-%m-%d %H:%M:%S] BaseException (longpull_loop), description:", time.localtime())))
        traceback.print_tb(err.__traceback__)
        print(err.args[0])
        time.sleep(3)
        print(str(time.strftime("===[%Y-%m-%d %H:%M:%S] CHAT BOT RESTART", time.localtime())))