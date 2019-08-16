# sessiyabot/core/chat_module
# - longpoll chat, text anaizer engine and keybord browser
# Маракулин Андрей @annndruha
# 2019
import time
import traceback
import json

import psycopg2
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id

from data import config
from data import dictionary as dict
from func import chat_functions as chat
from func import datetime_functions as dt
from core import keybords as kb

vk = vk_api.VkApi(token=config.access_token)# Auth with community token
longpoll = VkLongPoll(vk)# Create a longpull variable

def vk_user_get(user_id):
    return vk.method('users.get', {'user_ids': user_id})

def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': get_random_id()})

class User:
    def __init__(self, user_id, message, first_name, last_name):
        self.user_id=user_id
        self.message=message
        self.first_name=first_name
        self.last_name=last_name


def message_analyzer(user):
    try:
        request = (user.message).lower()
        l = len(request)
        if   (l <= 0):
            ans = dict.chat_ans[-1]
        elif (l > 299):
            ans = dict.chat_ans[-2]
        elif (l == 1):
            for keyword in dict.one_letter_word:
                if (request == keyword):
                    ans = dict.one_letter_word[keyword]
                else:
                    ans = dict.chat_ans[0]
        elif (l == 2):
            for keyword in dict.two_letter_word:
                if (request == keyword):
                    ans = dict.two_letter_word[keyword]
                else:
                    ans = dict.chat_ans[0]

        elif ((l > 2) and (l <= 299)):
            ans_exist = 0
            for keyword in dict.answer:
                if (request.find(keyword) >= 0):
                    ans = dict.answer[keyword]
                    ans_exist = 1
            for keyword in dict.functions:#Hello fn, open kb.main page
                if (request.find(keyword) >= 0):
                    k = dict.functions[keyword]
                    if k == 0:
                        ans = chf.chat_sessiya_mesage(user_id)
                    if k == 1:
                        ans = chf.chat_time(user_id, request, user_first_name, user_last_name)
                    if k == 2:
                        ans = chf.chat_date(user_id, request, user_first_name, user_last_name)
                    if k == 3:
                        ans = chf.chat_stop(user_id, request)
                    if k == 4:
                        ans = chf.chat_tz(user_id, request, user_first_name, user_last_name)
                    if k == 5:
                        ans = dict.random_wish()
                    ans_exist = 1
            if ((ans_exist == 0) and (request.find('?') >= 0)):
                ans = dict.random_answer()
            elif ans_exist == 0:
                ans = chf.chat_find_in_wiki(user_id, request)
        return ans

    except BaseException as err:
        traceback.print_tb(err.__traceback__)
        ans = dict.chat_ans[-3]
        return ans

def keyboard_browser(user, str_payload):
    try:
        payload = json.loads(str_payload)

        if payload[0] == 'command':
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
            print("--- %s seconds chat_time ---" % (time.time() -start_time))


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
        print(time.strftime("---[%Y-%m-%d %H:%M:%S] Database Error", time.localtime()))
        ans = dict.errors['not_available']
        write_msg(user.user_id, ans)
    except BaseException as err:
        print(time.strftime("---[%Y-%m-%d %H:%M:%S] Keyboard_browser error, way:", time.localtime()))
        traceback.print_tb(err.__traceback__)
        ans = dict.chat_ans[-4]
        write_msg(user.user_id, ans)


def longpull_loop():
    while True:
        try:
            kb.main_page(478143147, 'Привет!')
            for event in longpoll.listen():
                if (event.type == VkEventType.MESSAGE_NEW and event.to_me):
                    vk_user = vk_user_get(event.user_id)
                    first_name = (vk_user[0])['first_name']
                    last_name = (vk_user[0])['last_name']

                    user = User(event.user_id, event.text, first_name, last_name)
                    try:
                        print(event.payload)
                        keyboard_browser(user, event.payload)
                    except:
                        ans = chat.sessiya_mesage(user)
                        write_msg(user.user_id, ans)
                        k=0 #message_analyzer(user)

        except OSError as err:
            print(str(time.strftime("---[%Y-%m-%d %H:%M:%S] OSError in longpull_loop:", time.localtime())))
            #traceback.print_tb(err.__traceback__)
            print(err.args)
            time.sleep(10)
            print('-------------------------\tCHAT MODULE REBOOT\t------------------------')
        except BaseException as err:
            print(str(time.strftime("---[%Y-%m-%d %H:%M:%S] BaseException in chat_module, way:", time.localtime())))
            traceback.print_tb(err.__traceback__)
            print(err.args)
            time.sleep(2)
            print('-------------------------\tCHAT MODULE REBOOT\t------------------------')

print('start')
longpull_loop()