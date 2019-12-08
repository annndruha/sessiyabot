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

from data import config ## !!!!!!!!!

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
        cur.execute("SELECT tstamp, status FROM sessiyabot.online WHERE id=%s ORDER BY tstamp DESC LIMIT 2880;", (id,))
        time_and_status = cur.fetchmany(2880)

    if len(time_and_status)<3:
        raise NameError('small data') # Скорей всего вы подписались недавно, эта функция заработает для вас через 10 минут 

    hour_bins = []
    current_dat = time_and_status[0][0].day
    for i, ts_point in enumerate(time_and_status):
        if ts_point[1]==1:
            con = ((current_dat==1)and(ts_point[0].day==31)) or ((current_dat==1)and(ts_point[0].day==30)) or ((current_dat==1)and(ts_point[0].day==29)) or ((current_dat==1)and(ts_point[0].day==28))
            if (ts_point[0].day == current_dat-1) or con:
                h = ts_point[0].hour
                hour_bins.append(h)



    fig, axs = plt.subplots()

    yesterday = time_and_status[0][0] - datetime.timedelta(hours=24)
    lbl = 'Статистика за '+str(yesterday.day)+'.'+str(yesterday.month)+'.'+str(yesterday.year)
    axs.set_axisbelow(True)
    axs.yaxis.grid(True, linestyle =":")
    axs.xaxis.grid(True, linestyle =":")
    plt.xlabel('Часы')
    plt.ylabel('Минут в сети')


    plt.xticks(ticks=range(0,24), size='small')
    
    axs.hist(hour_bins, bins = range(0,25), label=lbl, color='#8b00ff') 
    plt.xlim([0,24])

    axs.legend()
    plt.savefig('data/temp.png', dpi=400, bbox_inches='tight')
    plt.show()

    time_online = str(datetime.timedelta(minutes= len(hour_bins)))
    return 'Вчера вы были онлайн: '+ time_online.split(':')[0]+' ч '+time_online.split(':')[1]+' м'


def day_plot(id):
    with connection.cursor() as cur: ## Объединить в один запрос!
        cur.execute("SELECT tstamp, status FROM sessiyabot.online WHERE id=%s ORDER BY tstamp DESC LIMIT 1440;", (id,))
        #cur.execute("select * from sessiyabot.day_bins where id =%s;")
        time_and_status = cur.fetchmany(1440)


    #check in members
    #raise ....


    if len(time_and_status)<3:
        raise NameError('small data') # Скорей всего вы подписались недавно, эта функция заработает для вас через 10 минут 

    hour_bins = []
    last_hour = time_and_status[0][0].hour
    for i, ts_point in enumerate(time_and_status):
        if ts_point[1]==1:
            h = ts_point[0].hour
            if h>last_hour:
                hour_bins.append(h-24)
            else:
                hour_bins.append(h)


    fig, axs = plt.subplots()

    lbl = 'Статистика за последние сутки'
    axs.set_axisbelow(True)
    axs.yaxis.grid(True, linestyle =":")
    axs.xaxis.grid(True, linestyle =":")
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
    plt.savefig('data/temp.png', dpi=400, bbox_inches='tight')
    #plt.show()

    time_online = str(datetime.timedelta(minutes= len(hour_bins)))
    return 'За последние сутки вы были онлайн: '+ time_online.split(':')[0]+' ч '+time_online.split(':')[1]+' м'

print(yesterday_plot(35886154))