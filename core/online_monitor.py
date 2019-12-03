# sessiyabot/core/online_monitor.py
# Marakulin Andrey
# Monitor to write down online status of followers
# 2019
import time
import datetime
import traceback

from vk_api import VkApi
from vk_api.keyboard import VkKeyboard
from vk_api.longpoll import VkLongPoll, VkEventType
import psycopg2

from data import config

vk = VkApi(token=config.access_token)

connection = psycopg2.connect(dbname=config.db_name,
    user=config.db_account,
    password=config.db_password,
    host= config.db_host,
    port = config.db_port)

def reconnect_db():
    global connection
    connection = psycopg2.connect(dbname=config.db_name,
    user=config.db_account,
    password=config.db_password,
    host= config.db_host,
    port = config.db_port)


def day_plot(id):
    '''
    Dont work well!
    '''
    # user = vk.method('users.get', {'user_ids': id})

    with connection.cursor() as cur:
        cur.execute("SELECT tstamp FROM sessiyabot.online WHERE id=%s", (id,)) # AND status=1;
        timestams = cur.fetchmany(1440)

        cur.execute("SELECT status FROM sessiyabot.online WHERE id=%s", (id,)) # ORDER By
        status = cur.fetchmany(1440)
        #connection.commit()


    print(len(timestams))
    online = []
    for i, timestamp in enumerate(timestams):
        if status[i][0]==1:
            online.append(timestamp[0])
    print(len(online))

    #print(min(online))
    #print(max(online))
    if len(online)<3:
        raise Exception('small data') # Скорей всего вы подписались недавно, эта функция заработает для вас через 10 минут 

    if max(online)-min(online) < datetime.timedelta(minutes= 5):
        raise Exception('only one hour data') # Вы были в сети не больше пяти минут, поздравляю!
        

    hour_bins = []
    [hour_bins.append(status.hour) for status in online]


    fig, axs = plt.subplots()
    
    
    plt.grid(True, linestyle =":")
    plt.xlabel('Часы')
    plt.ylabel('Минут в сети')
    lbl = 'Статистика для id= '+ str(id)



    h = datetime.datetime.now().hour
    rng = range(h, h-24, -1)

    plt.xticks(rng, size='small')
    axs.hist(hour_bins, bins = range(min(rng), max(rng)+2), label=lbl, color='#8b00ff')
    plt.xlim(min(rng), max(rng)+1)


    axs.legend()
    plt.savefig('./temp.png', dpi=400, bbox_inches='tight')
    plt.show()

    return 0