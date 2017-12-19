import sqlite3
import matplotlib.pyplot as plt

def create_bar(counts, path):
    ds = get_ds(counts)
    plt.bar(ds, height=[counts[i] for i in counts], tick_label=[i for i in counts])
    plt.savefig(path, bbox_inches='tight')
    plt.show()

def get_ds(x):
    c = 0
    output = []
    for i in x:
        c += len(i)
        output.append(c)
    return output

def get_counts(query_list,val_list=[]):
    if val_list:
        return {i:query_list.count(i) for i in val_list}
    else:
        s = set(query_list)
        return {i:query_list.count(i) for i in s}

def get_bar(values, c, path):
    occurences = []
    for val in values:
        c.execute('SELECT * FROM words_and_glosses INNER JOIN glosses ON words_and_glosses.gloss_id = glosses.id WHERE glosses.gloss = "'+val+'"')
        occurences += [i[3] for i in c.fetchall()]
    create_bar(get_counts(occurences,values), path)

conn = sqlite3.connect('hittite2.db')
c = conn.cursor()

##Части речи
PoSes = ['ADV','ADJ','N','P','V','CONJ','ADV','Q']
print('here is the part-of-speech graph, close it to see another one')
get_bar(PoSes,c,'parts_of_speech.png')

##Падежи:
cases = ['NOM','LOC','GEN','DAT','ABL','INSTR','DAT-LOC','VOC']
print('here is the cases graph, close it to see another one')
get_bar(cases,c,'cases.png')

##Типы местоимений:
c.execute('SELECT * FROM words_and_glosses INNER JOIN glosses ON words_and_glosses.gloss_id = glosses.id WHERE glosses.meaning LIKE "%pronoun%"')
pronounoccurences = [i[3] for i in c.fetchall()]
print('here is the pronouns graph, close it to see another one')
create_bar(get_counts(pronounoccurences), 'pronoun_types.png')


