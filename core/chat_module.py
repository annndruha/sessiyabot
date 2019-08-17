# sessiyabot/core/chat_module
# - longpoll chat, text anaizer engine and keybord browser
# Маракулин Андрей @annndruha
# 2019
import time
import traceback
import json

import psycopg2
from vk_api import VkApi
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id

from data import config
from data import dictionary as dict
from data.class_user import User
from func import chat_functions as chat
from func import datetime_functions as dt
from core import keybords as kb

vk = VkApi(token=config.access_token)# Auth with community token
longpoll = VkLongPoll(vk)# Create a longpull variable

def vk_reconnect():
    global vk
    global longpoll
    vk = VkApi(token=config.access_token)
    longpoll = VkLongPoll(vk)

def vk_user_get(user_id):
    return vk.method('users.get', {'user_ids': user_id})

def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': get_random_id()})

def message_analyzer(user):
    try:
        user.message = (user.message).lower()
        l = len(user.message)
        open_kb = False
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
                        ans = chat.sessiya_mesage(user, 'chat')
                    if k == 1:
                        ans = chat.time(user)
                    if k == 2:
                        ans = chat.date(user)
                    if k == 3:
                        ans = chat.stop(user)
                    if k == 4:
                        ans = chat.tz(user)
                    if k == 5:
                        ans = dict.random_wish()
                    ans_exist = True

            if ((ans_exist == False) and (user.message.find('?') >= 0)):
                ans = dict.random_answer()
            elif ans_exist == False:
                ans = 'Я разучился гуглить'
                #ans = chat.find_in_wiki(user_id, user.message)
        if open_kb:
            kb.main_page(user.user_id, ans)
        else:
            write_msg(user.user_id, ans)
    except BaseException as err:
        print(str(time.strftime("---[%Y-%m-%d %H:%M:%S] Unknown Exception (message_analyzer)", time.localtime())))
        traceback.print_tb(err.__traceback__)
        print('\t'+str(err.args))
        ans = dict.errors['im_broken']
        write_msg(user.user_id, ans)

def keyboard_browser(user, str_payload):
    try:
        payload = json.loads(str_payload)
        if not isinstance(payload, list):
            ans = dict.hello['начать']
            kb.main_page(user.user_id, ans)
        elif payload[0] == 'command':
            start_time = time.time()
            if payload[1] == 'cancel':
                kb.main_page(user.user_id)
            elif payload[1] == 'set_time':
                user.message = payload[2]
                ans = chat.time(user)
                kb.main_page(user.user_id, ans)
            elif payload[1] == 'set_tz':
                user.message = payload[2]
                ans = chat.tz(user)
                kb.main_page(user.user_id, ans)
            elif payload[1] == 'set_date':
                user.message = dt.neareat_date(payload[2])
                ans = chat.date(user)
                kb.main_page(user.user_id, ans)
            elif payload[1] == 'set_subcribe':
                if payload[2] == 'start':
                    user.message = payload[2]
                    ans = chat.time(user)
                elif payload[2] == 'stop':
                    user.message = payload[2]
                    ans = chat.stop(user)
                kb.main_page(user.user_id, ans)
            print("--- %s seconds ---" % (time.time() - start_time))

        elif payload[0] == 'next_page':
            if payload[1] == 'notify_page':
                kb.notify_page(user.user_id)
            elif payload[1] == 'month_page':
                kb.month_page(user.user_id)
            elif payload[1] == 'hour_page1':
                kb.hour_page1(user.user_id)
            elif payload[1] == 'hour_page2':
                kb.hour_page2(user.user_id)
            elif payload[1] == 'tz_page':
                kb.tz_page(user.user_id)

        elif payload[0] == 'jump':
            if payload[1] == 'minute_page':
                kb.minute_page(user.user_id, payload[2])
            elif payload[1] == 'day_page1':
                kb.day_page1(user.user_id, payload[2])
            elif payload[1] == 'day_page2':
                kb.day_page2(user.user_id, payload[2])
            elif payload[1] == 'day_page3':
                kb.day_page3(user.user_id, payload[2])

    except psycopg2.Error as err:
        ans = dict.errors['not_available']
        write_msg(user.user_id, ans)
        print(time.strftime("---[%Y-%m-%d %H:%M:%S] Database Error (keyboard_browser), raise:", time.localtime()))
        raise err

    except OSError as err:
        print(str(time.strftime("---[%Y-%m-%d %H:%M:%S] OSError (keyboard_browser), description:", time.localtime())))
        raise err
    except BaseException as err:
        print(time.strftime("---[%Y-%m-%d %H:%M:%S] Unknown Exception (keyboard_browser)", time.localtime()))
        traceback.print_tb(err.__traceback__)
        print(str(err.args))
        ans = dict.errors['kb_error']
        write_msg(user.user_id, ans)


def longpull_loop():
    while True:
        try:
            for event in longpoll.listen():
                if (event.type == VkEventType.MESSAGE_NEW and event.to_me):
                    vk_user = vk_user_get(event.user_id)
                    first_name = (vk_user[0])['first_name']
                    last_name = (vk_user[0])['last_name']
                    user = User(event.user_id, event.text, first_name, last_name)

                    try:
                        keyboard_browser(user, event.payload)
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