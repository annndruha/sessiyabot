# Script to add user online status into database
import time
import datetime

import psycopg2
from vk_api import VkApi

import config


vk = VkApi(token=config.access_token)
def reconnect_vk():
    global vk
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


def add_users_data():
        members = vk.method('groups.getMembers', {'group_id': 'sessiyabot', 'fields':"online"})

        onlines = []
        [onlines.append(user['online']) for user in members['items']]
        onlines = 'ARRAY' + str(onlines)

        ids = []
        [ids.append(user['id']) for user in members['items']]
        ids = 'ARRAY' + str(ids)

        with connection.cursor() as cur:
            cur.execute(f"SELECT * FROM update_status({ids},{onlines});")
            res = cur.fetchone()
            connection.commit()
            return res[0]


print('=== Members monitor start at '+  datetime.datetime.strftime(datetime.datetime.now(), "%Y.%m.%d %H:%M:%S"))
start_time = time.time()
while True:
        try:
            add_users_data()
        except Exception as err:
            # reconnect_vk()
            # reconnect_db()
            # print('===RECONNECT at ' +  datetime.datetime.strftime(datetime.datetime.now(), "%Y.%m.%d %H:%M:%S"))
            print(err)
            time.sleep(10)
        time.sleep(60.0 - ((time.time() - start_time) % 60.0))
