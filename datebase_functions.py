# Sessiya_bot: datebase_functions - Functions for work with usres datebase
# Маракулин Андрей @annndruha
# 2019
import config
import engine
from dictionary import db_ans

# Lines + file = love
def get_lines():
    with open(config.users_file) as f:
        lines = f.read().splitlines()
    return lines

def add_line(new_line):
    with open(config.users_file, 'a') as f:
        f.write('\n' + new_line)

def write_lines(lines):
    with open(config.users_file, 'w') as f:
        f.write('\n'.join(lines))

def validate_user(user_id):
    for line in get_lines():
        if (line.split(' ')[0] == str(user_id)):
            user_line = line.split(' ')
            if user_line[3] == 'y':
                return 'y'
            if user_line[3] == 'n':
                return 'n'
    return 'e'

# Change user data functions
def change_date(user_id, new_date):
    lines = get_lines()
    for line in lines:
        if (line.split(' ')[0] == str(user_id)):
            user_line = line.split(' ')
            user_line[1] = new_date
            lines.remove(line)
    lines.append(' '.join(user_line))
    write_lines(lines)

def change_time(user_id, new_time):
    lines = get_lines()
    for line in lines:
        if (line.split(' ')[0] == str(user_id)):
            user_line = line.split(' ')
            user_line[2] = new_time
            lines.remove(line)
    lines.append(' '.join(user_line))
    write_lines(lines)

def change_flag(user_id):
    lines = get_lines()
    for line in lines:
        if (line.split(' ')[0] == str(user_id)):
            user_line = line.split(' ')
            if (user_line[3] == "n"):
                user_line[3] = "y"
            else:
                user_line[3] = "n"
            lines.remove(line)
    lines.append(' '.join(user_line))
    write_lines(lines)

def start(user_id, message):# Start notify message from user
    try:
        new_user_time = (message.split(' '))[1]
        if (engine.validate_time(new_user_time) == False):
            ans = db_ans[incorrect_time]
        else:
            if validate_user(user_id) == 'e':
                s = '{} {} {} y'.format(str(user_id), config.default_exam_date, new_user_time)
                add_line(s)
                ans = db_ans['start_notify'] + ' ' + new_user_time + ' ' + db_ans['msk']
            elif validate_user(user_id) == 'n':
                change_time(user_id,new_user_time)
                change_flag(user_id)
                ans = db_ans['start_notify'] + ' ' + new_user_time + ' ' + db_ans['msk']
            elif validate_user(user_id) == 'y':
                change_time(user_id, new_user_time)
                ans = db_ans['change_time'] + ' ' + new_user_time + ' ' + db_ans['msk']
    except:
        print('[' + engine.timestamp() + '] DBFunctions: Start: Exception')
        ans = db_ans['not_available']
    return ans

def change(user_id, message):# Change notify message from user
    try:
        new_user_date = (message.split(' '))[1]
        if (engine.validate_date(new_user_date) == False):
            ans = db_ans['incorrect_date'] + ' ' + config.default_exam_date
        else:
            if validate_user(user_id) == 'e':
                s = str(user_id) + ' ' + new_user_date + ' 00:00 n'
                add_line(s)
                ans = db_ans['change_date'] + ' ' + new_user_date
            else:
                change_date(user_id,new_user_date)
                ans = db_ans['change_date'] + ' ' + new_user_date
    except:
        print('[' + engine.timestamp() + '] DBFunctions: Change: Exception')
        ans = db_ans['not_available']
    return ans

def stop(user_id, message):# Stop notify message from user
    try:
        if validate_user(user_id) == 'e':
            ans = db_ans['no_sub']
        elif validate_user(user_id) == 'n':
            ans = db_ans['unfollow_yet']
        elif validate_user(user_id) == 'y':
            change_flag(user_id)
            ans = db_ans['unfollow']
    except:
        print('[' + engine.timestamp() + '] DBFunctions: Stop: Exception')
        ans = db_ans['not_available']
    return ans