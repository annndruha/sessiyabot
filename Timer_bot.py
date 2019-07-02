import vk_api
import random
import engine
import time as bed
import datetime
from pytz import timezone

token = "ce15c65b20b72f10b0e456c7a8a20bc618f5c23f98076e10416a4820dac8c30bb256c9fa0169fc91f685f"
vk = vk_api.VkApi(token=token)

def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message, "random_id": random.randint(1,4294967295)})


last_send_minute=-1
write_msg(478143147, "Таймер-бот запустился! "+engine.date_and_time_now())
print("Я запущен в  "+engine.date_and_time_now())
while True:
    print("Перезагрузка осуществлена в  "+engine.date_and_time_now())
    try:
        while True:
            lines = open('user_list.txt').read().splitlines() #Открытие списка рассылки какждые 20 секунд
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
        print("Ошибка произошла в "+engine.date_and_time_now())
        bed.sleep(3)


