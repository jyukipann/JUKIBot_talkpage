import spacy
import howToUseSqlite as tools
import numpy as np

def dict_factory(cursor, row):
	d = {}
	for idx, col in enumerate(cursor.description):
		d[col[0]] = row[idx]
	return d

if __name__ == "__main__":
	nlp = spacy.load('ja_ginza')
	"""
	s = 300
	g = 700
	where = "WHERE id >= {startid} AND id <= {endid} AND name = 'じゅき'".format(startid=s,endid=g)
	messages = tools.read_data(where=where)
	print(messages)
	zero = np.zeros(300)
	for i in range(len(messages)):
		print(messages[i][1])
		doc = nlp(messages[i][2])
		print(list(doc.sents))
		for token in doc:
			#print((token.vector.shape))
			print("<",token.text, bool((token.vector == zero).all()),">", end=" ")
		print()
		print()
	"""
	t = "明日は晴れますか？いいえ、晴れないと思いますが。"
	doc = nlp(t)
	sents = [i for i in doc.sents]
	token = [str(i) for i in doc]
	print(sents)
	print(token)
	print(type(token[0]))