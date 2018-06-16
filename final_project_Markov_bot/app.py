from flask import Flask, redirect, render_template, request
import StarTrekBot

replier = StarTrekBot.MarkoffTrigramBot('trigram_frequencies.csv',12)
app = Flask(__name__)

@app.route('/askBot', methods = ['GET'])
def handle_request():
    if request.method == 'GET':
        if request.args:
            # print(request.args["text"])
            return replier.reply(request.args["text"])
        else:
            return redirect('/')
    else:
        return redirect('/')

@app.route('/')
def show_chat_page():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()