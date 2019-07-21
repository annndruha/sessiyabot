# Functions for work with usres datebase
#Маракулин Андрей @annndruha
#2019

#from engine import va
from dictionary import db_ans

default_exam_date = '04.01.2020'
users_file = 'users.txt'

def validate_user(user_id):
    f = open(users_file)
    lines = f.readlines()
    for line in lines:
        if (line.find(str(user_id)) >= 0):
            user_line = line.split(' ')
            if user_line[3].find('y') >= 0:
               f.close()
               return 'y'
            if user_line[3].find('n') >= 0:
                f.close()
                return 'n'
    f.close()
    return 'e'

def add_line(user_id, new_line):
    f = open(users_file, 'a')
    f.write(new_line + '\n')
    f.close()

def change_date(user_id, date):
    with open(users_file) as f:
        lines = f.read().splitlines()
        for line in lines:
            if (line.find(str(user_id)) >= 0):
                user_line = line.split(' ')
                user_line[1] = date
                lines.remove(line)
        lines.append(' '.join(user_line))
    f = open(users_file,'w')
    f.write('\n'.join(lines))
    f.close()

def change_time(user_id, my_time):
    f = open(users_file)
    lines = f.read().splitlines()
    f.close()
    for line in lines:
        if (line.find(str(user_id)) >= 0):
            user_line = line.split(' ')
            user_line[2] = my_time
            lines.remove(line)
    lines.append(' '.join(user_line))
    f = open(users_file,'w')
    f.write('\n'.join(lines))
    f.close()

def change_flag(user_id):
    f = open(users_file)
    lines = f.read().splitlines()
    f.close()
    for line in lines:
        if (line.find(str(user_id)) >= 0):
            user_line = line.split(' ')
            if (user_line[3] == "n"):
                user_line[3] = "y"
            else:
                user_line[3] = "n"
            lines.remove(line)
    lines.append(' '.join(line_temp))
    f = open(users_file,'w')
    f.write('\n'.join(lines))
    f.close()

def start(user_id, message):
    try:
        new_user_time = (message.split(' '))[1]
        if (validate_time(new_user_time) == False):
            ans = db_ans[incorrect_time]
        else:
            if validate_user(user_id) == 'e':
                s = '{} {} {} y'.format(str(user_id), default_exam_date, new_user_time)
                add_line(user_id, s)
                ans = '{} {} {}'.format(db_ans['start_notify'], new_user_time, db_ans['msk'])
            elif validate_user(user_id) == 'n':
                change_time(user_id,new_user_time)
                change_flag(user_id)
                ans = '{} {} {}'.format(db_ans['start_notify'], new_user_time, db_ans['msk'])
            elif validate_user(user_id) == 'y':
                change_time(user_id, new_user_time)
                ans = '{} {} {}'.format(db_ans['change_time'] , new_user_time, db_ans['msk'])
    except:
        ans = db_ans['not_available']
    return ans

def change(user_id, message):
    try:
        new_user_date = (message.split(' '))[1]
        if (validate_date(new_user_date) == False):
            ans = db_ans['incorrect_date'] + ' ' + default_exam_date
        else:
            if validate_user(user_id) == 'e':
                s = str(user_id) + ' ' + new_user_date + ' 00:00 n'
                add_line(user_id, s)
                ans = db_ans['change_date'] + ' ' + new_user_date
            else:
                change_date(user_id,new_user_date)
                ans = db_ans['change_date'] + ' ' + new_user_date
    except:
        ans = db_ans['not_available']
    return ans

def stop(user_id, message):
    try:
        if validate_user(user_id) == 'e':
            ans = db_ans[4]
        elif validate_user(user_id) == 'n':
            ans = db_ans['unfollow_yet']
        elif validate_user(user_id) == 'y':
            change_flag(user_id)
            ans = db_ans['unfollow']
    except:
        ans = db_ans['not_available']
    return ans