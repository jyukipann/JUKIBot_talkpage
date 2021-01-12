import csv
import itertools
from collections import deque
import hashlib
from . import _createDB
import sqlite3
"""

2019/04/12 Fri
22:48	あやか あーちゃん（情工	次はショッキングピンク
22:49	じゅき	絶対やらない

=>
latest_hash latest_date latest_author latest reply_hash reply_dateb reply_author reply 
[int(hash),'2019/04/12/22:48','あやか あーちゃん（情工','次はショッキングピンク',int(hash),'じゅき','絶対やらない']

"""

def tohash(data):
	hashId = hashlib.md5()
	hashId.update(repr(data).encode("utf-8"))
	return hashId.digest()

def LINEtext2list(path,start=0,end=None,dbpath="",name="じゅき"):
	LINElist = []
	queue = deque([[0,"","",""]],maxlen=2)
	date = ""
	if dbpath != "":
		_createDB.createLRtable(dbpath)
		conn = sqlite3.connect(dbpath)
		with open(path, newline='',encoding="utf-8") as f:
			reader = csv.reader(itertools.islice(f, start, end), delimiter='\t')
			for row in reader:
				if len(row) == 1:
					date = row[0].split()[0]
				elif len(row) == 3:
					tmp = row
					tmp[0] = date+" "+tmp[0]
					hh = hashlib.md5(str(tmp).encode()).digest()
					hh = int(str(int.from_bytes(hh, byteorder='big'))[:18])
					queue.append([hh,tmp[0],tmp[1],tmp[2]])
					l = queue[0] + queue[1]
					if name == l[-2]:
						print(l)
						_createDB.insertLR(l,conn)
		conn.close()
	else:
		with open(path, newline='',encoding="utf-8") as f:
			reader = csv.reader(itertools.islice(f, start, end), delimiter='\t')
			for row in reader:
				if len(row) == 1:
					date = row[0].split()[0]
				elif len(row) == 3:
					tmp = row
					tmp[0] = date+" "+tmp[0]
					hh = hashlib.md5(str(tmp).encode()).digest()
					hh = int(str(int.from_bytes(hh, byteorder='big'))[:18])
					queue.append([hh,tmp[0],tmp[1],tmp[2]])
					l = queue[0] + queue[1]
					if name == l[-2]:
						LINElist.append(tuple(l))
		return LINElist

if __name__ == '__main__':
	pathdb = '../databases/testdatabases/JukiBot.db'
	pathraw = 'code_test/[LINE] Chat in じゅきじゅきのお部屋💕.txt'
	LINEList = LINEtext2list(path=pathraw)
	for i in LINEList:
		print(i)
	print()
	LINEtext2list(path=pathraw,end=100,dbpath=pathdb)
