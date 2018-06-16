
# coding: utf-8

# In[2]:


import random
import pandas
import re
import html


# In[ ]:


class MarkoffTrigramBot():
    def __init__(self,model,reply_len):
        self.re_token = re.compile(u"[a-zA-Z0-9-]+'?|[.,:;?!]+")
        self.df = pandas.read_csv(model)
        self.tokenize = lambda x: self.re_token.findall(x)
        self.reply_len = reply_len
        if reply_len<3:
            print('Invalid argument - reply_len must be more or equal to 3.')
            raise Exception
    def reply(self, message):
        message = html.unescape(message)
        message = self.tokenize(message)[-2:]
        reply = ''
        if len(message)>=2:
            freqs = self.df.loc[(self.df['word1']==message[-2])&(self.df['word2']==message[-1])]
            if freqs.values.size>0:
                max_freq = freqs.max()['frequency']
                # print(max_freq)
                idx = random.choice(freqs.loc[freqs['frequency']==max_freq].index)
                trigram = self.df.loc[idx]
                reply += trigram['word3']
            else:
                message.pop(0)
        if len(message)==1:
            freqs = self.df.loc[self.df['word1']==message[-1]]
            if freqs.values.size>0:
                max_freq = freqs.max()['frequency']
                idx = random.choice(freqs.loc[freqs['frequency']==max_freq].index)
                trigram = self.df.loc[idx]
                reply += ' '+trigram['word2']+' '+trigram['word3']
            else:
                message.pop(0)
        if len(message)==0:
            trigram = self.df.loc[random.choice(self.df.index)]
            # print(trigram)
            reply += trigram['word1']+' '+trigram['word2']+' '+trigram['word3']
        for i in range(0,self.reply_len):
            freqs = self.df.loc[(self.df['word1']==trigram['word2'])&(self.df['word2']==trigram['word3'])]
            ##Если нужные триграммы нашлись:
            if freqs.values.size > 0:
                max_freq = freqs.max()['frequency']
                ##если есть несколько триграмм с максимальной частотой, выбираем из них
                ##случайную
                idx = random.choice(freqs.loc[freqs['frequency']==max_freq].index)
                trigram = self.df.loc[idx]
                reply += ' '+trigram['word3']
            ##Если не нашлись:
            else:
                ##Пробуем найти триграмму, начинающуюся с последнего слова предыдущей:
                freqs = self.df.loc[self.df['word1']==trigram['word3']]
                if freqs.values.size > 0:
                    max_freq = freqs.max()['frequency']
                    ##если есть несколько триграмм с максимальной частотой, выбираем из них
                    ##случайную
                    idx = random.choice(freqs.loc[freqs['frequency']==max_freq].index)
                    trigram = self.df.loc[idx]
                    reply += ' '+trigram['word2']+' '+trigram['word3']
                ##Иначе берём рандомную триграмму:
                else:
                    trigram = self.df.loc[random.choice(self.df.index)]
                    reply += ' '+trigram['word1']+' '+trigram['word2']+' '+trigram['word3']
        # print(reply[0])
        reply = reply.replace(' .','.').lstrip(".?!").strip()
        # print(reply)
        return reply
                    
class testReplier():
    def __init__(self):
        pass
    def reply(self,message):
        # print(message)
        # return "Hello"
        return message