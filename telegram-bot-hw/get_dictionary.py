import pymorphy2, json
from pymorphy2.tokenizers import simple_word_tokenize

def analyze(x):
    analysis = analyser.parse(x)[0]
    return (str(analysis.tag),analysis.word)

analyser = pymorphy2.MorphAnalyzer()

output_path = 'dictionary.json'

input_path = '1grams-3.txt'

with open(input_path,'r',encoding='utf-8') as f:
    raw_input = f.read()

print('raw text loaded')
text = [i.split('\t')[1] for i in raw_input.splitlines() if i]
print('text tokenized')
tokens = [analyze(i) for i in text]
print('text analyzed')

all_tags = set(i[0] for i in tokens)

dictionary = {i:list(set(j[1] for j in tokens if j[0]==i)) for i in all_tags}

print('dictionary generated')
print('dumping into json...')
with open(output_path,'w',encoding='utf-8') as out:
    json.dump(dictionary,out,ensure_ascii=False,indent=4)


