# sessiyabot/core/keybords
# - list of keybords pages
# Маракулин Андрей @annndruha
# 2019
from vk_api import VkApi
from vk_api.keyboard import VkKeyboard
from vk_api.utils import get_random_id

from data import config
from func import database_functions as db

vk = VkApi(token=config.access_token)

def send_keyboard(user_id, kb, message):
    vk.method('messages.send', {'user_id': user_id, 'keyboard': kb, 'message': message, 'random_id': get_random_id()})

# Pages of keyboard menu:
# main_page
def main_page(user_id, ans='Главное меню:'):
    kb = VkKeyboard(one_time=False)
    kb.add_button('Настройки напоминаний', color='primary', payload = ["next_page","notify_page"])
    kb.add_line()
    kb.add_button('Сменить дату экзамена', color='primary', payload = ["next_page","month_page"])
    kb.add_line()
    kb.add_button('Подбодри меня!', color='positive')

    send_keyboard(user_id, kb.get_keyboard(), ans)

# notify_page
def notify_page(user_id, ans='Настройки напоминаний:'):
    kb = VkKeyboard(one_time=False)
    data =db.get_user(user_id)
    if data is not None:
        if data[2] is not None:
            if (data[3] == False):
                kb.add_button('Включить напоминания', color='positive', payload = ["command","set_subcribe", "start"])
                kb.add_line()
                kb.add_button('Изменить время напоминаний', color='primary', payload = ["next_page","hour_page1"])
            else:
                kb.add_button('Выключить напоминания', color='negative', payload = ["command","set_subcribe", "stop"])
                kb.add_line()
                kb.add_button('Изменить время напоминаний', color='primary', payload = ["next_page","hour_page1"])
        else:
            kb.add_button('Настроить напоминания', color='positive', payload = ["next_page","hour_page1"])
    else:
        kb.add_button('Настроить напоминания', color='positive', payload = ["next_page","hour_page1"])
    kb.add_line()
    kb.add_button('Изменить часовой пояс', color='primary', payload = ["next_page","tz_page"])
    kb.add_line()
    kb.add_button('Отмена', color='default', payload = ["command","cancel"])

    send_keyboard(user_id, kb.get_keyboard(), ans)

# hour_page1
def hour_page1(user_id, ans = 'Выберите новое время:'):
    kb = VkKeyboard(one_time=False)

    kb.add_button('00:', color='primary', payload = ["jump","minute_page","00"])
    kb.add_button('01:', color='primary', payload = ["jump","minute_page","01"])
    kb.add_button('02:', color='primary', payload = ["jump","minute_page","02"])
    kb.add_button('03:', color='primary', payload = ["jump","minute_page","03"])
    kb.add_line()
    kb.add_button('04:', color='primary', payload = ["jump","minute_page","04"])
    kb.add_button('05:', color='primary', payload = ["jump","minute_page","05"])
    kb.add_button('06:', color='primary', payload = ["jump","minute_page","06"])
    kb.add_button('07:', color='primary', payload = ["jump","minute_page","07"])
    kb.add_line()
    kb.add_button('08:', color='primary', payload = ["jump","minute_page","08"])
    kb.add_button('09:', color='primary', payload = ["jump","minute_page","09"])
    kb.add_button('10:', color='primary', payload = ["jump","minute_page","10"])
    kb.add_button('11:', color='primary', payload = ["jump","minute_page","11"])
    kb.add_line()
    kb.add_button('Отменить', color='default', payload = ["command","cancel"])
    kb.add_button('Далее ->', color='default', payload = ["next_page","hour_page2"])

    send_keyboard(user_id, kb.get_keyboard(), ans)

# hour_page2
def hour_page2(user_id, ans = 'Выберите новое время:'):
    kb = VkKeyboard(one_time=False)

    kb.add_button('12:', color='primary', payload = ["jump","minute_page","12"])
    kb.add_button('13:', color='primary', payload = ["jump","minute_page","13"])
    kb.add_button('14:', color='primary', payload = ["jump","minute_page","14"])
    kb.add_button('15:', color='primary', payload = ["jump","minute_page","15"])
    kb.add_line()
    kb.add_button('16:', color='primary', payload = ["jump","minute_page","16"])
    kb.add_button('17:', color='primary', payload = ["jump","minute_page","17"])
    kb.add_button('18:', color='primary', payload = ["jump","minute_page","18"])
    kb.add_button('19:', color='primary', payload = ["jump","minute_page","19"])
    kb.add_line()
    kb.add_button('20:', color='primary', payload = ["jump","minute_page","20"])
    kb.add_button('21:', color='primary', payload = ["jump","minute_page","21"])
    kb.add_button('22:', color='primary', payload = ["jump","minute_page","22"])
    kb.add_button('23:', color='primary', payload = ["jump","minute_page","23"])
    kb.add_line()
    kb.add_button('<- Назад', color='default', payload = ["next_page","hour_page1"])
    kb.add_button('Отменить', color='default', payload = ["command","cancel"])

    send_keyboard(user_id, kb.get_keyboard(), ans)

# minute_page
def minute_page(user_id, hour, ans = 'Завершите выбор времени:'):
    kb = VkKeyboard(one_time=False)

    kb.add_button(hour + ':00', color='primary', payload = ["command","set_time","time " + hour + ":00"])
    kb.add_button(hour + ':05', color='primary', payload = ["command","set_time","time " + hour + ":05"])
    kb.add_button(hour + ':10', color='primary', payload = ["command","set_time","time " + hour + ":10"])
    kb.add_button(hour + ':15', color='primary', payload = ["command","set_time","time " + hour + ":15"])
    kb.add_line()
    kb.add_button(hour + ':20', color='primary', payload = ["command","set_time","time " + hour + ":20"])
    kb.add_button(hour + ':25', color='primary', payload = ["command","set_time","time " + hour + ":25"])
    kb.add_button(hour + ':30', color='primary', payload = ["command","set_time","time " + hour + ":30"])
    kb.add_button(hour + ':35', color='primary', payload = ["command","set_time","time " + hour + ":35"])
    kb.add_line()
    kb.add_button(hour + ':40', color='primary', payload = ["command","set_time","time " + hour + ":40"])
    kb.add_button(hour + ':45', color='primary', payload = ["command","set_time","time " + hour + ":45"])
    kb.add_button(hour + ':50', color='primary', payload = ["command","set_time","time " + hour + ":50"])
    kb.add_button(hour + ':55', color='primary', payload = ["command","set_time","time " + hour + ":55"])
    kb.add_line()
    kb.add_button('Отменить', color='default', payload = ["command","cancel"])

    send_keyboard(user_id, kb.get_keyboard(), ans)

# tz_page
def tz_page(user_id, ans = 'Установите новый часовой пояс:'):
    kb = VkKeyboard(one_time=False)
    
    my_col = ['primary']*12
    data = db.get_user(user_id)

    if data is not None:
        if ((data[4] >=0) and (data[4] <=11)):
            my_col[data[4]] = 'positive'

    kb.add_button('МСК', color=my_col[0], payload = ["command","set_tz","tz 0"])
    kb.add_button('МСК+1', color=my_col[1], payload = ["command","set_tz","tz 1"])
    kb.add_button('МСК+2', color=my_col[2], payload = ["command","set_tz","tz 2"])
    kb.add_button('МСК+3', color=my_col[3], payload = ["command","set_tz","tz 3"])
    kb.add_line()
    kb.add_button('МСК+4', color=my_col[4], payload = ["command","set_tz","tz 4"])
    kb.add_button('МСК+5', color=my_col[5], payload = ["command","set_tz","tz 5"])
    kb.add_button('МСК+6', color=my_col[6], payload = ["command","set_tz","tz 6"])
    kb.add_button('МСК+7', color=my_col[7], payload = ["command","set_tz","tz 7"])
    kb.add_line()
    kb.add_button('МСК+8', color=my_col[8], payload = ["command","set_tz","tz 8"])
    kb.add_button('МСК+9', color=my_col[9], payload = ["command","set_tz","tz 9"])
    kb.add_button('МСК+10', color=my_col[10], payload = ["command","set_tz","tz 10"])
    kb.add_button('МСК+11', color=my_col[11], payload = ["command","set_tz","tz 11"])
    kb.add_line()
    kb.add_button('Отменить', color='default', payload = ["command","cancel"])

    send_keyboard(user_id, kb.get_keyboard(), ans)

# month_page
def month_page(user_id, ans = 'Установите месяц:'):
    kb = VkKeyboard(one_time=False)

    kb.add_button('Январь', color='primary', payload = ["jump","day_page1","01"])
    kb.add_button('Февраль', color='primary', payload = ["jump","day_page1","02"])
    kb.add_button('Март', color='primary', payload = ["jump","day_page1","03"])
    kb.add_line()
    kb.add_button('Апрель', color='primary', payload = ["jump","day_page1","04"])
    kb.add_button('Май', color='primary', payload = ["jump","day_page1","05"])
    kb.add_button('Июнь', color='primary', payload = ["jump","day_page1","06"])
    kb.add_line()
    kb.add_button('Июль', color='primary', payload = ["jump","day_page1","07"])
    kb.add_button('Август', color='primary', payload = ["jump","day_page1","08"])
    kb.add_button('Сентябрь', color='primary', payload = ["jump","day_page1","09"])
    kb.add_line()
    kb.add_button('Октябрь', color='primary', payload = ["jump","day_page1","10"])
    kb.add_button('Ноябрь', color='primary', payload = ["jump","day_page1","11"])
    kb.add_button('Декабрь', color='primary', payload = ["jump","day_page1","12"])
    kb.add_line()
    kb.add_button('Отменить', color='default', payload = ["command","cancel"])

    send_keyboard(user_id, kb.get_keyboard(), ans)

# day_page1
def day_page1(user_id, month, ans ='Установите день:'):
    kb = VkKeyboard(one_time=False)

    kb.add_button('01', color='primary', payload = ["command","set_date","01." + month])
    kb.add_button('02', color='primary', payload = ["command","set_date","02." + month])
    kb.add_button('03', color='primary', payload = ["command","set_date","03." + month])
    kb.add_button('04', color='primary', payload = ["command","set_date","04." + month])
    kb.add_line()
    kb.add_button('05', color='primary', payload = ["command","set_date","05." + month])
    kb.add_button('06', color='primary', payload = ["command","set_date","06." + month])
    kb.add_button('07', color='primary', payload = ["command","set_date","07." + month])
    kb.add_button('08', color='primary', payload = ["command","set_date","08." + month])
    kb.add_line()
    kb.add_button('09', color='primary', payload = ["command","set_date","09." + month])
    kb.add_button('10', color='primary', payload = ["command","set_date","10." + month])
    kb.add_button('11', color='primary', payload = ["command","set_date","11." + month])
    kb.add_button('12', color='primary', payload = ["command","set_date","12." + month])
    kb.add_line()
    kb.add_button('Отменить', color='default', payload = ["command","cancel"])
    kb.add_button('Далее ->', color='default', payload = ["jump","day_page2", month])

    send_keyboard(user_id, kb.get_keyboard(), ans)

# day_page2
def day_page2(user_id, month, ans = 'Установите день:'):
    kb = VkKeyboard(one_time=False)

    kb.add_button('13', color='primary', payload = ["command","set_date","13." + month])
    kb.add_button('14', color='primary', payload = ["command","set_date","14." + month])
    kb.add_button('15', color='primary', payload = ["command","set_date","15." + month])
    kb.add_button('16', color='primary', payload = ["command","set_date","16." + month])
    kb.add_line()
    kb.add_button('17', color='primary', payload = ["command","set_date","17." + month])
    kb.add_button('18', color='primary', payload = ["command","set_date","18." + month])
    kb.add_button('19', color='primary', payload = ["command","set_date","19." + month])
    kb.add_button('20', color='primary', payload = ["command","set_date","20." + month])
    kb.add_line()
    kb.add_button('21', color='primary', payload = ["command","set_date","21." + month])
    kb.add_button('22', color='primary', payload = ["command","set_date","22." + month])
    kb.add_button('23', color='primary', payload = ["command","set_date","23." + month])
    kb.add_button('24', color='primary', payload = ["command","set_date","24." + month])
    kb.add_line()
    kb.add_button('<- Назад', color='default', payload = ["jump","day_page1", month])
    kb.add_button('Отменить', color='default', payload = ["command","cancel"])
    kb.add_button('Далее ->', color='default', payload = ["jump","day_page3", month])

    send_keyboard(user_id, kb.get_keyboard(), ans)

# day_page3
def day_page3(user_id, month, ans = 'Установите день:'):
    kb = VkKeyboard(one_time=False)

    kb.add_button('25', color='primary', payload = ["command","set_date","25." + month])
    kb.add_button('26', color='primary', payload = ["command","set_date","26." + month])
    kb.add_button('27', color='primary', payload = ["command","set_date","27." + month])
    kb.add_button('28', color='primary', payload = ["command","set_date","28." + month])
    kb.add_line()
    if month == '02':
        kb.add_button('29', color='primary', payload = ["command","set_date","29." + month])
    elif ((month == '04') or (month == '06') or (month == '09') or (month == '11')):
        kb.add_button('29', color='primary', payload = ["command","set_date","29." + month])
        kb.add_button('30', color='primary', payload = ["command","set_date","30." + month])
    else:
        kb.add_button('29', color='primary', payload = ["command","set_date","29." + month])
        kb.add_button('30', color='primary', payload = ["command","set_date","30." + month])
        kb.add_button('31', color='primary', payload = ["command","set_date","31." + month])
    kb.add_line()
    kb.add_button('<- Назад', color='default', payload = ["jump", "day_page2", month])
    kb.add_button('Отменить', color='default', payload = ["command", "cancel"])

    send_keyboard(user_id, kb.get_keyboard(), ans)