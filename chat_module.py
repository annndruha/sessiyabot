# Sessiya_bot: chat_module - Text analysis engine
# Маракулин Андрей @annndruha
# 2019
import datebase_functions as dbf
import dictionary as dict
import engine

def chat_module(user_id,request):
    try:
        request = (request).lower()
        ans_exist = 0
        l = len(request)
        if   (l <= 0):
            ans_exist = -1
        elif (l == 1):
            for keyword in dict.one_letter_word:
                if (request == keyword):
                    ans = dict.one_letter_word[keyword]
                    ans_exist = 1
        elif (l == 2):
            for keyword in dict.two_letter_word:
                if (request == keyword):
                    ans = dict.two_letter_word[keyword]
                    ans_exist = 1
        elif (l > 299):
            ans_exist = -2
        elif ((l > 2) and (l <= 299)):
            for keyword in dict.answer:
                if (request.find(keyword) >= 0):
                    ans = dict.answer[keyword]
                    ans_exist = 1
            for keyword in dict.functions:
                if (request.find(keyword) >= 0):
                    k = dict.functions[keyword]
                    if k == 0:
                        ans = engine.sessiya_mesage(user_id)
                    if k == 1:
                        ans = dbf.start(user_id, request)
                    if k == 2:
                        ans = dbf.change(user_id, request)
                    if k == 3:
                        ans = dbf.stop(user_id, request)
                    ans_exist = 1
            if ((ans_exist == 0) and (request.find('?') >= 0)):
                ans = dict.random_answer()
                ans_exist = 1

        if ((l == 1 or l == 2 or l == 3) and ans_exist == 0):
            ans = engine.chat_ans[0]
        elif ans_exist == 0:
            ans = engine.find_in_wiki(request)
        elif ans_exist == 1:
            ans = ans
        else:
            ans = engine.chat_ans[ans_exist]
        return ans

    except:
        print("[" + engine.timestamp() + "] Chat module: Unknown exception")
        ans = engine.chat_ans[-3]
        return ans