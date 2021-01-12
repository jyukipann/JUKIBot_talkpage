from markovGen.generateText import *

if __name__ == "__main__":
	dbpath = "databases/JUKI.db"
	mk = markov(dbpath,N=int(input("N = ")))
	while True:
		print("ほぼじゅき :",mk.generateReply(input("あなた : ")))
