# sessiyabot/func/vk_functions
# - vk functions
# Marakulin Andrey @annndruha
# 2019
from vk_api import VkApi
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard
from vk_api.utils import get_random_id

from data import config

vk = VkApi(token=config.access_token)# Auth with community token
longpoll = VkLongPoll(vk)# Create a longpull variable
class User:
    def __init__(self, user_id, message, first_name, last_name):
        self.user_id = user_id
        self.message = message
        self.first_name = first_name
        self.last_name = last_name

def reconnect():
    global vk
    global longpoll
    vk = VkApi(token=config.access_token)
    longpoll = VkLongPoll(vk)

def user_get(user_id):
    return vk.method('users.get', {'user_ids': user_id})

def write_msg(user_id, message, attach=None):
    if attach is None:
        vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': get_random_id()})
    else:
        vk.method('messages.send', {'user_id': user_id, 'message': message, 'attachment':attach,'random_id': get_random_id()})

def send_keyboard(user_id, kb, message):
    vk.method('messages.send', {'user_id': user_id, 'keyboard': kb, 'message': message, 'random_id': get_random_id()})