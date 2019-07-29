# Sessiya_bot: datebase_functions - Functions for work with usres datebase
# Маракулин Андрей @annndruha
# 2019
from data import config

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

def check_user(user_id):
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
            if (user_line[3] == 'n'):
                user_line[3] = 'y'
            else:
                user_line[3] = 'n'
            lines.remove(line)
    lines.append(' '.join(user_line))
    write_lines(lines)