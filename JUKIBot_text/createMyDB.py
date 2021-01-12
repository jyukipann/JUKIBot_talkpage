import spacy
from Message2DB import createMarkovDB, forLINE
import sqlite3
import os

#you should execute only once.

if __name__ == "__main__":

	pathdb = 'databases/JUKI.db'
	path = './../JUKIBot_text_data/LINE'
	N = int(input("N = "))
	files = os.listdir(path)
	files_file = [os.path.join(path, f) for f in files if os.path.isfile(os.path.join(path, f))]
	#print(str(files_file).encode('utf-8',errors='replace'))
	print(str(files_file))
	nlp = spacy.load('ja_ginza')
	for file_path in files_file:
		#print("loading",str(file_path).encode('utf-8',errors='replace'),"making up LR")
		print("loading",file_path,"making up LR")
		forLINE.LINEtext2list(file_path,dbpath=pathdb)
	createMarkovDB.create_Markov_table(pathdb,N)
	conn = sqlite3.connect(pathdb)
	cur = conn.cursor()
	result = cur.execute('select * from LatestReply')
	for LRrow in result:
		rows = createMarkovDB.LRrow2Words(nlp,LRrow,N)
		print("markov_table={N}".format(N=N),rows)
		createMarkovDB.insertMT(rows,conn,N)
	cur.execute('select * from markov_table_{N}'.format(N=N))
	conn.commit()
	result = cur.fetchall()
	print("result")
	for rows in result:
		print(rows)
	createMarkovDB.insertMT(result,conn,N)
	conn.close()
	"""
	forLINE.LINEtext2list(path=pathraw,end=100,dbpath=pathdb)
	testrow = (1234,"author","datetime","明日は晴れますか？",4321,"Author","datetime","いいえ、晴れないと思いますが")
	nlp = spacy.load('ja_ginza')
	dbrow = []
	rows = []
	for row in dbrow:
		rows.append(createMarkovDB.LRrow2Words(nlp,row,4))
	print(rows)
	dbpath = "databases/testdatabases/oncnflicttest.db"
	createMarkovDB.create_Markov_table(dbpath,4)
	conn = sqlite3.connect(dbpath)
	cur = conn.cursor()
	createMarkovDB.insertMT(rows,conn)
	cur.execute('select * from markov_table_4')
	conn.commit()
	result = cur.fetchall()
	conn.close()
	print(result)
	"""