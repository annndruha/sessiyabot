import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import random
import dictionary as sheet
import engine
import datebase_functions




#Настройка VK_API
token = "ce15c65b20b72f10b0e456c7a8a20bc618f5c23f98076e10416a4820dac8c30bb256c9fa0169fc91f685f" #API-ключ созданный в сообществе
#k = vk_api.VkApi(token=token).method('users.get', {'user_id': 231000957, 'fields':'timezone',})
#print(k)

vk = vk_api.VkApi(token=token) # Авторизуемся как сообщество
longpoll = VkLongPoll(vk)# Работа с сообщениями

def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message, "random_id": random.randint(1,4294967295)})

#----------------------------------------------------------Начало основного кода
write_msg(478143147, "Основной бот запустился "+engine.date_and_time_now())
while True:
    print("Перезапуск произведён:  "+engine.date_and_time_now())
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
        print("Найдена ошибка. \n")
