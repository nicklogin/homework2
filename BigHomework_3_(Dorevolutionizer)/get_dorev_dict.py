import urllib.request
import re, html, json

def get_definition(word, article):
    if ' ' in article:
        output = article[:article.find(' ')]
    else:
        output = article
    if word == 'я':
        output = output.lower()
    abbr = re.search('[А-Я]\..*[А-Я]\.',article)
    if abbr:
        output = abbr.group(0)
        print(word, output)
    return output
    
address = 'http://www.dorev.ru/ru-index.html?l='
re_word = re.compile('<td class="uu">[а-яА-ЯёЁ]+?</td><td></td><td class="uu">.*?</td>')

pageindices = [hex(i).split('x')[1] for i in range(16*12,16*14)]

allarticles = []

for index in pageindices:
    page = address+index
    f = urllib.request.urlopen(page).read().decode('cp1251')
    allarticles += re.findall(re_word ,f)
    print(page+' - ok!')

allarticles = '\n'.join(allarticles)
allarticles = re.sub('</td><td></td>',':',allarticles)
allarticles = re.sub('<.*?>','',allarticles)

with open ('dorev_articles1.txt','w',encoding='cp1251') as t:
    t.write(allarticles)

allarticles = allarticles.split('\n')
allarticles = [i.replace("'","").split(':') for i in allarticles]
try:
    allarticles = {i[0]:get_definition(i[0],i[1]) for i in allarticles}
except:
    raise Error

##for i in allarticles:
##    print(i, html.unescape(allarticles[i]))

with open ('dorev_dict1.json','w',encoding='cp1251') as x:
    json.dump(allarticles,x,ensure_ascii = False, indent = 4)




    
    

    
