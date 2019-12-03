# sessiyabot/core/online_monitor.py
# Monitor to write down online status of followers
# Marakulin Andrey @annndruha
# 2019

import time
import datetime
import traceback

import psycopg2
import numpy as np
import matplotlib.pyplot as plt

import config ## from data !!!!!!!!!

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

def yesterday_plot(id):
    with connection.cursor() as cur:
        cur.execute("SELECT tstamp FROM sessiyabot.online WHERE id=%s ORDER BY tstamp DESC LIMIT 2880;", (id,))
        timestamps = cur.fetchmany(2880)

        cur.execute("SELECT status FROM sessiyabot.online WHERE id=%s ORDER BY tstamp DESC LIMIT 2880;", (id,))
        status = cur.fetchmany(2880)


    if len(timestamps)<3:
        raise Exception('small data') # Скорей всего вы подписались недавно, эта функция заработает для вас через 10 минут 

    hour_bins = []
    current_dat = timestamps[0][0].day
    for i, timestamp in enumerate(timestamps):
        if status[i][0]==1:
            con = ((current_dat==1)and(timestamp[0].day==31)) or ((current_dat==1)and(timestamp[0].day==30)) or ((current_dat==1)and(timestamp[0].day==29)) or ((current_dat==1)and(timestamp[0].day==28))
            if (timestamp[0].day == current_dat-1) or con:
                h = timestamp[0].hour
                hour_bins.append(h)



    from collections import Counter
    print(Counter(hour_bins).keys())
    print(Counter(hour_bins).values())

    fig, axs = plt.subplots()

    yesterday = timestamps[0][0] - datetime.timedelta(hours=24)
    lbl = 'Статистика за '+str(yesterday.day)+'.'+str(yesterday.month)+'.'+str(yesterday.year)
    plt.grid(True, linestyle =":")
    plt.xlabel('Часы')
    plt.ylabel('Минут в сети')


    plt.xticks(ticks=range(0,24), size='small')
    
    axs.hist(hour_bins, bins = range(0,25), label=lbl, color='#8b00ff') 
    plt.xlim([0,24])

    axs.legend()
    plt.savefig('./temp.png', dpi=400, bbox_inches='tight')
    plt.show()

    time_online = str(datetime.timedelta(minutes= len(hour_bins)))
    return 'Вчера вы были онлайн: '+ time_online.split(':')[0]+'ч '+time_online.split(':')[1]+'м'


def day_plot(id):
    with connection.cursor() as cur:
        cur.execute("SELECT tstamp FROM sessiyabot.online WHERE id=%s ORDER BY tstamp DESC LIMIT 1440;", (id,))
        timestamps = cur.fetchmany(1440)

        cur.execute("SELECT status FROM sessiyabot.online WHERE id=%s ORDER BY tstamp DESC LIMIT 1440;", (id,))
        status = cur.fetchmany(1440)


    if len(timestamps)<3:
        raise Exception('small data') # Скорей всего вы подписались недавно, эта функция заработает для вас через 10 минут 

    hour_bins = []
    last_hour = timestamps[0][0].hour
    for i, timestamp in enumerate(timestamps):
        if status[i][0]==1:
            h = timestamp[0].hour
            if h>last_hour:
                hour_bins.append(h-24)
            else:
                hour_bins.append(h)


    fig, axs = plt.subplots()

    lbl = 'Статистика за последние сутки'
    plt.grid(True, linestyle =":")
    plt.xlabel('Часы')
    plt.ylabel('Минут в сети')


    plot_range = range(last_hour-23, last_hour+1)
    x_lables = []
    for l in plot_range:
        if l<0:
            l+=24
            x_lables.append(str(l))
        else:
            x_lables.append(str(l))

    plt.xticks(ticks=plot_range, labels=x_lables, size='small')
    
    axs.hist(hour_bins, bins = range(last_hour-23, last_hour+2), label=lbl, color='#8b00ff') 
    plt.xlim(last_hour-23, last_hour+1)

    axs.legend()
    plt.savefig('./temp.png', dpi=400, bbox_inches='tight')
    plt.show()

    time_online = str(datetime.timedelta(minutes= len(hour_bins)))
    return 'За последние сутки вы были онлайн: '+ time_online.split(':')[0]+'ч '+time_online.split(':')[1]+'м'


id = 478143147
print(day_plot(id))