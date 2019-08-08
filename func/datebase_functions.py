# Sessiya_bot: datebase_functions - SQL fuction for work with datebase
# Маракулин Андрей @annndruha
# 2019
import psycopg2

from data import config as config

connection = psycopg2.connect(
    dbname=config.db_name,
    user=config.db_account,
    password=config.db_password,
    host= config.db_host,
    port = config.db_port)

#Getters
def get_user_exist(user_id):
    with connection.cursor() as cur:
        cur.execute("SELECT id FROM sessiyabot.users WHERE id=%s;", (user_id,))
        if (cur.fetchone()==None):
            return False
        else:
            return True

def get_user_full_info(user_id):
    with connection.cursor() as cur:
        cur.execute("SELECT * FROM sessiyabot.users WHERE id=%s;", (user_id,))
        return cur.fetchone()

def get_user_examdate(user_id):
    with connection.cursor() as cur:
        cur.execute("SELECT examdate FROM sessiyabot.users WHERE id=%s;", (user_id,))
        examdate = cur.fetchone()[0]
        return examdate

def get_user_notifytime(user_id):
    with connection.cursor() as cur:
        cur.execute("SELECT notifytime FROM sessiyabot.users WHERE id=%s;", (user_id,))
        notifytime = cur.fetchone()[0]
        return notifytime

def get_user_subscribe(user_id):
    with connection.cursor() as cur:
        cur.execute("SELECT subscribe FROM sessiyabot.users WHERE id=%s;", (user_id,))
        subscribe = cur.fetchone()[0]
        return subscribe

def get_user_tz(user_id):
    with connection.cursor() as cur:
        cur.execute("SELECT tz FROM sessiyabot.users WHERE id=%s;", (user_id,))
        tz = cur.fetchone()[0]
        return tz

def get_user_firstname(user_id):
    with connection.cursor() as cur:
        cur.execute("SELECT firstname FROM sessiyabot.users WHERE id=%s;", (user_id,))
        firstname = cur.fetchone()[0]
        return firstname

def get_user_lastname(user_id):
    with connection.cursor() as cur:
        cur.execute("SELECT lastname FROM sessiyabot.users WHERE id=%s;", (user_id,))
        lastname = cur.fetchone()[0]
        return lastname

def get_users_who_sub_at(time):
    with connection.cursor() as cur:
        cur.execute("SELECT * FROM sessiyabot.users WHERE notifytime=%s AND subscribe=True;", (time,))
        return cur.fetchall()

def get_users_all():
    with connection.cursor() as cur:
        cur.execute("SELECT * FROM sessiyabot.users")
        return cur.fetchall()

#Setters
def add_user(user_id):
    if get_user_exist(user_id)==False:
        with connection.cursor() as cur:
            cur.execute("INSERT INTO sessiyabot.users (id) VALUES (%s);", (user_id,))
            connection.commit()

def set_examdate(user_id, examdate):
    with connection.cursor() as cur:
        cur.execute("UPDATE sessiyabot.users SET examdate=%s WHERE id=%s;", (examdate, user_id))
        connection.commit()

def set_notifytime(user_id, notifytime):
    with connection.cursor() as cur:
        cur.execute("UPDATE sessiyabot.users SET notifytime=%s WHERE id=%s;", (notifytime, user_id))
        connection.commit()

def set_subscribe(user_id, subscribe):
    with connection.cursor() as cur:
        cur.execute("UPDATE sessiyabot.users SET subscribe=%s WHERE id=%s;", (subscribe, user_id))
        connection.commit()

def set_tz(user_id, tz):
    with connection.cursor() as cur:
        cur.execute("UPDATE sessiyabot.users SET tz=%s WHERE id=%s;", (tz, user_id))
        connection.commit()

def set_firstname(user_id, firstname):
    with connection.cursor() as cur:
        cur.execute("UPDATE sessiyabot.users SET firstname=%s WHERE id=%s;", (firstname, user_id))
        connection.commit()

def set_lastname(user_id, lastname):
    with connection.cursor() as cur:
        cur.execute("UPDATE sessiyabot.users SET lastname=%s WHERE id=%s;", (lastname, user_id))
        connection.commit()