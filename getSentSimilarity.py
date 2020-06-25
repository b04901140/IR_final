import spacy
from sklearn.metrics.pairwise import cosine_similarity
nlp = spacy.load('en_core_web_md')

def get_sent_similarity(query,doc,tfidf):
	doc = nlp(doc)
	query = nlp(query).vector  # mean of query word embedding
	total_similarity = 0
	for index in range(len(doc)):
		word_sim = float(cosine_similarity(query.reshape(1,-1),doc[index].vector.reshape(1,-1)))
		total_similarity += word_sim * tfidf[index]
	return total_similarity


	