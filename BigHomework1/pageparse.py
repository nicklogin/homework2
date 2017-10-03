import re, urllib.request, html

def getmeta(page, url):
    '''Input - html code of the page, page url;
Output - page metadata dict'''
    metadata = dict()
    metadata['path'] = url.split('/')
    metadata['path'] = metadata['path'][len(metadata['path'])-1]
    metadata['path'] = metadata['path'][:metadata['path'].find('.html')]+'.txt'
    try:
        metadata['author'] = re.search(r'<p>([А-Я]\w+ [А-Я]\w+)</p><br>',page).group(1)
    except:
        metadata['author'] = ''
    metadata['sex'] = ''
    metadata['birthday'] = ''
    metadata['header'] = re.search('<meta property="og:title" content="(.*?)" />',page).group(1)
    try:
        metadata['created'] = re.search(r'<span class="pull-right date">(.*?)</span>', page).group(1) #индекс в возвр. массиве - 5
        metadata['day'], metadata['month'], metadata['publ_year'] = metadata['created'].split('.')
        metadata['month']=str(int(metadata['month']))
    except:
        metadata['created'], metadata['day'], metadata['month'], metadata['publ_year'] = '','','',''
    metadata['path'] = 'газета/plain/'+metadata['publ_year']+'/'+metadata['month']+'/'+metadata['path']
    metadata['sphere'] = 'публицистика'
    metadata['genre_fi'] = ''
    metadata['type'] = ''
    try:
        metadata['topic'] = re.search(r'Другие материалы по теме &laquo;(.*?)&raquo;',page).group(1)
    except:
        metadata['topic'] = ''
    metadata['chronotop'] = ''
    metadata['style'] = 'нейтральный'
    metadata['audience_age'] = 'н-возраст'
    metadata['audience_level'] = 'н-уровень'
    metadata['audience_size'] = 'республиканская'
    metadata['source'] = url
    metadata['publication'] = 'Деловая газета.ЮГ'
    metadata['publisher'] = ''
    metadata['medium'] = 'газета'
    metadata['country'] = 'Россия'
    metadata['region'] = 'Краснодарский край'
    metadata['language'] = 'ru'
    return metadata

def html_save_text(code, outputfile, meta):
    '''save plain text of a webpage as a text file with some meta information'''
    reArticleText = re.compile(r'<span class="data">(.*?)<div class="responsive-banner">', re.DOTALL)
    try:
        code = re.search(reArticleText, code).group(1)
    except:
        code = code
    regTag = re.compile(r'<.*?>', re.DOTALL)
    regStyle = re.compile(r'<style.*?>.*?</style>', re.DOTALL)
    regScript = re.compile(r'<script.*?>.*?</script>', re.DOTALL)
    code = regScript.sub('',code)
    code = regStyle.sub('',code)
    code = regTag.sub('',code)
    code = html.unescape(code)
    with open(outputfile,'w',encoding = 'utf-8') as f:
        if meta['author']:
            f.write('@au '+meta['author']+'\n')
        else:
            f.write('@au Noname'+'\n')
        f.write('@ti '+meta['header']+'\n')
        f.write('@da '+meta['created']+'\n')
        f.write('@topic '+meta['topic']+'\n')
        f.write('@url '+meta['source']+'\n')
        f.write(code)

def get_meta_startline():
    '''return array of metadata columns'''
    ln = 'path,author,sex,birthday,header,created,sphere,genre_fi,type,topic,chronotop,style,audience_age,audience_level,audience_size,source,publication,publisher,publ_year,medium,country,region'
    ln += ',language'
    return ln.split(',')

##if __name__ == '__main__':
##    pagead = r'http://www.dg-yug.ru/rubriki/world/88222-kto-s-kem-suditsya-v-krasnodarskom-krae-25-oktyabrya.html'
##    with urllib.request.urlopen(pagead) as p:
##        htmlcode = p.read().decode('utf-8')
##    meta = getmeta(htmlcode,pagead)
##    for i in meta:
##        print(i,':',meta[i])
##    print(get_meta_startline())
##    print ('\t'.join((get_meta_startline())))
##    html_save_text(htmlcode,'./статья.txt',meta)   
