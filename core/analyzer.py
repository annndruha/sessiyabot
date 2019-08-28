# sessiyabot/core/analyzer
# - text anaizer engine, runner and keybord browser
# Marakulin Andrey @annndruha
# 2019
import time
import traceback

import psycopg2

from data import ru_dictionary as dict
from func import vkontakte_functions as vk
from core import engine as eng
from core import keybords as kb

def message_analyzer(user):
    try:
        user.message = (user.message).lower()
        l = len(user.message)

        ans = None
        attach = None
        open_kb = False

        if   (l <= 0):
            ans = dict.errors['null_length']
        elif (l >= 300):
            ans = dict.errors['big_lenght']
        elif ((l == 1) or (l == 2)):
            for keyword in dict.small_message:
                if (user.message == keyword):
                    ans = dict.small_message[keyword]
            if ans is None:
                ans = dict.errors['hm']
        elif ((l > 2) and (l < 300)):
            for keyword in dict.answer:
                if (user.message.find(keyword) >= 0):
                    ans = dict.answer[keyword]
            for keyword in dict.hello:
                if (user.message.find(keyword) >= 0):
                    ans = dict.hello[keyword]
                    open_kb = True
            for keyword in dict.functions:
                if (user.message.find(keyword) >= 0):
                    k = dict.functions[keyword]
                    if k == 0:
                        ans = eng.sessiya_message(user)
                    if k == 1:
                        ans = eng.alter_time(user)
                    if k == 2:
                        ans = eng.alter_date(user)
                    if k == 3:
                        ans = eng.alter_stop(user)
                    if k == 4:
                        ans = eng.alter_tz(user)
                    if k == 5:
                        ans, attach = dict.cheer(user)
                    if k == 6:
                        ans, attach = dict.cheer(user, True)

            if ans == None and eng.validate_expression(user.message)==True:
                ans = eng.calculator(user.message)
            if ans == None:
                ans = eng.find_in_internet(user.message)
            if ans == None:
                if user.message.find('?') >= 0:
                    ans = dict.random_answer()

        if ans == None:
            ans = dict.random_not_found()
            #max idi nahui

        if open_kb:
            kb.main_page(user.user_id, ans)
        else:
            vk.write_msg(user.user_id, ans, attach)

    except psycopg2.Error:
        raise err
    except OSError as err:
        raise err
    except BaseException as err:
        ans = dict.errors['im_broken']
        vk.write_msg(user.user_id, ans)
        print(str(time.strftime("---[%Y-%m-%d %H:%M:%S] Unknown Exception (message_analyzer), description:", time.localtime())))
        traceback.print_tb(err.__traceback__)
        print(str(err.args))