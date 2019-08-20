# sessiyabot/core/chat_module
# - longpoll chat, text anaizer engine and keybord browser
# Маракулин Андрей @annndruha
# 2019
import time
import traceback
import random

import psycopg2

from data import config
from data import dictionary as dict
from func import chat_functions as chat
from func import datetime_functions as dt
from func import vk_functions as vk
from core import keybords as kb

class User:
    def __init__(self, user_id, message, first_name, last_name):
        self.user_id = user_id
        self.message = message
        self.first_name = first_name
        self.last_name = last_name

def message_analyzer(user):
    try:
        user.message = (user.message).lower()
        l = len(user.message)
        open_kb = False
        already_send = False
        if   (l <= 0):
            ans = dict.errors['null_length']
        elif (l >= 300):
            ans = dict.errors['big_lenght']

        elif ((l == 1) or (l == 2)):
            for keyword in dict.small_message:
                if (user.message == keyword):
                    ans = dict.small_message[keyword]
                else:
                    ans = dict.errors['hm']
        elif ((l > 2) and (l < 300)):
            ans_exist = False
            for keyword in dict.answer:
                if (user.message.find(keyword) >= 0):
                    ans = dict.answer[keyword]
                    ans_exist = True
            for keyword in dict.hello:
                if (user.message.find(keyword) >= 0):
                    ans = dict.hello[keyword]
                    ans_exist = True
                    open_kb = True
            for keyword in dict.functions:
                if (user.message.find(keyword) >= 0):
                    k = dict.functions[keyword]
                    if k == 0:
                        ans = chat.sessiya_mesage(user)
                    if k == 1:
                        ans = chat.time(user)
                    if k == 2:
                        ans = chat.date(user)
                    if k == 3:
                        ans = chat.stop(user)
                    if k == 4:
                        ans = chat.tz(user)
                    if k == 5:
                        chat.cheer(user)
                        already_send = True
                    ans_exist = True

            if ((ans_exist == False) and (user.message.find('?') >= 0)):
                ans = dict.random_answer()
            elif ans_exist == False:
                ans = random_not_found()
                #ans = chat.find_in_wiki(user_id, user.message)
        if open_kb:
            kb.main_page(user.user_id, ans)
        elif already_send is False:
            vk.write_msg(user.user_id, ans)
    except BaseException as err:
        print(str(time.strftime("---[%Y-%m-%d %H:%M:%S] Unknown Exception (message_analyzer)", time.localtime())))
        traceback.print_tb(err.__traceback__)
        print('\t'+str(err.args))
        ans = dict.errors['im_broken']
        vk.write_msg(user.user_id, ans)


def longpull_loop():
    while True:
        try:
            for event in longpoll.listen():
                if (event.type == vk.VkEventType.MESSAGE_NEW and event.to_me):
                    vk_user = vk.user_get(event.user_id)
                    first_name = (vk_user[0])['first_name']
                    last_name = (vk_user[0])['last_name']
                    user = User(event.user_id, event.text, first_name, last_name)

                    try:
                        kb.keyboard_browser(user, event.payload)
                    except AttributeError:
                        message_analyzer(user)

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
            print(str(time.strftime("---[%Y-%m-%d %H:%M:%S] CHAT MODULE RESTART", time.localtime())))
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
            print(str(time.strftime("---[%Y-%m-%d %H:%M:%S] CHAT MODULE RESTART", time.localtime())))
        except BaseException as err:
            print(str(time.strftime("---[%Y-%m-%d %H:%M:%S] BaseException (longpull_loop), description:", time.localtime())))
            traceback.print_tb(err.__traceback__)
            print(err.args[0])
            time.sleep(3)
            print(str(time.strftime("---[%Y-%m-%d %H:%M:%S] CHAT MODULE RESTART", time.localtime())))