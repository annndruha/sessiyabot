#Sessiya-bot - Chat bot for students
#Маракулин Андрей @annndruha
#2019
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

from chat_module import chat_module
from notification_module import notification_module
from random import randint
from threading import Thread

# Setings VK_API
# Auth with community token
# Create a longpull variable
vk = vk_api.VkApi(token="ce15c65b20b72f10b0e456c7a8a20bc618f5c23f98076e10416a4820dac8c30bb256c9fa0169fc91f685f")
longpoll = VkLongPoll(vk)

def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message, "random_id": randint(1,4294967295)})

def longpool_chat():
    while True:
        try:
            for event in longpoll.listen():# Longpull loop
                if ((event.type == VkEventType.MESSAGE_NEW) and (event.to_me)):
                    answer = chat_module(event.text)# Start text analysis function
                    write_msg(answer)
        except:
            print("Longpull error")

#Thread_chat = Thread(target=longpool_chat)
Thread_notification = Thread(target=notification_module())

#Thread_chat.start()
Thread_notification.start()

#Thread_chat.join()
Thread_notification.join()