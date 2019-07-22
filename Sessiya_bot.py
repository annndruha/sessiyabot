#Sessiya-bot - Chat bot for students
#Маракулин Андрей @annndruha
#2019

from vk_api import VkApi
from vk_api.longpoll import VkLongPoll, VkEventType
from threading import Thread
from random import randint

from config import chat_token
from engine import timestamp
from chat_module import chat_module
from notification_module import notification_module

print("["+timestamp()+"] Sessiya-bot: Build successful")

vk = VkApi(token=chat_token)# Auth with community token
longpoll = VkLongPoll(vk)# Create a longpull variable
print("["+timestamp()+"] Sessiya-bot: Vk connected")

def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message, "random_id": randint(1,4294967295)})

def longpull_loop():
    while True:
        print("["+timestamp()+"] Longpull loop: Start")
        try:
            for event in longpoll.listen():# Longpull loop
                if ((event.type == VkEventType.MESSAGE_NEW) and (event.to_me)):
                    ans = chat_module(event.user_id, event.text)# Start text analysis function
                    write_msg(event.user_id, ans)
        except:
            print("["+timestamp()+"] Longpull loop: Unknown exception")

Thread_notification = Thread(target=notification_module)
Thread_chat = Thread(target=longpull_loop)

Thread_notification.start()
Thread_chat.start()

Thread_chat.join()
Thread_notification.join()