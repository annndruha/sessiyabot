# Sessiya-bot - Chat bot for students
# Маракулин Андрей @annndruha
# 2019
from random import randint

from vk_api import VkApi
from vk_api.longpoll import VkLongPoll, VkEventType
from threading import Thread

from data import config
from core import chat_module
from core import notify_module

print('BOT STARTING')
vk = VkApi(token=config.chat_token)# Auth with community token
longpoll = VkLongPoll(vk)# Create a longpull variable
print('Vk_connected')

def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': randint(1,4294967295)})

def longpull_loop():
    while True:
        print('Chat module: Start')
        try:
            for event in longpoll.listen():# Longpull loop
                if ((event.type == VkEventType.MESSAGE_NEW) and (event.to_me)):
                    ans = chat_module.message_analyzer(event.user_id, event.text)# Start text analysis function
                    write_msg(event.user_id, ans)
        except:
            print('Longpull loop: Unknown exception')

Thread_chat = Thread(target=longpull_loop)
Thread_notification = Thread(target=notification_module.notification_loop)

Thread_chat.start()
Thread_notification.start()

Thread_chat.join()
Thread_notification.join()