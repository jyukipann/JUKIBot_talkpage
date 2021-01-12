import sqlite3
import spacy
import sys
import os
from collections import deque
sys.path.append(os.path.abspath(".."))
sys.path.append(os.path.abspath("./JUKIBot_text/"))
from Message2DB import createMarkovDB
import random


class markov:
	def __init__(self, dbpath, N=4):
		self.N = N
		self.path = dbpath
		self.nlp = spacy.load('ja_ginza')
		#self.nodict = ["わからん。","うん。","ふーん。"]

	def __selectRow(self):
		def createTupleText(N):
			PK = ''
			for i in range(N,0,-1):
				PK += "word_{i}, ".format(i=i)
			PK = PK[:-2]
			return PK
		sql = """SELECT word FROM markov_table_{N} 
		WHERE ({t}) == ({q})
		""".format(N=self.N, t=createTupleText(self.N), q=("?,"*self.N)[:-1])
		return sql

	def generateReply(self, message):
		reply = ""
		words = createMarkovDB.morphologicalAnalysis(self.nlp,message,strmode=True)
		#データベースからMessageの後ろからN単語までの一致を探す。
		#queueで押し出しながら、一致を探し、文を作成。文末文字。！？がくるまで続ける。
		sql = self.__selectRow()
		queue = deque(["" for i in range(self.N)],maxlen=self.N)
		for word in words:
			queue.append(word)
		for i in range(100):
			#print("queue",queue)
			conn = sqlite3.connect(self.path)
			cur = conn.cursor()
			cur.execute(sql,tuple(queue))
			conn.commit()
			#[(word,),(word,)]
			result = cur.fetchall()
			#print("result",result)
			predict_words = []
			for words in result:
				predict_words += words[0].split()
			if len(predict_words) == 0:
				#見つからなかったときには次数を下げて再チャレンジしたい。
				if len(reply) > 0:
					reply += "。"
					break
				#reply += random.choice(self.nodict)
			else:
				part = random.choice(predict_words)
				queue.append(part)
				reply += part
			if len(reply) > 0 and reply[-1] in ["。","！","？"] and random.random() > 0.5:
				break
			if len(reply) > 140:
				break
			#print("reply",i,reply)
		if len(reply) > 0 and random.random() > 0.5:
			reply = reply[:-1]
		return reply


if __name__ == "__main__":
	dbpath = "../databases/JUKI.db"
	mk = markov(dbpath)
	while True:
		print("ほぼじゅき :",mk.generateReply(input("あなた : ")))
	