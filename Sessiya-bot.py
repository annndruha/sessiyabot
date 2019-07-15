import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

from threading import Thread
import random
import datetime
import time as bed
from pytz import timezone
import os #для смены директории


import dictionary as sheet
import engine
import datebase_functions


#Настройка VK_API
token = "ce15c65b20b72f10b0e456c7a8a20bc618f5c23f98076e10416a4820dac8c30bb256c9fa0169fc91f685f" #API-ключ созданный в сообществе
vk = vk_api.VkApi(token=token) # Авторизуемся как сообщество
longpoll = VkLongPoll(vk)# Работа с сообщениями

#Функция отправки сообщения
def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message, "random_id": random.randint(1,4294967295)})

def Chat_module():
    write_msg(478143147, "Chat module start at ["+engine.date_and_time_now()+"]")
    while True:
        try:
            try:
                for event in longpoll.listen():#Слушаем лонгпул
                    if ((event.type == VkEventType.MESSAGE_NEW) and (event.to_me)):
                        request = (event.text).lower()
                        ans_exist=0
                        l=len(request)
                        if   (l<=0):
                            ans_exist = -1
                        elif (l==1):
                             for keyword in sheet.one_letter_word:
                                if (request==keyword):
                                    ans = sheet.one_letter_word[keyword]
                                    ans_exist = 1
                        elif (l==2):
                            for keyword in sheet.two_letter_word:
                                if (request==keyword):
                                    ans = sheet.two_letter_word[keyword]
                                    ans_exist = 1
                        elif (l>299):
                            ans_exist = -2
                        elif ((l>2) and (l<=299)):
                            for keyword in sheet.answer:
                                if (request.find(keyword)>=0):
                                    ans = sheet.answer[keyword]
                                    ans_exist = 1
                            for keyword in sheet.functions:
                                if (request.find(keyword)>=0):
                                    k=sheet.functions[keyword]
                                    if k==0:
                                        ans = engine.sessiya_mesage(event.user_id)
                                    if k==1:
                                        ans = datebase_functions.start(event.user_id, request)
                                    if k==2:
                                        ans = datebase_functions.change(event.user_id, request)
                                    if k==3:
                                        ans = datebase_functions.stop(event.user_id, request)
                                    if k==4:
                                        ans = "Сейчас "+engine.time_now()+" по Москве"
                                    if k==5:
                                        ans = "Сегодня " + engine.date_now()
                                    ans_exist = 1
                            if ((ans_exist == 0) and (request.find('?')>=0)):
                                ans = sheet.random_answer[random.randint(1,8)]
                                ans_exist = 1

                        #Проверка кодов существования сообщения
                        if ((l==1 or l==2 or l==3) and ans_exist==0):
                            ans='&#128580;'
                        elif ans_exist==-2:
                            ans = 'Длина вашего сообщения слишком большая'
                        elif ans_exist==-1:
                            ans = 'Я распознаю только текст.\n¯\_(ツ)_/¯'
                        elif ans_exist==0:
                            ans = engine.find_in_wiki(request)
                            if (event.user_id==231000957):
                                ans = 'Макс, иди нахуй'
                            #if (event.user_id==478143147):
                                #photo = api.photos.saveMessagesPhoto(server = pfile['855724'], photo = pfile['{\"photo\":\"abfc538e88:w\",\"sizes\":[[\"s\",855724545,\"74ce7\",\"eZtYlny6IbU\",75,75],[\"m\",855724545,\"74ce8\",\"ZozlZLx5DfM\",130,130],[\"x\",855724545,\"74ce9\",\"YJdMJ_PlZyk\",604,604],[\"y\",855724545,\"74cea\",\"axRoLM-rFEA\",807,807],[\"z\",855724545,\"74ceb\",\"AGchdCMUDRs\",1080,1080],[\"w\",855724545,\"74cec\",\"QVFfJDZQsds\",1280,1280],[\"o\",855724545,\"74ced\",\"8oEXU5fHuO0\",130,130],[\"p\",855724545,\"74cee\",\"tmAPJVbr0ko\",200,200],[\"q\",855724545,\"74cef\",\"rmxBDTr1rJo\",320,320],[\"r\",855724545,\"74cf0\",\"teVf4NZBSHE\",510,510]],\"latitude\":0,\"longitude\":0,\"kid\":\"834e14e1690e37f5924b6d56b25389d8\"}'], hash = pfile['960e9d592a38680c9a14f5ecc0bd1ba7'])[0]
                                #ans = 'Андрей, иди нахуй'https://pp.userapi.com/c851032/v851032545/146f05/3Gfpl_iIhJ0.jpg
                                #write_msg(event.user_id, ans, attachment = 'doc%s_%s,photo%s_%s'%(doc['owner_id'], doc['id'], doc['owner_id'], photo['id'])
                        elif ans_exist==1:
                            ans = ans
                        write_msg(event.user_id, ans)
            except Exception as e:
                print("Тип:  "+str(e.__class__)+'\n')
        except:
            print("Найдена ошибка в Chat_module ["+engine.date_and_time_now()+"]\n")

def Notification_module():
    last_send_minute=-1
    os.chdir('.\Sessiya-bot-master')
    write_msg(478143147, "Notification module start at ["+engine.date_and_time_now()+"]")
    while True:
        try:
            while True:
                try:
                    user_list=open("user_list.txt","r")
                    lines = user_list.read().splitlines() #Открытие списка рассылки
                    user_list.close()
                except:
                    print("No file")
                today = datetime.date.today()#Получение текущего времени и даты
                time_is_now = (datetime.datetime.strftime(datetime.datetime.now(timezone('Europe/Moscow')), "%H:%M")).split(':')

                if (last_send_minute!=time_is_now[1]):
                    last_send_minute=-1
                    for line in lines:

                        user_line=line.split(' ')#Парсим информацию о пользователе

                        user_id=user_line[0]
                        user_sessiya_date=(user_line[1]).split('.')
                        user_notify_time=(user_line[2]).split(':')
                        user_subscribe=user_line[3]

                        h=user_notify_time[0]
                        m=user_notify_time[1]

                        sessiya_begin = datetime.date(int(user_sessiya_date[2]),int(user_sessiya_date[1]),int(user_sessiya_date[0]))
                        days_to_end = (sessiya_begin-today).days#Считаем сколько до сессии, чтобы проверить не прошла ли она

                        if (user_subscribe=='y'):
                            if ((h==time_is_now[0]) and (m==time_is_now[1])):
                                if days_to_end>1:
                                    ans = 'Доброго времени суток!\n'+engine.sessiya_mesage(user_id)+'\nПродуктивной вам подготовки! &#128214;'
                                elif days_to_end==1:
                                    ans = 'Уже завтра экзамен, я в вас верю и желаю самой продуктивной работы сегодня! &#10024;'
                                elif days_to_end==0:
                                    ans = 'Удачи сегодня на экзамене! Я верю в тебя и желаю всего самого наилучшего! &#127808;'
                                elif days_to_end<0:
                                    ans = 'Здравствуйте!\nЭкзамен прошёл, надеюсь вы хорошо его сдали. Чтобы поставить новую дату ближайшего экзамена воспользуйтесть командой:\n/change дд.мм.гггг\n\nЧтобы отписаться от уведомлений наберите мне:\n/stop'

                                write_msg(user_id, ans)
                                print('Я отправил сообщение '+user_id+' в '+ engine.date_and_time_now())
                                last_send_minute=m
                bed.sleep(10)
        except:
            print("Найдена ошибка в Notification_module ["+engine.date_and_time_now()+"]")
            bed.sleep(3)

thread1 = Thread(target=Chat_module)
thread2 = Thread(target=Notification_module)

thread1.start()
thread2.start()
thread1.join()
thread2.join()
