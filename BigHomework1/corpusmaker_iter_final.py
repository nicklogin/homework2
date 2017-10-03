import pageparse
import re, urllib.request, urllib.parse, os, random, dirmaker, time

class corpora:
    def __init__(self, start_page, site_name, articles_number = 1200):
        dirmaker.mkdirs_by_month(2007, 2017, r'./газета/plain/')
        self.art_nmb = articles_number #ограничение сверху на число статей в корпусе
        self.site_name = site_name
        self.metadata = []
        self.getallpages(start_page)

    def getallpages(self, start_page):
        regurl = re.compile(r'<div class="col-sm-9">.*?<a.*?href="(.*?)">', re.DOTALL)
        regcat = re.compile(r'<li>.*?<a.*?href="(rubriki.*?/.*?/).*></li>')
        regpagesnmb = re.compile(r'<a href="rubriki/.*?/?page=([0-9]+)">Последняя</a>')
        htmlcode = getpage(start_page)
        allcats = set(re.findall(regcat,htmlcode))
        artcount = 0
        for i in allcats:
            catad = self.site_name + i
            htmlcode = getpage(catad)
            try:
                pgnmb = int(re.search(regpagesnmb,htmlcode).group(1))
            except:
                continue
            for j in range(1, pgnmb+1):
                htmlcode = getpage(catad + '?page=' + str(j))
                urls = re.findall(regurl,htmlcode)
                if urls:
                    for k in urls:
                        articlead = get_readable_ad(self.site_name + k)
                        htmlcode = getpage(articlead)
                        meta = pageparse.getmeta(htmlcode,articlead)
                        if meta['created']: #исключаем статьи с непроставленной датой
                            artcount += 1 #считаем все загруженные статьи
                            print(artcount)
                            self.metadata.append(meta)
                            pageparse.html_save_text(htmlcode, meta['path'], meta)
                        if artcount >= self.art_nmb:
                            break
                if artcount >= self.art_nmb:
                    break
            if artcount >= self.art_nmb:
                print('corpora_loaded')
                break
            

    def write_meta(self, path_for_meta):
        meta_head = pageparse.get_meta_startline()
        with open(path_for_meta,'w', encoding = 'utf-8') as m:
            m.write('\t'.join(meta_head)+'\n')
            for line in self.metadata:
                new_line = '\t'.join([line[i] for i in meta_head])
                m.write(new_line+'\n')
                            
def getpage(url):
    print(url)
    with urllib.request.urlopen(url) as s:
        h = s.read().decode('utf-8')
    return h

def get_readable_ad(url):
    new_add = url.split('/')
    new_add[len(new_add)-1] = urllib.parse.quote(new_add[len(new_add)-1])
    new_add = '/'.join(new_add)
    return new_add
                   
if __name__ == '__main__':
    my_corp = corpora('http://www.dg-yug.ru/rubriki/','http://www.dg-yug.ru/')
    my_corp.write_meta('./газета/metadata.csv')
    
