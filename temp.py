

def validate_user(user_id):
    f=open('user_list.txt')
    lines = f.readlines()
    for line in lines:
        if (line.find(str(user_id))>=0):
            user_line=line.split(' ')
            if user_line[3].find('y')>=0:
               f.close()
               return 'y'
            if user_line[3].find('n')>=0:
                f.close()
                return 'n'
    f.close()
    return 'e'


print(validate_user(478143147))