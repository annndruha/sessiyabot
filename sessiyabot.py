# sessiyabot
# - Chat bot vk.com for students
# Маракулин Андрей @annndruha
# 2019
from threading import Thread

from core import chat_module
from core import notify_module

Thread_chat = Thread(target=chat_module.longpull_loop)
Thread_notification = Thread(target=notify_module.notify_loop)

Thread_chat.start()
Thread_notification.start()
print('BOT START SUCCSESSFULLY')

Thread_chat.join()
Thread_notification.join()