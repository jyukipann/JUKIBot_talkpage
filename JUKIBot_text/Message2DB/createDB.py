import forLINE
import forDiscord
import forTwitter
import sqlite3
from . import _createDB

def pushList2LR(dbpath,LRList):
	_createDB._createLRtable(dbpath)
	conn = sqlite3.connect(dbpath)
	cur = conn.cursor()
	for row in LRList:
		_createDB.insertLR(row,conn)
	conn.close()

def read_all_data(dbpath,tablename,where=""):
	_createDB.createLRtable(dbpath)
	conn = sqlite3.connect(dbpath)
	cur = conn.cursor()
	cur.execute("SELECT * FROM {t} {w}".format(t=tablename,w=where))
	LINEList = [message for message in cur.fetchall()]
	conn.close()
	return LINEList

if __name__ == '__main__':
	pathdb = 'databases/testdatabases/JukiBot.db'
	pathraw = 'code_test/[LINE] Chat in じゅきじゅきのお部屋💕.txt'
	linelist = forLINE.LINEtext2list(pathraw)
	pushList2LR(pathdb,linelist)
	print(read_all_data(pathdb,"LatestReply"))