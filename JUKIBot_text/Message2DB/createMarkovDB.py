import sqlite3
import spacy
import re
from collections import deque

def detectURL(splited_text):
	re_pattern = "https?://[\w/:%#\$&\?\(\)~\.=\+\-]+"
	detected_URL = []
	for word in splited_text:
		if re.match(re_pattern, word):
			detected_URL.append(word)
	return detected_URL

def morphologicalAnalysis(nlp,text,strmode=False):
	t = text
	if len(t) == 0:
		return []
	if (not (t[-1] in ["?","？","!","！",".","。"])):
		t += "。"
	doc = nlp(t)
	if strmode:
		word_list = [str(token) for token in doc]
	else:
		word_list = [token for token in doc]
	return word_list

#URLや不要な語を排除する関数
def removeNeedlessPart(text):
	t = text
	splited = text.split()
	#remove URL
	URLs = detectURL(splited)
	for URL in URLs:
		t.replace(URL,"")
	#remove Emoji NONE
	return t
	

#this
#	latest_hash latest_date latest_author latest reply_hash reply_dateb reply_author reply 
#into this
#	(word_4, word_3, word_2, word_1, word)
def LRrow2Words(nlp,LRrow,N):
	rows = []
	latest = removeNeedlessPart(LRrow[3])
	reply = removeNeedlessPart(LRrow[7])
	latest = morphologicalAnalysis(nlp,latest,strmode=True)
	reply = morphologicalAnalysis(nlp,reply,strmode=True)
	#queue = deque(latest[-1*N:],maxlen=N+1)
	queue = deque(["" for i in range(N+1)],maxlen=N+1)
	for word in latest[-1*N:]:
		queue.append(word)
	for word in reply:
		queue.append(word)
		rows.append(tuple(queue))
	return rows

#	(word_4, word_3, word_2, word_1, word) if N == 4
def create_Markov_table(dbpath,N):
	conn = sqlite3.connect(dbpath)
	cur = conn.cursor()
	sql = "CREATE TABLE IF NOT EXISTS markov_table_{N} ( ".format(N=N)
	PK = ''
	for i in range(N,0,-1):
		sql += "word_{i} TEXT, ".format(i=i)
		PK += "word_{i}, ".format(i=i)
	PK = PK[:-2]
	sql += "word TEXT, PRIMARY KEY ({pk}));".format(pk=PK)
	cur.execute(sql)
	conn.commit()
	conn.close()

"""
insert into product
  ( id, name, quantity, remark)
values
  ( 2, 'potato', 150, '')
on conflict(id)
do update
  set
    quantity = excluded.quantity
;   
"""
def createTupleText(N):
	PK = ''
	for i in range(N,0,-1):
		PK += "word_{i}, ".format(i=i)
	PK = PK[:-2]
	return PK

def insertMT(rows,conn,N):
	cur = conn.cursor()
	textTuple = createTupleText(N)
	sql = 'INSERT INTO markov_table_{N} '.format(N=N)
	sql += '({t}, word) '.format(t=textTuple)
	sql += 'VALUES ( '+('?,'*(N+1))[:-1]+') '
	sql += 'ON CONFLICT ({t})'.format(t=textTuple)
	sql += 'DO UPDATE '
	sql += 'SET word = word || " " || excluded.word;'
	# near "-": syntax error
	#print(sql)
	cur.executemany(sql,rows)
	conn.commit()

if __name__ == '__main__':
	testrow = (1234,"author","datetime","明日は晴れますか？",4321,"Author","datetime","いいえ、晴れないと思いますが")
	nlp = spacy.load('ja_ginza')
	rows = LRrow2Words(nlp,testrow,4)
	print(rows)
	dbpath = "databases/testdatabases/oncnflicttest.db"
	create_Markov_table(dbpath,4)
	conn = sqlite3.connect(dbpath)
	cur = conn.cursor()
	insertMT(rows,conn,4)
	cur.execute('select * from markov_table_4')
	conn.commit()
	result = cur.fetchall()
	conn.close()
	print(result)