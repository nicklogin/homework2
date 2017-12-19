import sqlite3, os

def is_gr(gloss):
    if gloss.isupper() and len(gloss)>1:
        return True
    else:
        return False

def get_id(el, tbl):
    for i in tbl:
        if i[1] == el:
            return i[0]

glosspath = 'glosses.txt'
old_db_path = 'hittite.db'
new_db_path = 'hittite2.db'

conn = sqlite3.connect(old_db_path)
c = conn.cursor()

c.execute('SELECT * FROM wordforms')

t = c.fetchall()

conn.close()
 
with open (glosspath, 'r', encoding='utf-8') as f:
    glossesdict = f.readlines()

for i in range(len(glossesdict)):
    glossesdict[i] = glossesdict[i].split('—')
    glossesdict[i] = [j.strip() for j in glossesdict[i]]

print(glossesdict)

glossesdict = {i[0]:i[1] for i in glossesdict}

lemmas, wordforms, glosses = [], [], []
for i in t:
    lemmas.append(i[0])
    wordforms.append(i[1])
    glosses.append(i[2])
    
words = [(str(i),lemmas[i],wordforms[i],glosses[i]) for i in range(len(lemmas))]

glosslist = []
c = 0

for i in glossesdict:
    glosslist.append((str(c), i, glossesdict[i]))
    c += 1

##print(glosslist)
words_and_glosses = []

for word in words:
    wordglosses = [i for i in word[3].split('.') if is_gr(i)]
    for gl in wordglosses:
        if gl not in glossesdict:
            print(gl)
            glosslist.append((str(c),gl,None))
            glossesdict[gl] = ''
            c += 1
        words_and_glosses.append((word[0], get_id(gl, glosslist)))
    
if os.path.exists(new_db_path):
    os.remove(new_db_path)

conn1 = sqlite3.connect(new_db_path)

d = conn1.cursor()

d.execute('CREATE TABLE words (id, Lemma, Wordform, Glosses)')
d.execute('CREATE TABLE glosses (id, gloss, meaning)')
d.execute('CREATE TABLE words_and_glosses (word_id, gloss_id)')

for word in words:
    d.execute('INSERT INTO words VALUES (?,?,?,?)', word)
for gloss in glosslist:
    d.execute('INSERT INTO glosses VALUES (?,?,?)', gloss)
for wordgloss in words_and_glosses:
    d.execute('INSERT INTO words_and_glosses VALUES (?,?)', wordgloss)

conn1.commit()
conn1.close()
