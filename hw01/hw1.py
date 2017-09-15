import urllib.request
import re

with urllib.request.urlopen('http://www.dg-yug.ru/') as p:
    htmlcode = p.read().decode('utf-8')
h = re.compile('<a class="title".*?>[\s\S]*?</a>', re.DOTALL)
h1 = re.compile('(Сегодня)|(Вчера).*?</span>(.*?)<\a>', re.DOTALL)
heads = h.findall(htmlcode) + [i[2] for i in h1.findall(htmlcode)]
regTag = re.compile('<.*?>', re.DOTALL)
regSpace = re.compile('\s{2,}', re.DOTALL)

with open ('headings.txt','w', encoding = 'utf-8') as f:
    for i in heads:
        j = regSpace.sub("",i)
        j = regTag.sub("",j)
        if j != '':
            print(j)
            f.write(j+'\n')
