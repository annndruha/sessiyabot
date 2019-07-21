from datetime import datetime
from datetime import date
from datetime import time
from pytz import timezone

import random
import wikipedia
import dictionary
wikipedia.set_lang("RU")

def datetime_now():
    return datetime.strftime(datetime.now(timezone('Europe/Moscow')), "%d.%m.%Y %H:%M:%S")

def date_now():
    return datetime.strftime(datetime.now(timezone('Europe/Moscow')), "%d.%m.%Y")

def time_now():
    return datetime.strftime(datetime.now(timezone('Europe/Moscow')), "%H:%M")

def datetime_to_str(datetime_object):
    return datetime.strftime(datetime_object, "%d.%m.%Y %H:%M:%S")

def date_to_str(datetime_object):
    return datetime.strftime(datetime_object, "%d.%m.%Y")

def time_to_str(datetime_object):
    return datetime.strftime(datetime_object, "%H:%M")

def str_to_datetime(string):
    return datetime.strptime(string, "%d.%m.%Y %H:%M:%S")

def str_to_date(string):
    return datetime.strptime(string, "%d.%m.%Y")

def str_to_time(string):
    return datetime.strptime(string, "%H:%M")

def validate_date(date_text):
    try:
        if date_text != datetime.strptime(date_text, "%d.%m.%Y").strftime('%d.%m.%Y'):
            raise ValueError
        return True
    except ValueError:
        return False

def validate_time(time_text):
    try:
        if time_text != datetime.strptime(time_text, "%H:%M").strftime('%H:%M'):
            raise ValueError
        return True
    except ValueError:
        return False


def numerals_days(n):
    if ((10<n) and (n<20)):
        return 'дней'
    else:
        n = n%10
        if ((n==0) or (n>=5)):
            return 'дней'
        elif n==1:
            return 'день'
        elif ((n>1) and (n<5)):
            return 'дня'

def sessiya_mesage(user_id):
    first_exam = default_exam_date.split('.')
    today = date_now().split('.')

    try:
        f = open('users.txt')
    except:
        print('Не удалось открыть файл '+dateime_now())
    else:
        for line in f:
            if (line.find(str(user_id))>=0):
                first_exam = line.split(' ')[1]
                first_exam = first_exam.split('.')
        f.close()

    first_exam = date(int(first_exam[2]),int(first_exam[1]),int(first_exam[0]))
    today =  date(int(today[2]),int(today[1]),int(today[0]))
    days_to_end = (first_exam-today).days

    if days_to_end<=-30:
        return 'Сессия уже прошла, надеюсь ты хорошо её сдал!'
    elif days_to_end<=0:
        return 'Сессия уже идёт! Ты молодец, я в тебя верю и желаю успеха на экзаменах! &#10084;'
    else:
        return 'До ближайшего экзамена: '+ str(days_to_end) +' '+ numerals_days(days_to_end)# +'\nУже прошло: '+str(days_from_begin*100//(days_from_begin+days_to_end))+'% семестра'


def find_in_wiki(wiki_request):
    try:
        n=2#По умлочанию возвращаем два предложения
        exit = 0

        while ((n<5) and (exit==0)):
            exit = 1
            ans = str(wikipedia.summary(wiki_request, sentences=n, auto_suggest=True))
            if ((ans.rfind('('))>(ans.rfind(')'))):#Ищем конец предложения не между скобками
                n=n+1
                exit = 0
            if len(ans)<100:
                n=n+1
                exit = 0
        if ans.find('=='):
            ans = ans[:(ans.find('==')-1)]
    except wikipedia.exceptions.DisambiguationError:
        ans = dictionary.random_not_found[9]
    except:
        ans = dictionary.random_not_found[random.randint(1,8)]
    return ans
