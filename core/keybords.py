
import vk_api

from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id
from data import config

def main():

    vk_session = vk_api.VkApi(token=config.access_token)
    vk = vk_session.get_api()

    keyboard = VkKeyboard(one_time=True)

    keyboard.add_button('Настройки уведомлений', color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('Сменить дату экзамена', color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('Подбодри меня!', color=VkKeyboardColor.POSITIVE)

    vk.messages.send(
        peer_id=478143147,
        random_id=get_random_id(),
        keyboard=keyboard.get_keyboard(),
        message = 'Начинаем'
    )


if __name__ == '__main__':
    main()