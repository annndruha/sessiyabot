# Sessiya_bot: engine - Main use functions
# Маракулин Андрей @annndruha
# 2019
import datetime as dt

# DateTime class functions
def datetime_now_obj():
    delta=dt.timedelta(seconds = 18000)
    tzone = dt.timezone(delta)
    return dt.datetime.now(tzone)

def datetime_to_str(datetime_object):
    return dt.datetime.strftime(datetime_object, '%d.%m.%Y %H:%M')

def str_to_datetime(string):
    return dt.datetime.strptime(string, '%d.%m.%Y %H:%M')

# Date class functions
def date_now_obj():
    return datetime_now_obj().date()

def date_to_str(date_obj):
    return dt.date.strftime(date_obj, '%d.%m.%Y')

def str_to_date(string):
    return dt.datetime.strptime(string, '%d.%m.%Y').date()

# Time class functions
def time_now_obj():
    return dt.time(datetime_now_obj().hour, datetime_now_obj().minute)

def time_to_str(time_obj):
    return dt.time.strftime(time_obj, '%H:%M')

def str_to_time(string):
    return dt.datetime.strptime(string, '%H:%M').time()

# Validate format functions
def validate_date(date_text):
    try:
        if date_text != dt.datetime.strptime(date_text, '%d.%m.%Y').strftime('%d.%m.%Y'):
            raise ValueError
        return True
    except ValueError:
        return False

def validate_time(time_text):
    try:
        if time_text != dt.datetime.strptime(time_text, '%H:%M').strftime('%H:%M'):
            raise ValueError
        return True
    except ValueError:
        return False

# Logs timestamp
def timestamp():
    return dt.datetime.strftime(datetime_now_obj(), '%d.%m.%Y %H:%M:%S')

def datetime_to_random_id():# Use in message_write and protect user from two similar message
    i = dt.datetime.strftime(datetime_now_obj(), '%y%m%d%H%M')
    return int(i)