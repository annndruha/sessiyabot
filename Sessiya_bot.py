# Sessiya-bot - Chat bot for students
# Маракулин Андрей @annndruha
# 2019
from random import randint

from vk_api import VkApi
from vk_api.longpoll import VkLongPoll, VkEventType
from threading import Thread

from config import chat_token
from chat_module import message_analyzer
from notification_module import notification_loop

print('BOT STARTING')
vk = VkApi(token=chat_token)# Auth with community token
longpoll = VkLongPoll(vk)# Create a longpull variable

def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': randint(1,4294967295)})

def longpull_loop():
    while True:
        print('Chat module: Start')
        try:
            for event in longpoll.listen():# Longpull loop
                if ((event.type == VkEventType.MESSAGE_NEW) and (event.to_me)):
                    ans = message_analyzer(event.user_id, event.text)# Start text analysis function
                    write_msg(event.user_id, ans)
        except:
            print('Longpull loop: Unknown exception')

Thread_notification = Thread(target=notification_loop)
Thread_chat = Thread(target=longpull_loop)

Thread_notification.start()
Thread_chat.start()

Thread_chat.join()
Thread_notification.join()