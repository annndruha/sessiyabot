# Sessiya_bot: chat_fuction - analyze unusulal chat requestes_user
# Маракулин Андрей @annndruha
# 2019

import wikipedia

import config
import dictionary as dict
import engine
import datebase_functions as dbf

def start(user_id, message):# Start notify message from user
    try:
        if (len(message.split(' '))<2):
            ans = dict.db_ans['incorrect_time']
        elif (engine.validate_time(message.split(' ')[1]) == False):
            ans = dict.db_ans['incorrect_time']
        else:
            new_user_time = message.split(' ')[1]
            if dbf.check_user(user_id) == 'e':
                dbf.add_line(f'{str(user_id)} {config.default_exam_date} {new_user_time} y')
                ans = dict.db_ans['start_notify'] + ' ' + new_user_time + ' ' + dict.db_ans['msk']
            elif dbf.check_user(user_id) == 'n':
                dbf.change_time(user_id,new_user_time)
                dbf.change_flag(user_id)
                ans = dict.db_ans['start_notify'] + ' ' + new_user_time + ' ' + dict.db_ans['msk']
            elif dbf.check_user(user_id) == 'y':
                dbf.change_time(user_id, new_user_time)
                ans = dict.db_ans['change_time'] + ' ' + new_user_time + ' ' + dict.db_ans['msk']
    except:
        print('Chat functions: Start: Exception')
        ans = dict.db_ans['not_available']
    return ans

def change(user_id, message):# Change notify message from user
    try:
        if (len(message.split(' '))<2):
            ans = dict.db_ans['incorrect_date'] + ' ' + config.default_exam_date
        elif (engine.validate_date(message.split(' ')[1]) == False):
            ans = dict.db_ans['incorrect_date'] + ' ' + config.default_exam_date
        else:
            new_user_date=message.split(' ')[1]
            if dbf.check_user(user_id) == 'e':
                dbf.add_line(str(user_id) + ' ' + new_user_date + ' 00:00 n')
                ans = dict.db_ans['change_date'] + ' ' + new_user_date
            else:
                dbf.change_date(user_id,new_user_date)
                ans = dict.db_ans['change_date'] + ' ' + new_user_date
    except:
        print('Chat functions: Change: Exception')
        ans = dict.db_ans['not_available']
    return ans

def stop(user_id, message):# Stop notify message from user
    try:
        if dbf.check_user(user_id) == 'e':
            ans = dict.db_ans['no_sub']
        elif dbf.check_user(user_id) == 'n':
            ans = dict.db_ans['unfollow_yet']
        elif dbf.check_user(user_id) == 'y':
            change_flag(user_id)
            ans = dict.db_ans['unfollow']
    except:
        print('Chat functions:: Stop: Exception')
        ans = dict.db_ans['not_available']
    return ans

def sessiya_mesage(user_id):
    try:
        user_exam_date = config.default_exam_date
        today = engine.date_now_obj()
        try:
            lines = dbf.get_lines()
        except:
            print('Sessiya message: File open error')

        for line in lines:
            if (line.find(str(user_id)) >= 0):
                user_line = line.split(' ')
                user_exam_date = engine.str_to_date(user_line[1])
                days_to_exam = (user_exam_date - engine.date_now_obj()).days

        if days_to_exam > 1:
            ans = dict.exam_message['time_until_exam'] +' '+ str(days_to_exam) + ' ' + dict.numerals_days(days_to_exam)
        elif days_to_exam == 1:
            ans = dict.exam_message['exam_tomorrow']
        elif days_to_exam == 0:
            ans = dict.exam_message['exam_today']
        elif days_to_exam <0:
            ans = dict.exam_message['ask_exam_past']
    except:
        print('Chat functions:: Sessiya_mesage: Exception')
        ans = dict.db_ans['forget']
    return ans

def find_in_wiki(user_id, message):
    try:
        wikipedia.set_lang(config.wiki_language)
        n = 2
        max_n = 7
        exit = 0

        while ((n < max_n) and (exit == 0)):
            exit = 1
            ans = str(wikipedia.summary(message, sentences=n, auto_suggest=True))
            if ((ans.rfind('(')) > (ans.rfind(')'))):
                n = n + 1
                exit = 0
            if len(ans) < 100:
                n = n + 1
                exit = 0
        if ans.find('\n\n'):
            ans = ans[:(ans.find('\n\n'))]
    except:
        ans = dict.random_not_found()
    return ans