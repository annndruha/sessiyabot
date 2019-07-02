import datetime

def validate_date(date_text):
    try:
        if date_text != datetime.datetime.strptime(date_text, "%d.%m.%Y").strftime('%d.%m.%Y'):
            raise ValueError
        return True
    except ValueError:
        return False

def validate_time(time_text):
    try:
        if time_text != datetime.datetime.strptime(time_text, "%H:%M").strftime('%H:%M'):
            raise ValueError
        return True
    except ValueError:
        return False

def validate_file():
    try:
        f = open('user_list.txt', 'r+')
    except IOError as e:
        return False
    else:
        return True
        f.close()

def validate_user(user_id):
    lines = open('user_list.txt').read().splitlines()
    found=0
    for line in lines:
        if (line.find(str(user_id))>=0):
            found=1
            if line.find('y')>=0:
                return 'y'
            if line.find('n')>=0:
                return 'n'
    if found!=1:
        return 'e'

def add_line(user_id, new_line):
    lines = open('user_list.txt').read().splitlines()
    lines.append(new_line)
    open('user_list.txt','w').write('\n'.join(lines))

def change_date(user_id, date):
    lines = open('user_list.txt').read().splitlines()
    line_temp=''
    for line in lines:
        if (line.find(str(user_id))>=0):
            line_temp=line.split(' ')
            line_temp[1]=date
            lines.remove(line)
    lines.append(' '.join(line_temp))
    open('user_list.txt','w').write('\n'.join(lines))

def change_time(user_id, my_time):
    lines = open('user_list.txt').read().splitlines()
    line_temp=''
    for line in lines:
        if (line.find(str(user_id))>=0):
            line_temp=line.split(' ')
            line_temp[2]=my_time
            lines.remove(line)
    lines.append(' '.join(line_temp))
    open('user_list.txt','w').write('\n'.join(lines))

def change_flag(user_id):
    lines = open('user_list.txt').read().splitlines()
    line_temp=''
    for line in lines:
        if (line.find(str(user_id))>=0):
            line_temp=line.split(' ')
            st=str(user_id)+" change flag from " +line_temp[3]
            if (line_temp[3]=="n"):
                line_temp[3]="y"
            else:
                line_temp[3]="n"
            st+=" to " + line_temp[3]
            print(st)
            lines.remove(line)

    lines.append(' '.join(line_temp))#после того как цикл завершился добавить новую линию чтобы на неё снова не попасть
    open('user_list.txt','w').write('\n'.join(lines))

def start(user_id, message):
    if (validate_file()==True):
        if (len(message.split(' '))==2):
            user_time=(message.split(' '))[1]
            if (validate_time(user_time)==True):
                if validate_user(user_id)=='e':
                    s=str(user_id)+' '+ '08.06.2019'+' '+user_time+' y'
                    add_line(user_id, s)
                    ans="Вы будете получать напоминания о сессии ежедневно в "+ user_time+" мск"
                elif validate_user(user_id)=='n':
                    change_time(user_id,user_time)
                    change_flag(user_id)
                    ans="Вы будете получать напоминания о сессии ежедневно в "+ user_time+" мск"
                elif validate_user(user_id)=='y':
                    change_time(user_id, user_time)
                    ans="Время напоминаний изменено на: "+ user_time+" мск"
            else:
                ans = "Некорректный формат времени для ежедневных напоминаний, правильный пример:\n/start 07:30"
        else:
            ans = "Некорректный формат ввода для ежедневных напоминаний, правильный пример:\n/start 07:30"
    else:
        ans='К сожалению, действие временно недоступно'
    return ans


def change(user_id, message):
    if (validate_file()==True):
        if (len(message.split(' '))==2):
            user_date=(message.split(' '))[1]
            if (validate_date(user_date)==True):
                if validate_user(user_id)=='e':
                    s=str(user_id)+' '+user_date+' '+'00:00'+' n'
                    add_line(user_id, s)
                    ans="Дата ближайшего экзамена изменена на: "+ user_date
                elif validate_user(user_id)=='n':
                    change_date(user_id,user_date)
                    ans="Дата ближайшего экзамена изменена на: "+ user_date
                elif validate_user(user_id)=='y':
                    change_date(user_id,user_date)
                    ans="Дата ближайшего экзамена изменена на: "+ user_date
            else:
                ans="Некорректный формат даты, правильный пример:\n/change 03.06.2019"
        else:
            ans = "Некорректный формат ввода, правильный пример:\n/change 03.06.2019"
    else:
        ans='К сожалению, действие временно недоступно'
    return ans

def stop(user_id, message):
    if (validate_file()==True):
        if validate_user(user_id)=='e':
            ans = "Вы ещё не подписались на напоминания, чтобы от них отписываться :)"
        elif validate_user(user_id)=='n':
            ans = "Вы уже отписались от напоминаний, чтобы снова подписаться воспользуйтесь командой: /start чч:мм"
        elif validate_user(user_id)=='y':
            change_flag(user_id)
            ans = "Я больше не буду присылать вам напоминания о сессии. Надеюсь у вас всё получится и без меня!"
    else:
        ans='К сожалению, действие временно недоступно'
    return ans