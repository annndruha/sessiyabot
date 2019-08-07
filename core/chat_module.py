# Sessiya_bot: chat_module - Text analysis engine
# Маракулин Андрей @annndruha
# 2019
from random import randint


import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id

from data import config
from data import dictionary as dict
from func import chat_functions as chf


#vk = VkApi(token=config.access_token)# Auth with community token
#longpoll = VkLongPoll(vk)# Create a longpull variable
vk_session = vk_api.VkApi(token=config.access_token)
vk = vk_session.get_api()

def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': randint(1,4294967295)})

def send_keybord(user_id):
    keyboard = VkKeyboard(one_time=True)

    keyboard.add_button('Белая кнопка', color=VkKeyboardColor.DEFAULT)
    keyboard.add_button('Зелёная кнопка', color=VkKeyboardColor.POSITIVE)

    keyboard.add_line()
    keyboard.add_vkpay_button(hash="action=transfer-to-group&group_id=74030368&aid=6222115")
    
    keyboard.add_line()
    keyboard.add_vkapps_button(app_id=6979558, 
                               owner_id=-181108510, 
                               label="Отправить клавиатуру",
                               hash="sendKeyboard")

     vk.method('messages.send', {'user_id': user_id, 'keyboard':keyboard.get_keyboard(),'message': 'Пример клавиатуры', 'random_id': randint(1,4294967295)})

send_keybord(478143147)

def vk_user_get(user_id):
    return vk.method('users.get', {'user_ids': user_id})

def message_analyzer(user_id,request, user_first_name, user_last_name):
    try:
        request = (request).lower()
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
            for keyword in dict.functions:
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
                    ans_exist = 1
            if ((ans_exist == 0) and (request.find('?') >= 0)):
                ans = dict.random_answer()
            elif ans_exist == 0:
                ans = chf.chat_find_in_wiki(user_id, request)
        return ans

    except:
        print('Chat module: Unknown exception')
        ans = dict.chat_ans[-3]
        return ans

def longpull_loop():
    while True:
        print('Chat module: Start')
        try:
            for event in longpoll.listen():# Longpull loop
                if ((event.type == VkEventType.MESSAGE_NEW) and (event.to_me)):

                    vk_user = vk_user_get(event.user_id)
                    if vk_user !=None:
                        user_first_name = (vk_user[0])['first_name']
                        user_last_name = (vk_user[0])['last_name']
                    else:
                        user_first_name = None
                        user_last_name = None
                    ans = message_analyzer(event.user_id, event.text, user_first_name, user_last_name)
                    write_msg(event.user_id, ans)
        except:
            print('Longpull loop: Unknown exception')