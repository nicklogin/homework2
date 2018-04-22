from flask import Flask, url_for, render_template, redirect, request
import html, json
import derevolutionizer, question_maker
import get_scopie_weather
##scopie_weather = dorevolutionizer.derevolutionize_text(get_scopie_weather.get_weather())

def calculate_result(answers):
    result = dict()
    result["mark"] = len([i for i in answers if answers[i] == '1'])
    if result["mark"]<4:
        result['comment'] = 'Не огорчайтесь, но вамъ необходимо подучить дореволюцiонную орѳографiю.'
    elif result["mark"]<7:
        result["comment"] = 'Вы  - заправскiй гимназистъ!'
    elif result["mark"]<9:
        result["comment"] = 'Вы - коллежскiй асессоръ!'
    elif result["mark"]<11:
        result["comment"] = 'Вы - Государь-императоръ!'
    result["mark"] = str(result['mark'])
    return result
    
with open ('dorev_dict.json','r',encoding = 'cp1251') as f:
    d = {k:html.unescape(v).strip(',') for k,v in json.load(f).items()}
de = {k:v for k,v in d.items() if ('ѣ' in v) or ('е' in v)}
dorevolutionizer = derevolutionizer.Derevolutionizer('C:\Programming\mystem\mystem.exe', dorev_dict = d)
old_text = 'Введите текстъ здѣсь...'
new_text = 'Ничего не введено'

app = Flask(__name__)

@app.route('/')
def dorevolutionizer_page(old = old_text, new = new_text):
    if request.args:
        old = request.args['old_text']
        new = dorevolutionizer.derevolutionize_text(request.args['old_text'])
    return render_template('index.html', old_text = old, new_text = new, scopie_weather = dorevolutionizer.derevolutionize_text(get_scopie_weather.get_weather()))

@app.route('/test')
def test():
    if request.args:
        return redirect(url_for('results',result = calculate_result(request.args)))
    return render_template('quiz.html', questions = question_maker.make_questions(de))

@app.route('/results')
def results():
    if request.args:
        result = request.args['result'].replace("'",'"')
        print(result, type(result))
        result = json.loads(result)
        return render_template('results.html', result = result)
    return render_template('no_results.html', message = 'Чтобы посмотрѣть результаты, пройдите тестъ, доступный по кнопкѣ "Провѣрь себя"')

@app.route('/analysis')
def analysis(url0 = 'https://lenta.ru/'):
    if request.args:
        url0 = request.args['asked_url']
    analyzis = dorevolutionizer.analyse_page(url0)
    print(analyzis)
    return render_template('analysis.html', topten = analyzis['topten'], wordlist = analyzis['words'], asked_url = url0)

if __name__ == '__main__':
    app.run()
