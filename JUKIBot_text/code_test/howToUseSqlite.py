import sqlite3
import csv
import itertools

"""
LINEのデータをいい感じにデータベースにしてみる。
LINEのテキストデータはタブ区切り

年月日
時間	名前	メッセージ

年月日はその日の始まりにしか書かれていない。年月日と時刻を結合させて保存したい。
手順としては、
txt list sql
の順番で変形
"""

def LINEtext2list(path,start=0,end=None):
	LINElist = []
	date = ""
	with open(path, newline='') as f:
		reader = csv.reader(itertools.islice(f, start, end), delimiter='\t')
		for row in reader:
			if len(row) == 1:
				date = row[0].split()[0]
			elif len(row) == 3:
				tmp = row
				tmp[0] = date+"/"+tmp[0]
				LINElist.append(tmp)
	return LINElist

def create_table():
	database = 'databases/testdatabases/LINE_text.db'
	conn = sqlite3.connect(database)
	cur = conn.cursor()
	sql = 'CREATE TABLE IF NOT EXISTS LINE_messages (id INTEGER PRIMARY KEY, date TEXT, name TEXT, message TEXT)'
	cur.execute(sql)
	conn.commit()
	conn.close()

def put_data(LINE_messages):
	create_table()
	database = 'databases/testdatabases/LINE_text.db'
	conn = sqlite3.connect(database)
	cur = conn.cursor()
	sql = 'SELECT COUNT(*) FROM LINE_messages'
	cur.execute(sql)
	result = cur.fetchall()
	LINE_messages = [result[0][0] + 1] + LINE_messages
	cur.execute('INSERT INTO LINE_messages VALUES (?, ?, ?, ?)', LINE_messages)
	conn.commit()
	conn.close()

def read_all_data():
	create_table()
	database = 'databases/testdatabases/LINE_text.db'
	conn = sqlite3.connect(database)
	cur = conn.cursor()
	cur.execute('SELECT * FROM LINE_messages')
	LINEList = [message for message in cur.fetchall()]
	conn.close()
	return LINEList

def read_data(where=""):
	create_table()
	database = 'databases/testdatabases/LINE_text.db'
	conn = sqlite3.connect(database)
	cur = conn.cursor()
	cur.execute("SELECT id,name,message FROM LINE_messages " + where)
	LINEList = [message for message in cur.fetchall()]
	conn.close()
	return LINEList

if __name__ == "__main__":
	''' 
	LINEList = LINEtext2list(path="code_test/[LINE] Chat in じゅきじゅきのお部屋💕.txt")
	print(LINEList)
	for message in LINEList:
		put_data(message)
	LINEList = read_all_data()
	print(LINEList)
	print(read_data(where="WHERE id >= {startid} AND id <= {endid}".format(startid=500,endid=505)))
	'''
	conn = sqlite3.connect('./databases/testdatabases/oncnflicttest.db')
	cur = conn.cursor()
	sql = """create table IF NOT EXISTS onconflicttest (id1 TEXT,id2 TEXT,word TEXT, primary key (id1,id2))"""
	cur.execute(sql)
	conn.commit()
	sql = '''insert into onconflicttest (id1 ,id2 ,word ) 
	values (?, ?, ?)
	on conflict (id1,id2)
	do update
	set word = word || " " || excluded.word;
	'''
	cur.executemany(sql,[("12","13","aaaa"),("11","12","bbbb"),("12","11","cccc"),("12","13","dddd")])
	conn.commit()
	cur.execute('select * from onconflicttest')
	conn.commit()
	result = cur.fetchall()
	conn.close()
	print(result)
