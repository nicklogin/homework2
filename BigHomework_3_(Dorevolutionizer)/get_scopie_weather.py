import re, urllib.request#, derevolutionizer, json, html

def get_weather():
    try:
        urlad = 'https://yandex.ru/pogoda/10463'
        with urllib.request.urlopen(urlad) as p:
            weatherpage = p.read().decode('utf-8')

        reweather = re.compile('<div class="fact">.*?<div class="content__brief">', re.DOTALL)
        retime = re.compile('<time class="time fact__time" .*?>.*?</time>', re.DOTALL)
        retemp = re.compile('<div class="temp fact__temp">.*?</div>', re.DOTALL)
        recond = re.compile('<div class="fact__condition.*?>.*?</div>', re.DOTALL)
        refeels = re.compile('<dl class="term term_orient_h fact__feels-like">.*?</dl>', re.DOTALL)
        reyest = re.compile('<dl class="term term_orient_h fact__yesterday">.*?</dl>', re.DOTALL)
        rewind = re.compile('<dl class="term term_orient_v fact__wind-speed">.*?</dl>', re.DOTALL)
        repress = re.compile('<dl class="term term_orient_v fact__pressure">.*?</dl>', re.DOTALL)
        rehum = re.compile('<dl class="term term_orient_v fact__humidity">.*?</dl>', re.DOTALL)
        output = []

        Scopie_weather = re.search(reweather, weatherpage).group(0)

        for i in (retime, retemp, recond, refeels, reyest, rewind, repress, rehum):
            x = re.sub('<.*?>','',re.search(i, Scopie_weather).group(0))
            x = re.sub('([0-9+-][0-9-%°:,^]+)',' \\1',x)
##            print(x)
            output.append(x)

        output = '<p>Погода в Скопье:</p><p>'+'</p><p>'.join(output)+'</p><p><a href="'+urlad+'">Источник</a></p>'
        output = output.replace('<sup>','').replace('</sup>','').replace('°','<sup>o</sup>')
    except:
        output = 'Не удаётся получить информацию о погоде в Скопье.'
    return output

##def testing_interface():
####    with open ('dorev_dict.json','r',encoding = 'cp1251') as f:
####        d = {k:html.unescape(v).strip(',') for k,v in json.load(f).items()}
####    de = {k:v for k,v in d.items() if ('ѣ' in v) or ('е' in v)}
####    dorevolutionizer = derevolutionizer.Derevolutionizer('C:\Programming\mystem\mystem.exe', dorev_dict = d)
####    print(dorevolutionizer.derevolutionize_text(get_weather()))
##    print(get_weather())
##
##if __name__ == '__main__':
##    testing_interface()




