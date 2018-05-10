import pymorphy2, json, random
from pymorphy2.tokenizers import simple_word_tokenize as tokenize

class Generator():
    def __init__(self):
        self.analyzer = pymorphy2.MorphAnalyzer()
        with open('dictionary.json','r',encoding='utf-8') as d:
            self.dictionary = json.load(d)
    def get_analysis(self,message):
        return [self.analyzer.parse(token)[0]  for token in tokenize(message)] 
    def reply(self,message):
        message = self.get_analysis(message)
        s = ''
        for i in message:
            try:
                if 'PNCT' in i.tag:
                    s += i.word
                elif 'CONJ' in i.tag or 'PREP' in i.tag:
                    s += ' '+i.word
                else:
                    s += ' '+random.choice(self.dictionary[str(i.tag)])
            except:
                s += ' '+i.word
        return s.capitalize().strip()
            

##def test():
##    g = Generator()
##    while True:
##        s = input()
##        if s.strip()!='exit':
##            print(g.reply(s))
##        else:
##            print('До свидания')
##            break
##
##test()
        
