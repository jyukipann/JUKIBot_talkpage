import bottle
import sqlite3

class talkDB:
	def __init__(self,dbpath):
		self.conn = sqlite3.connect(dbpath)
		self.cur = self.conn.cursor()
		self.count = 0

	def create(self):
		sql = '''CREATE TABLE IF NOT EXISTS talk (
			id INTEGER,
			message TEXT, 
			reply TEXT,
			PRIMARY KEY (id));'''
		self.cur.execute(sql)
		self.conn.commit()
	
	def get_latest(self,n):
		self.get_count()
		if self.count > n:
			"""
			sql = '''SELECT (message, reply) FROM talk
			ORDER BY id DESC
			LIMIT {n};
			'''.format(n=n)
			"""
			sql = '''SELECT * FROM talk ORDER BY id DESC LIMIT {n}'''.format(n=n)
		elif self.count == 0:
			return []
		else:
			sql = '''SELECT * FROM talk ORDER BY id DESC LIMIT {n}
			'''.format(n=self.count)
		self.cur.execute(sql)
		t = self.cur.fetchall()
		return t

	def get_count(self):
		sql = '''SELECT count(*) FROM talk'''
		self.cur.execute(sql)
		self.conn.commit()
		self.count = self.cur.fetchall()[0][0]

	def insert(self,message,reply):
		sql = '''INSERT INTO talk VALUES (?,?,?)'''
		self.get_count()
		self.cur.execute(sql,(self.count+1,message,reply))
		self.conn.commit()
