# Sessiya_bot: chat_module - Text analysis engine
# Маракулин Андрей @annndruha
# 2019
from data import dictionary as dict
from func import chat_functions as chf

def message_analyzer(user_id,request):
    try:
        request = (request).lower()
        l = len(request)
        if   (l <= 0):
            ans = dict.chat_ans[-1]
        elif (l > 299):
            ans = dict.chat_ans[-2]
        elif (l == 1):
            for keyword in dict.one_letter_word:
                if (request == keyword):
                    ans = dict.one_letter_word[keyword]
                else:
                    ans = dict.chat_ans[0]
        elif (l == 2):
            for keyword in dict.two_letter_word:
                if (request == keyword):
                    ans = dict.two_letter_word[keyword]
                else:
                    ans = dict.chat_ans[0]

        elif ((l > 2) and (l <= 299)):
            ans_exist = 0
            for keyword in dict.answer:
                if (request.find(keyword) >= 0):
                    ans = dict.answer[keyword]
                    ans_exist = 1
            for keyword in dict.functions:
                if (request.find(keyword) >= 0):
                    k = dict.functions[keyword]
                    if k == 0:
                        ans = chf.sessiya_mesage(user_id)
                    if k == 1:
                        ans = chf.set_notify_time(user_id, request)
                    if k == 2:
                        ans = chf.set_exam_date(user_id, request)
                    if k == 3:
                        ans = chf.stop(user_id, request)
                    if k == 4:
                        ans = chf.set_tz(user_id, request)
                    ans_exist = 1
            if ((ans_exist == 0) and (request.find('?') >= 0)):
                ans = dict.random_answer()
            elif ans_exist == 0:
                ans = chf.find_in_wiki(user_id, request)
        return ans

    except:
        print('Chat module: Unknown exception')
        ans = dict.chat_ans[-3]
        return ans