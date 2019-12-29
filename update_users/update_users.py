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
        except:
            reconnect_vk()
            reconnect_db()
            print('===RECONNECT at ' +  datetime.datetime.strftime(datetime.datetime.now(), "%Y.%m.%d %H:%M:%S"))
            time.sleep(10)
        time.sleep(60.0 - ((time.time() - start_time) % 60.0))


# CREATE OR REPLACE FUNCTION sessiyabot.update_status(ids integer[], status integer[])
# RETURNS integer
# LANGUAGE plpgsql
# AS $function$
# DECLARE
#     id integer;
#     ts timestamp;
#     n integer :=1;
#     BEGIN
#         ts = date_trunc('seconds', LOCALTIMESTAMP);
#         FOREACH id IN ARRAY ids
#             LOOP
#                 execute 'INSERT INTO online (id, tstamp, status) VALUES('|| id || ','|| quote_literal(ts) || ','|| status[n] ||');';
#                 n = n+1;
#             END LOOP;
#         DELETE FROM online WHERE tstamp < now() - interval '7 days';
#         RETURN 0;
#     END;
# $function$;