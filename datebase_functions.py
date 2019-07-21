# Functions for work with usres datebase
# and addictioanal functions
#Маракулин Андрей @annndruha
#2019

from datetime import datetime
from datetime import date
from datetime import time
from pytz import timezone
import random
import wikipedia
import dictionary
wikipedia.set_lang("RU")

default_exam_date = '04.01.2020'
users_file = 'users.txt'

#Функции для работы с базой
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

def validate_user(user_id):
    f = open(users_file)
    lines = f.readlines()
    for line in lines:
        if (line.find(str(user_id)) >= 0):
            user_line = line.split(' ')
            if user_line[3].find('y') >= 0:
               f.close()
               return 'y'
            if user_line[3].find('n') >= 0:
                f.close()
                return 'n'
    f.close()
    return 'e'

def add_line(user_id, new_line):
    f = open(users_file, 'a')
    f.write(new_line+'\n')
    f.close()

def change_date(user_id, date):
    with open(users_file) as f:
        lines = f.read().splitlines()
        for line in lines:
            if (line.find(str(user_id)) >= 0):
                user_line = line.split(' ')
                user_line[1] = date
                lines.remove(line)
        lines.append(' '.join(user_line))
    with open(users_file, 'w') as f:
        f.writelines(lines)

def change_time(user_id, my_time):
    f = open(users_file, 'r+')
    lines = f.readlines()
    for line in lines:
        if (line.find(str(user_id)) >= 0):
            user_line = line.split(' ')
            user_line[2] = my_time
            lines.remove(line)
    lines.append(' '.join(user_line))
    f.truncate()
    f.writelines(lines)
    f.close()

def change_flag(user_id):
    f = open(users_file)
    lines = f.read().splitlines()
    f.close()
    for line in lines:
        if (line.find(str(user_id)) >= 0):
            user_line = line.split(' ')
            if (user_line[3] == "n"):
                user_line[3] = "y"
            else:
                user_line[3] = "n"
            lines.remove(line)
    lines.append(' '.join(line_temp))
    f = open(users_file,'w')
    f.write('\n'.join(lines))
    f.close()

def start(user_id, message):
    try:
        new_user_time = (message.split(' '))[1]
        if (validate_time(new_user_time) == False):
            ans = "Некорректный формат времени для ежедневных напоминаний, правильный пример:\n/start 07:30"
        else:
            if validate_user(user_id) == 'e':
                s = str(user_id) + ' ' + default_exam_date + ' ' + new_user_time + ' y'
                add_line(user_id, s)
                ans = "Вы будете получать напоминания о сессии ежедневно в " + new_user_time + " мск"
            elif validate_user(user_id) == 'n':
                change_time(user_id,new_user_time)
                change_flag(user_id)
                ans = "Вы будете получать напоминания о сессии ежедневно в " + new_user_time + " мск"
            elif validate_user(user_id) == 'y':
                change_time(user_id, new_user_time)
                ans = "Время напоминаний изменено на: " + new_user_time + " мск"
    except:
        ans = 'К сожалению, действие временно недоступно'
    return ans

def change(user_id, message):
    try:
        new_user_date = (message.split(' '))[1]
        if (validate_date(new_user_date) == False):
            ans = "Некорректный формат даты, правильный пример:\n/change " + default_exam_date
        else:
            if validate_user(user_id) == 'e':
                s = str(user_id) + ' ' + new_user_date + ' ' + '00:00' + ' n'
                add_line(user_id, s)
                ans = "Дата ближайшего экзамена изменена на: " + new_user_date
            else:
                change_date(user_id,new_user_date)
                ans = "Дата ближайшего экзамена изменена на: " + new_user_date
    except:
        ans = 'К сожалению, действие временно недоступно'
    return ans

def stop(user_id, message):
    try:
        if validate_user(user_id) == 'e':
            ans = "Вы ещё не подписались на напоминания, чтобы от них отписываться :)"
        elif validate_user(user_id) == 'n':
            ans = "Вы уже отписались от напоминаний, чтобы снова подписаться воспользуйтесь командой: /start чч:мм"
        elif validate_user(user_id) == 'y':
            change_flag(user_id)
            ans = "Я больше не буду присылать вам напоминания о сессии. Надеюсь у вас всё получится и без меня!"
    except:
        ans = 'К сожалению, действие временно недоступно'
    return ans

#Остальные вспомонательные функции
def date_and_time_now():
    return datetime.strftime(datetime.now(timezone('Europe/Moscow')), "%d.%m.%Y %H:%M:%S")

def date_now():
    return datetime.strftime(datetime.now(timezone('Europe/Moscow')), "%d.%m.%Y")

def time_now():
    return datetime.strftime(datetime.now(timezone('Europe/Moscow')), "%H:%M")

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
        print('Не удалось открыть файл '+date_and_time_now())
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

change_date(478143147, '02.08.2019')