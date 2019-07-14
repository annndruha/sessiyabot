import datetime
import random
import dictionary
import wikipedia

from pytz import timezone
wikipedia.set_lang("RU")

def numerals_days(n):
    if ((10<n) and (n<20)):
        return 'äíåé'
    else:
        n = n%10
        if n==0:
            return 'äíåé'
        elif n==1:
            return 'äåíü'
        elif ((n>1) and (n<5)):
            return 'äíÿ'
        elif (n>=5):
            return 'äíåé'

def date_and_time_now():
    return datetime.datetime.strftime(datetime.datetime.now(timezone('Europe/Moscow')), "%d.%m.%Y %H:%M:%S")

def date_now():
    return datetime.datetime.strftime(datetime.datetime.now(timezone('Europe/Moscow')), "%d.%m.%Y")

def time_now():
    return datetime.datetime.strftime(datetime.datetime.now(timezone('Europe/Moscow')), "%H:%M")

def sessiya_mesage(user_id):
    sessiya_begin = "08.06.2019".split('.')
    today = datetime.date.today()


    try:
        f = open('user_list.txt', 'r+')
    except IOError as e:
        result = date_and_time_now()
        print('Íå óäàëîñü îòêðûòü ôàéë '+result+ '  UTC\n')
    else:
        for line in f:
            if (line.find(str(user_id))>=0):
                sessiya_begin = line.split(' ')[1]
                sessiya_begin = sessiya_begin.split('.')
        f.close()



    #days_from_begin = (today-datetime.date(2019,2,7)).days#Ïðè ðàçíèöû äàò ïîëó÷àåòñÿ îñîáûé òèï, èçâëåêàåì èç íåãî äíè


    sessiya_begin = datetime.date(int(sessiya_begin[2]),int(sessiya_begin[1]),int(sessiya_begin[0]))
    days_to_end = (sessiya_begin-today).days

    if days_to_end<=-30:
        return 'Ñåññèÿ óæå ïðîøëà, íàäåþñü òû õîðîøî å¸ ñäàë!'
    elif days_to_end<=0:
        return 'Ñåññèÿ óæå èä¸ò! Òû ìîëîäåö, ÿ â òåáÿ âåðþ è æåëàþ óñïåõà íà ýêçàìåíàõ! &#10084;'
    else:
        return 'Äî áëèæàéøåãî ýêçàìåíà: '+ str(days_to_end) +' '+ numerals_days(days_to_end)# +'\nÓæå ïðîøëî: '+str(days_from_begin*100//(days_from_begin+days_to_end))+'% ñåìåñòðà'


def find_in_wiki(wiki_request):
    try:
        n=2#Ïî óìëî÷àíèþ âîçâðàùàåì äâà ïðåäëîæåíèÿ
        exit = 0

        while ((n<5) and (exit==0)):
            exit = 1
            ans = str(wikipedia.summary(wiki_request, sentences=n, auto_suggest=True))
            if ((ans.rfind('('))>(ans.rfind(')'))):#Èùåì êîíåö ïðåäëîæåíèÿ íå ìåæäó ñêîáêàìè
                n=n+1
                exit = 0
            if len(ans)<100:
                n=n+1
                exit = 0
        if ans.find('=='):
            ans = ans[:(ans.find('==')-1)]


    except wikipedia.exceptions.PageError:
        ans = dictionary.random_not_found[random.randint(1,8)]
    except wikipedia.exceptions.HTTPTimeoutError:
        ans = dictionary.random_not_found[random.randint(1,8)]
    except wikipedia.exceptions.RedirectError:
        ans = dictionary.random_not_found[random.randint(1,8)]
    except wikipedia.exceptions.WikipediaException:
        ans = dictionary.random_not_found[random.randint(1,8)]
    except wikipedia.exceptions.DisambiguationError:
        ans = dictionary.random_not_found[9]
    return ans









