# Sessiya_bot: keybords - list of keybords messages
# Маракулин Андрей @annndruha
# 2019

import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id

from data import config
from func import datebase_functions as dbf

vk_session = vk_api.VkApi(token=config.access_token)
vk = vk_session.get_api()

def main_page(user_id, message):
    keyboard = VkKeyboard(one_time=False)

    keyboard.add_button('Настройки уведомлений', color='primary', payload = {"next_page":"notify_page"})
    keyboard.add_line()
    keyboard.add_button('Сменить дату экзамена', color='primary', payload = {"next_page":"month_page"})
    keyboard.add_line()
    keyboard.add_button('Подбодри меня!', color=VkKeyboardColor.POSITIVE)

    print(keyboard.get_keyboard())

    vk.messages.send(
        peer_id=user_id,
        random_id=get_random_id(),
        keyboard=keyboard.get_keyboard(),
        message = message)

def notify_page(user_id):
    keyboard = VkKeyboard(one_time=False)

    if (dbf.get_user_exist(user_id)==False):
        keyboard.add_button('Настроить уведомления', color=VkKeyboardColor.POSITIVE, payload = {"next_page":"hour_page1"})
    elif (dbf.get_user_subscribe(user_id)==False):
        keyboard.add_button('Включить уведомления', color=VkKeyboardColor.POSITIVE, payload = {"notify_page":"start"})
        keyboard.add_line()
        keyboard.add_button('Изменить время уведомлений', color='primary', payload = {"next_page":"hour_page1"})
    else:
        keyboard.add_button('Выключить уведомления', color=VkKeyboardColor.NEGATIVE, payload = {"notify_page":"stop"})
        keyboard.add_line()
        keyboard.add_button('Изменить время уведомлений', color='primary', payload = {"next_page":"hour_page1"})
    keyboard.add_line()
    keyboard.add_button('Изменить часовой пояс', color='primary', payload = {"next_page":"tz_page"})
    keyboard.add_line()
    keyboard.add_button('Отмена', color='default', payload = {"cancel":"notify_page"})

    vk.messages.send(
        peer_id=user_id,
        random_id=get_random_id(),
        keyboard=keyboard.get_keyboard(),
        message = 'Настройки уведомлений:')

def hour_page1(user_id):
    keyboard = VkKeyboard(one_time=False)

    keyboard.add_button('00:', color='primary', payload = {"hour_page":"00"})
    keyboard.add_button('01:', color='primary', payload = {"hour_page":"01"})
    keyboard.add_button('02:', color='primary', payload = {"hour_page":"02"})
    keyboard.add_button('03:', color='primary', payload = {"hour_page":"03"})
    keyboard.add_line()
    keyboard.add_button('04:', color='primary', payload = {"hour_page":"04"})
    keyboard.add_button('05:', color='primary', payload = {"hour_page":"05"})
    keyboard.add_button('06:', color='primary', payload = {"hour_page":"06"})
    keyboard.add_button('07:', color='primary', payload = {"hour_page":"07"})
    keyboard.add_line()
    keyboard.add_button('08:', color='primary', payload = {"hour_page":"08"})
    keyboard.add_button('09:', color='primary', payload = {"hour_page":"09"})
    keyboard.add_button('10:', color='primary', payload = {"hour_page":"10"})
    keyboard.add_button('11:', color='primary', payload = {"hour_page":"11"})
    keyboard.add_line()
    keyboard.add_button('Отменить', color='default', payload = {"cancel":"hour_page"})
    keyboard.add_button('Далее >>', color='default', payload = {"next_page":"hour_page2"})

    vk.messages.send(
        peer_id=user_id,
        random_id=get_random_id(),
        keyboard=keyboard.get_keyboard(),
        message = 'Выберите новое время:')

def hour_page2(user_id):
    keyboard = VkKeyboard(one_time=False)

    keyboard.add_button('12:', color='primary', payload = {"hour_page2":"12"})
    keyboard.add_button('13:', color='primary', payload = {"hour_page2":"13"})
    keyboard.add_button('14:', color='primary', payload = {"hour_page2":"14"})
    keyboard.add_button('15:', color='primary', payload = {"hour_page2":"15"})
    keyboard.add_line()
    keyboard.add_button('16:', color='primary', payload = {"hour_page2":"16"})
    keyboard.add_button('17:', color='primary', payload = {"hour_page2":"17"})
    keyboard.add_button('18:', color='primary', payload = {"hour_page2":"18"})
    keyboard.add_button('19:', color='primary', payload = {"hour_page2":"19"})
    keyboard.add_line()
    keyboard.add_button('20:', color='primary', payload = {"hour_page2":"20"})
    keyboard.add_button('21:', color='primary', payload = {"hour_page2":"21"})
    keyboard.add_button('22:', color='primary', payload = {"hour_page2":"22"})
    keyboard.add_button('23:', color='primary', payload = {"hour_page2":"23"})
    keyboard.add_line()
    keyboard.add_button('<< Назад', color='default', payload = {"next_page":"hour_page2"})
    keyboard.add_button('Отменить', color='default', payload = {"cancel":"hour_page2"})

    vk.messages.send(
        peer_id=user_id,
        random_id=get_random_id(),
        keyboard=keyboard.get_keyboard(),
        message = 'Выберите новое время:')

def minute_page(user_id, hour):
    keyboard = VkKeyboard(one_time=False)

    keyboard.add_button(hour+':00', color='primary', payload = {"minute_page":"time "+hour+":00"})
    keyboard.add_button(hour+':05', color='primary', payload = {"minute_page":"time "+hour+":05"})
    keyboard.add_button(hour+':10', color='primary', payload = {"minute_page":"time "+hour+":10"})
    keyboard.add_button(hour+':15', color='primary', payload = {"minute_page":"time "+hour+":15"})
    keyboard.add_line()
    keyboard.add_button(hour+':20', color='primary', payload = {"minute_page":"time "+hour+":20"})
    keyboard.add_button(hour+':25', color='primary', payload = {"minute_page":"time "+hour+":25"})
    keyboard.add_button(hour+':30', color='primary', payload = {"minute_page":"time "+hour+":30"})
    keyboard.add_button(hour+':35', color='primary', payload = {"minute_page":"time "+hour+":35"})
    keyboard.add_line()
    keyboard.add_button(hour+':40', color='primary', payload = {"minute_page":"time "+hour+":40"})
    keyboard.add_button(hour+':45', color='primary', payload = {"minute_page":"time "+hour+":45"})
    keyboard.add_button(hour+':50', color='primary', payload = {"minute_page":"time "+hour+":50"})
    keyboard.add_button(hour+':55', color='primary', payload = {"minute_page":"time "+hour+":55"})
    keyboard.add_line()
    keyboard.add_button('Отменить', color='default', payload = {"cancel":"minute_page"})

    vk.messages.send(
        peer_id=user_id,
        random_id=get_random_id(),
        keyboard=keyboard.get_keyboard(),
        message = 'Завершите выбор времени:')

def tz_page(user_id):
    keyboard = VkKeyboard(one_time=False)

    keyboard.add_button('МСК', color='primary', payload = {"tz_page":"tz 0"})
    keyboard.add_button('МСК-1', color='primary', payload = {"tz_page":"tz -1"})
    keyboard.add_button('МСК+1', color='primary', payload = {"tz_page":"tz 1"})
    keyboard.add_button('МСК+2', color='primary', payload = {"tz_page":"tz 2"})
    keyboard.add_line()
    keyboard.add_button('МСК+3', color='primary', payload = {"tz_page":"tz 3"})
    keyboard.add_button('МСК+4', color='primary', payload = {"tz_page":"tz 4"})
    keyboard.add_button('МСК+5', color='primary', payload = {"tz_page":"tz 5"})
    keyboard.add_button('МСК+6', color='primary', payload = {"tz_page":"tz 6"})
    keyboard.add_line()
    keyboard.add_button('МСК+7', color='primary', payload = {"tz_page":"tz 7"})
    keyboard.add_button('МСК+8', color='primary', payload = {"tz_page":"tz 8"})
    keyboard.add_button('МСК+9', color='primary', payload = {"tz_page":"tz 9"})
    keyboard.add_button('МСК+10', color='primary', payload = {"tz_page":"tz 10"})
    keyboard.add_line()
    keyboard.add_button('Отменить', color='default', payload = {"cancel":"tz_page"})

    vk.messages.send(
        peer_id=user_id,
        random_id=get_random_id(),
        keyboard=keyboard.get_keyboard(),
        message = 'Установите новый часовой пояс:')

def month_page(user_id):
    keyboard = VkKeyboard(one_time=False)

    keyboard.add_button('Декабрь', color='primary', payload = {"month_page":"12"})
    keyboard.add_button('Январь', color='primary', payload = {"month_page":"01"})
    keyboard.add_button('Февраль', color='primary', payload = {"month_page":"02"})
    keyboard.add_line()
    keyboard.add_button('Март', color='primary', payload = {"month_page":"03"})
    keyboard.add_button('Апрель', color='primary', payload = {"month_page":"04"})
    keyboard.add_button('Май', color='primary', payload = {"month_page":"05"})
    keyboard.add_line()
    keyboard.add_button('Июнь', color='primary', payload = {"month_page":"06"})
    keyboard.add_button('Июль', color='primary', payload = {"month_page":"07"})
    keyboard.add_button('Август', color='primary', payload = {"month_page":"08"})
    keyboard.add_line()
    keyboard.add_button('Сентябрь', color='primary', payload = {"month_page":"09"})
    keyboard.add_button('Октябрь', color='primary', payload = {"month_page":"10"})
    keyboard.add_button('Ноябрь', color='primary', payload = {"month_page":"11"})
    keyboard.add_line()
    keyboard.add_button('Отменить', color='default', payload = {"cancel":"month_page"})

    vk.messages.send(
        peer_id=user_id,
        random_id=get_random_id(),
        keyboard=keyboard.get_keyboard(),
        message = 'Установите месяц:')

def day_page1(user_id, month): #Потеря аргумента при перелистывании страниц
    keyboard = VkKeyboard(one_time=False)

    keyboard.add_button('01', color='primary', payload = {"date_page":"01."+month})
    keyboard.add_button('02', color='primary', payload = {"date_page":"02."+month})
    keyboard.add_button('03', color='primary', payload = {"date_page":"03."+month})
    keyboard.add_button('04', color='primary', payload = {"date_page":"04."+month})
    keyboard.add_line()
    keyboard.add_button('05', color='primary', payload = {"date_page":"05."+month})
    keyboard.add_button('06', color='primary', payload = {"date_page":"06."+month})
    keyboard.add_button('07', color='primary', payload = {"date_page":"07."+month})
    keyboard.add_button('08', color='primary', payload = {"date_page":"08."+month})
    keyboard.add_line()
    keyboard.add_button('09', color='primary', payload = {"date_page":"09."+month})
    keyboard.add_button('10', color='primary', payload = {"date_page":"10."+month})
    keyboard.add_button('11', color='primary', payload = {"date_page":"11."+month})
    keyboard.add_button('12', color='primary', payload = {"date_page":"12."+month})
    keyboard.add_line()
    keyboard.add_button('Отменить', color='default', payload = {"cancel":"day_page1"})
    keyboard.add_button('Далее >>', color='default', payload = {"next_page":"day_page2"})

    vk.messages.send(
        peer_id=user_id,
        random_id=get_random_id(),
        keyboard=keyboard.get_keyboard(),
        message = 'Установите день:')

def day_page2(user_id, month):
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('13', color='primary', payload = {"date_page":"13."+month})
    keyboard.add_button('14', color='primary', payload = {"date_page":"14."+month})
    keyboard.add_button('15', color='primary', payload = {"date_page":"15."+month})
    keyboard.add_button('16', color='primary', payload = {"date_page":"16."+month})
    keyboard.add_line()
    keyboard.add_button('17', color='primary', payload = {"date_page":"17."+month})
    keyboard.add_button('18', color='primary', payload = {"date_page":"18."+month})
    keyboard.add_button('19', color='primary', payload = {"date_page":"19."+month})
    keyboard.add_button('20', color='primary', payload = {"date_page":"20."+month})
    keyboard.add_line()
    keyboard.add_button('21', color='primary', payload = {"date_page":"21."+month})
    keyboard.add_button('22', color='primary', payload = {"date_page":"22."+month})
    keyboard.add_button('23', color='primary', payload = {"date_page":"23."+month})
    keyboard.add_button('24', color='primary', payload = {"date_page":"24."+month})
    keyboard.add_line()
    keyboard.add_button('<< Назад', color='default', payload = {"next_page":"day_page1"})
    keyboard.add_button('Отменить', color='default', payload = {"cancel":"day_page2"})
    keyboard.add_button('Далее >>', color='default', payload = {"next_page":"day_page3"})

    vk.messages.send(
        peer_id=user_id,
        random_id=get_random_id(),
        keyboard=keyboard.get_keyboard(),
        message = 'Установите день:')

def day_page3(user_id, month):
    keyboard = VkKeyboard(one_time=False)

    keyboard.add_button('25', color='primary', payload = {"date_page":"25."+month})
    keyboard.add_button('26', color='primary', payload = {"date_page":"26."+month})
    keyboard.add_button('27', color='primary', payload = {"date_page":"27."+month})
    keyboard.add_button('28', color='primary', payload = {"date_page":"28."+month})
    keyboard.add_line()
    if month == '02':
        keyboard.add_button('29', color='primary', payload = {"date_page":"29."+month})
    elif ((month == '04') or (month == '06') or (month == '09') or (month == '11')):
        keyboard.add_button('30', color='primary', payload = {"date_page":"30."+month})
    else:
        keyboard.add_button('31', color='primary', payload = {"date_page":"31."+month})
    keyboard.add_line()
    keyboard.add_button('<< Назад', color='default', payload = {"next_page":"day_page2"})
    keyboard.add_button('Отменить', color='default', payload = {"cancel":"day_page3"})

    vk.messages.send(
    peer_id=user_id,
    random_id=get_random_id(),
    keyboard=keyboard.get_keyboard(),
    message = 'Установите день:')