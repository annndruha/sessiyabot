# Sessiya_bot: datebase_functions - SQL fuction fro work with datebase
# Маракулин Андрей @annndruha
# 2019
import psycopg2

from data import config as cfg

connection = psycopg2.connect(
    dbname=cfg.datebase_name,
    user=cfg.datebase_user,
    password=cfg.datebase_password,
    host= cfg.datebase_host,
    port = cfg.datebase_port)

#Getters
def get_users():
    with connection.cursor() as cur:
        cur.execute("""SELECT * FROM "sessiya-bot".users""")
        users = cur.fetchall()
        return users

def get_users_who_sub_at(time):
    with connection.cursor() as cur:
        cur.execute(f"""SELECT * FROM "sessiya-bot".users WHERE notifytime='{time}'AND subscribe=True;""")
        users = cur.fetchall()
        return users

def get_user(user_id):
    with connection.cursor() as cur:
        cur.execute(f"""SELECT * FROM "sessiya-bot".users WHERE id='{user_id}';""")
        user = cur.fetchone()
        return user

def check_user_exist(user_id):
    with connection.cursor() as cur:
        cur.execute(f"""SELECT * FROM "sessiya-bot".users WHERE id='{user_id}';""")
        if (cur.fetchone()!=None):
            return True
        else:
            return False

def check_user_subscribe(user_id):
    with connection.cursor() as cur:
        cur.execute(f"""SELECT * FROM "sessiya-bot".users WHERE id='{user_id}';""")
        user = cur.fetchone()
        if (user==None):
            return False
        elif (user[3]==True):#subscribe status locate
            return True
        else:
            return False

#Setters
def set_date(user_id, date):
    with connection.cursor() as cur:
        cur.execute("""UPDATE "sessiya-bot".users SET examdate=%s WHERE id=%s;""", (date, user_id))
        connection.commit()

def set_time(user_id, time):
    with connection.cursor() as cur:
        cur.execute("""UPDATE "sessiya-bot".users SET notifytime=%s WHERE id=%s;""", (time, user_id))
        connection.commit()

def add_user(user_id, date, time):
    with connection.cursor() as cur:
        if check_user_exist(user_id)==False:
            cur.execute("""INSERT INTO "sessiya-bot".users (id,examdate,notifytime) VALUES (%s,%s,%s);""", (user_id, date, time))
        else:
            set_date(user_id, date)
            set_time(user_id, time)
        connection.commit()

def set_subscribe(user_id, sub):
    with connection.cursor() as cur:
        cur.execute("""UPDATE "sessiya-bot".users SET subscribe=%s WHERE id=%s;""", (sub, user_id))
        connection.commit()

def set_tz(user_id, new_tz):
    with connection.cursor() as cur:
        cur.execute("""UPDATE "sessiya-bot".users SET tz=%s WHERE id=%s;""", (new_tz, user_id))
        connection.commit()

def set_firstname(user_id, name):
    with connection.cursor() as cur:
        cur.execute("""UPDATE "sessiya-bot".users SET firstname=%s WHERE id=%s;""", (name, user_id))
        connection.commit()

def set_lastname(user_id, surname):
    with connection.cursor() as cur:
        cur.execute("""UPDATE "sessiya-bot".users SET lastname=%s WHERE id=%s;""", (surname, user_id))
        connection.commit()