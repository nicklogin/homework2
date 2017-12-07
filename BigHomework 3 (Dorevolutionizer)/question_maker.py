import random
##import json

def make_questions(dorev_edict):
    keys =  random.sample(dorev_edict.keys(), 10)
    output = []
    c = 0
    for i in keys:
        c += 1
        wrong = dorev_edict[i]
        if 'ѣ' in wrong:
            wrong = wrong.replace('ѣ','e',1)
        else:
            wrong = wrong.replace('е','ѣ',1)
##        print(dorev_edict[i], wrong)
        question = [{'option':dorev_edict[i],'value':'1'},{'option':wrong, 'value':'0'}]
        random.shuffle(question)
        question.append(dorev_edict[i])
        output.append(question)
    return output
   
##def testing_interface():
##    with open ('dorev_dict.json','r',encoding = 'cp1251') as f:
##        d = {k:html.unescape(v).strip(',') for k,v in json.load(f).items()}
##    d = {k:v for k,v in d.items() if ('ѣ' in v) or ('е' in v)}
##    questions = make_questions(d)
##    print(questions)
##
##if __name__ == '__main__':
##    testing_interface()
    
        
