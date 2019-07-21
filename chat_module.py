import datebase_functions as dbf
import dictionary as dict

def chat_module(request):
    print("Chat module start at ["+dbf.date_and_time_now()+"]")
    try:
        request = (request).lower()
        ans_exist=0
        l=len(request)
        if   (l<=0):
            ans_exist = -1
        elif (l==1):
            for keyword in dict.one_letter_word:
                if (request==keyword):
                    ans = dict.one_letter_word[keyword]
                    ans_exist = 1
        elif (l==2):
            for keyword in dict.two_letter_word:
                if (request==keyword):
                    ans = dict.two_letter_word[keyword]
                    ans_exist = 1
        elif (l>299):
            ans_exist = -2
        elif ((l>2) and (l<=299)):
            for keyword in dict.answer:
                if (request.find(keyword)>=0):
                    ans = dict.answer[keyword]
                    ans_exist = 1
            for keyword in dict.functions:
                if (request.find(keyword)>=0):
                    k=dict.functions[keyword]
                    if k==0:
                        ans = dbf.sessiya_mesage(event.user_id)
                    if k==1:
                        ans = dbf.start(event.user_id, request)
                    if k==2:
                        ans = dbf.change(event.user_id, request)
                    if k==3:
                        ans = dbf.stop(event.user_id, request)
                    if k==4:
                        ans = "Сейчас "+dbf.time_now()+" по Москве"
                    if k==5:
                        ans = "Сегодня " + dbf.date_now()
                    ans_exist = 1
            if ((ans_exist == 0) and (request.find('?')>=0)):
                ans = dict.random_answer[random.randint(1,8)]
                ans_exist = 1

        #Проверка кодов существования сообщения
        if ((l==1 or l==2 or l==3) and ans_exist==0):
            ans='&#128580;'
        elif ans_exist==-2:
            ans = 'Длина вашего сообщения слишком большая'
        elif ans_exist==-1:
            ans = 'Я распознаю только текст.\n¯\_(ツ)_/¯'
        elif ans_exist==0:
            ans = dbf.find_in_wiki(request)
        elif ans_exist==1:
            ans = ans
        return ans
    except:
        print("Найдена ошибка в Chat_module. ["+dbf.date_and_time_now()+"]\n")
        ans = 'Во мне что-то сломалось...'
        return ans