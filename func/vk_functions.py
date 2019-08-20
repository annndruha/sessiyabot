from vk_api import VkApi
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard
from vk_api.utils import get_random_id


vk = VkApi(token=config.access_token)# Auth with community token
longpoll = VkLongPoll(vk)# Create a longpull variable

def reconnect():
    global vk
    global longpoll
    vk = VkApi(token=config.access_token)
    longpoll = VkLongPoll(vk)

def user_get(user_id):
    return vk.method('users.get', {'user_ids': user_id})

def write_msg(user_id, message, attach = None):
    if attach is None:
        vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': get_random_id()})
    else:
        vk.method('messages.send', {'user_id': user_id, 'message': message, 'attachment':attach,'random_id': get_random_id()})

def send_keyboard(user_id, kb, message):
    vk.method('messages.send', {'user_id': user_id, 'keyboard': kb, 'message': message, 'random_id': get_random_id()})