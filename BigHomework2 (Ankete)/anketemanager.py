import json
import xml.etree.ElementTree as ET
import os, statistics, math
import matplotlib.pyplot as plt
from flask import Flask, url_for, render_template, redirect, request, send_from_directory

def find_index (elem, lst):
    for i in range(len(lst)):
        if lst[i] == elem:
            return i
        else:
            return None
def get_max_img_ind():
    n = -1
    for i in os.listdir('./static'):
        if i.endswith('.png'):
            n += 1
    return n
            
def make_pie(ar, path):
    s = set(ar)
    counts = {str(l):ar.count(l) for l in s}
    plt.figure()
    plt.pie([counts[i] for i in counts], labels = [i+get_val(counts,i) for i in counts])
    plt.savefig(path, bbox_inches = 'tight')

def get_val(d,l):
    s = sum([d[k] for k in d])
    val = '( '+str(round((d[l]/s)* 100,2))+'% )'
    return val

def get_name():
    global c
    c += 1
    return str(c)
    
##def correlation(r1, r2):
##    #считаем лин. коэффициент корреляции Пирсона:
##    r_wo_gaps1 = [r1[i] for i in range(len(r1)) if r1[i]!=None and r2[i]!=None]
##    r_wo_gaps2 = [r2[i] for i in range(len(r1)) if r1[i]!=None and r2[i]!=None]
##    mean1 = statistics.mean(r_wo_gaps1)
##    mean2 = statistics.mean(r_wo_gaps2)
##    a, b, c = 0, 0, 0
##    for i in range(len(r_wo_gaps1)):
##        a += (r_wo_gaps1[i]-mean1)*(r_wo_gaps2[i]-mean2)
##        b += math.pow(r_wo_gaps1[i]-mean1, 2)
##        c += math.pow(r_wo_gaps2[i]-mean2, 2)
##    return a/math.pow(b*c, 0.5)

class anketetext():
    def __init__(self,varlist='variables.json',questionlist='questions.xml',social_parameters='social_parameters.json',jsonpath = 'responses.json',new=False):
        '''параметр new отвечает за то, чтобы создавать новую анкету или продолжать работу со старой'''
        self.jsonpath = jsonpath
        if new or not os.path.exists(jsonpath):
            with open (self.jsonpath, 'w', encoding='utf-8') as f:
               f.write('[]')
        self.questionlist = self.generate_questions(varlist, questionlist)
        with open (social_parameters, 'r', encoding='utf-8') as f:
            self.social_parameters = json.load(f)
        self.all_fields = [j['param'] for j in self.social_parameters]+[i['type'] for i in self.questionlist]

    def generate_questions(self,varlist,questionlist):
        with open (varlist,'r', encoding='utf-8') as x:
            vars = json.load(x)
        qtreeroot = ET.parse(questionlist).getroot()
        questions = []
        for i in qtreeroot:
            d = dict()
            d['question'] = i.text.strip()
            d['type'] = i.attrib['lingvar']+'_'+i.attrib['context']
            d['variants'] = vars[i.attrib['lingvar']]
            questions.append(d)
##        print(questions)
        return questions

    def get_responses_list(self):
        with open (self.jsonpath,'r',encoding='utf-8') as f:
            responses = json.load(f)
        return responses
        
app = Flask(__name__)

@app.route('/')
def startpage():
    if request.args:
        responsedict = {i:None for i in ankete.all_fields}
        for i in request.args:
            if request.args[i]:
                responsedict[i] = request.args[i].lower()
        responses = ankete.get_responses_list()
        responses.append(responsedict)
        f = open(ankete.jsonpath,'w',encoding='utf-8')
        json.dump(responses, f, ensure_ascii = False, indent = 4)
        f.close()
        return redirect('/thank_you')
    return render_template('index.html', questions = ankete.questionlist, soc_params = ankete.social_parameters)

@app.route('/thank_you')
def thanksgiving_page():
    return render_template('thank_you.html')

@app.route('/search')
def search():
    if request.args:
        return redirect(url_for('results', field = request.args['field'], value = request.args['value']))
    return render_template('search.html', fields = ankete.all_fields)

@app.route('/results')
def results():
    if request.args:
        responselist = []
        with open (ankete.jsonpath, 'r', encoding = 'utf-8') as x:
            allresults = json.load(x)
        if allresults:
            for i in allresults:
                if request.args['value'] in i[request.args['field']]:
                    responselist.append(i)
            return render_template('results.html', selection = responselist, fields = ankete.all_fields)
        else:
            return render_template('no_results.html')

@app.route('/stats')
def calculate_stats():
    global c
    with open (ankete.jsonpath, 'r', encoding = 'utf-8') as x:
        allresults = json.load(x)
    if allresults:
        intvalues = dict()
        qual_discr_values = dict()
        for i in ankete.social_parameters:
            if i['type'] == 'integer':
                x = []
                for j in allresults:
                    try:
                        x.append(int(j[i['param']]))
                    except:
                        x.append(None)
                intvalues[i['param']] = x
        
        numeric_chars = []
        for i in intvalues:
            row = [j for j in intvalues[i] if j!=None]
            if row:
                numeric_chars.append({'name':i,'q':len(row),'mean':round(statistics.mean(row),2),'harm':round(statistics.harmonic_mean(row),2),'median':round(statistics.median(row),2),
                                      'dev':round(statistics.pstdev(row),2),'var':round(statistics.pvariance(row),2)})
        pics = []
        for i in ankete.all_fields:
            if i not in intvalues:
                row = [j[i] for j in allresults]
                picname = get_name()+'.png'
                make_pie(row, './static/'+picname)
                pics.append((i, picname))
        c += 1
        return render_template('statistics.html', rowchars = numeric_chars, pictures = pics)
    else:
        return render_template('no_results.html')

@app.route('/json')
def send_json():
    ##да, здесь json некрасивый и неформатированный, зато он обновляется
    ##после каждого запроса, а не только при перезапуске сервера:
    with open (ankete.jsonpath,'r',encoding='utf-8') as x:
        f = x.read()
    return f

if __name__ == '__main__':
    c = get_max_img_ind()
    ankete = anketetext(new = True)
    app.run()
