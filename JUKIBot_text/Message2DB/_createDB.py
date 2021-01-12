import sqlite3
#latest_hash latest_date latest_author latest reply_hash reply_dateb reply_author reply 
def createLRtable(dbpath):
	conn = sqlite3.connect(dbpath)
	cur = conn.cursor()
	sql = '''CREATE TABLE IF NOT EXISTS LatestReply (
		latest_hash INTEGER, 
		latest_date TEXT, 
		latest_author TEXT, 
		latest TEXT,
		reply_hash INTEGER,
		reply_dateb TEXT,
		reply_author TEXT,
		reply TEXT,
		PRIMARY KEY (latest_hash,reply_hash)
	);
	'''
	cur.execute(sql)
	conn.commit()
	conn.close()

def insertLR(row,conn):
	cur = conn.cursor()
	sql = 'SELECT COUNT(*) FROM LatestReply WHERE latest_hash = {l} AND reply_hash = {r}'.format(l=row[0],r=row[4])
	cur.execute(sql)
	result = cur.fetchall()
	if result[0][0] != 0:
		return
	cur.execute('INSERT INTO LatestReply VALUES (?, ?, ?, ?,?, ?, ?, ?)', row)
	conn.commit()
