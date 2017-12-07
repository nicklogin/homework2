import json, re, urllib.request
##import html
import os

##предполагается, что пользователь
##вводит текст, соблюдая правила орфографии и пунктуации

class Derevolutionizer():
    def __init__(self, mystem_path, dorev_dict):
        self.mystem_path = mystem_path
        self.output_path = os.getcwd()+"\parsed.json"
        self.input_path = os.getcwd()+"\plaintext.txt"
        self.dictionary = dorev_dict
        self.dictionary = {k.lower():v for k,v in self.dictionary.items()}
        self.consonants = 'цкнгшщзхфвпрлджчсмтб'
        self.silent_consonants = 'цкшщхфпчст'
        self.vowels = 'аиуеоыиоэюяёѣй'
        self.before_vowel = re.compile('(и)(['+self.vowels+'])')
        self.cyril_text = re.compile('[а-яА-ЯёЁ]+')
##        self.retag = re.compile('<.*?>', re.DOTALL)
##        self.rescript = re.compile('<script.*?>.*?</script>', re.DOTALL)
##        self.restyle = re.compile('<style.*?>.*?</style>', re.DOTALL)

    def derevolutionize(self, lemma):
        if lemma in self.dictionary:
            return self.dictionary[lemma].lower()
        else:
            return ''

    def postprocess_form(self, form):
        bv = re.search(self.before_vowel, form)
        if bv is not None:
            bv = bv.group(2)
            form = re.sub(self.before_vowel,'i'+bv,form)
        if form[len(form)-1] in self.consonants:
            form = form+'ъ'
        return form

    def sfpl(self, analysed_token):
##        print(analysed_token)
        if 'analysis' in analysed_token and analysed_token['analysis']:
            lemma = analysed_token['analysis'][0]['lex']
            gr = analysed_token['analysis'][0]['gr']
            if gr.startswith('S') and (('жен' in gr) or ('сред' in gr)) and ('мн' in gr):
                return True
            elif 'мн' in gr.split('=')[0]:
                if lemma.endswith('и'):
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def restore_case(self, a, b):
        if b.isupper():
            a = a.upper()
        elif b.islower():
            a = a.lower()
        elif b.istitle():
            a = a.capitalize()
        return a

    def derevolutionize_text(self, text):
        derevolutionized = ''
        parsed = []
        with open(self.input_path,'w',encoding='utf-8') as f:
            f.write(text)
        command = self.mystem_path+' -i -c -d --format json '+self.input_path+' '+self.output_path
        print(command)
        os.system(command)
        with open ('parsed.json','r',encoding='utf-8') as f:
            for line in f:
                parsed += json.loads(line)            
##        print('analysis performed: '+text)
        for i in range(len(parsed)):
            token = parsed[i]['text'].lower()
            if 'analysis' in parsed[i] and parsed[i]['analysis']:
##                print(parsed[i])
                lemma = parsed[i]['analysis'][0]['lex']
                gr = parsed[i]['analysis'][0]['gr']
                dorev_lemma = self.derevolutionize(lemma)
                if dorev_lemma:
                    token = list(token.lower())
                    if ('ф' in lemma) or ('е' in lemma) or ('и' in lemma):
                        iter_lim = min(len(dorev_lemma), len(token))
                        for j in range(iter_lim):
                            if dorev_lemma[j] == 'ѳ' and token[j] == 'ф':
                                token[j] = 'ѳ'
                            elif dorev_lemma[j] == 'ѵ' and token[j] == 'и':
                                token[j] = ''
                            elif dorev_lemma[j] == 'ѣ' and token[j] == 'е':
                                token[j] = 'ѣ'
                    token = ''.join(token)
                elif token.startswith('бес') and token!='бес' and token[3] in self.silent_consonants:
                    token = 'без'+token[3:]
                elif token.startswith('чрес') and token[4] in self.silent_consonants:
                    token = 'чрез'+token[4:]
                elif token.startswith('черес') and token[5] in self.silent_consonants:
                    token = 'через'+token[5:]   
                if gr.startswith('S') and ('ед' in gr) and (('дат' in gr) or ('пр' in gr)) and token[-1] == 'е':
                    token = token[:-1]+'ѣ'
                elif (gr.startswith('A') or (gr.startswith('V') and 'прич' in gr)) and ('мн' in gr)\
                     and ((i>1 and self.sfpl(parsed[i-2]))or (i<len(parsed)-2 and self.sfpl(parsed[i+2]))):
##                    print(token)
                    if token.endswith('е'):
                        token = token[:-1]+'я'
                    elif token.endswith('иеся'):
                        token = token[:-4]+'ияся'
                if not 'сокр' in gr:
                    token = self.postprocess_form(token)
            token = self.restore_case(token,parsed[i]['text'])
            derevolutionized += token
        return derevolutionized.strip('\n')

    def analyse_page(self, urladdr):
        succeed_to_open = True
        try:
            with urllib.request.urlopen(urladdr) as p:
                derevol_page = p.read().decode('utf-8')
        except:
            succeed_to_open = False
        if succeed_to_open:
##            derevol_page = re.sub(self.rescript, '', derevol_page)
##            derevol_page = re.sub(self.restyle, '', derevol_page)
##            derevol_page = re.sub(self.retag, '', derevol_page)
            derevol_page = ','.join(re.findall(self.cyril_text,derevol_page))
            derevol_page = self.derevolutionize_text(derevol_page)
            topten = self.get_topten(derevol_page.split(','))
            return {'topten':topten,'words':derevol_page}
        else:
            return {'topten':'','words':'Приносимъ свои извиненiя, но дореволюцiонизировать можно только существующiя страницы въ кодировкѣ УТФ-8'}

    def get_topten(self, lst):
        wordset = set(lst)
        worddict = {i:lst.count(i) for i in wordset}
        output = ','.join(sorted(worddict, key = lambda m: -abs(worddict[m]))[:10])
        return output
                                                           
##def testing_interface():
##    with open ('dorev_dict.json','r',encoding='cp1251') as f:
##        d = {k:html.unescape(v).strip(',') for k,v in json.load(f).items()}
##    dorevolutionizer = Derevolutionizer(mystem_path = 'C:\Programming\mystem\mystem.exe', dorev_dict = d)
##    s = input()
##    while s != 'stop':
##        s = dorevolutionizer.analyse_page(s)
##        print(s['topten']+' ; '+s['words'][:100])
##        s = input()
##
##if __name__ == '__main__':
##    testing_interface()
