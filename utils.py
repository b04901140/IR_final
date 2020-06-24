from argparse import ArgumentParser
from getNews import getNews
from sklearn.feature_extraction.text import TfidfVectorizer
def init_args():
	# you can add any args as you need here
	parser = ArgumentParser()
	parser.add_argument('--query',default='Trump')
	parser.add_argument('--time',default='2019/12/10')
	parser.add_argument('--finish',default = False)
	return parser.parse_args()
def create_corpus(args):
	corpus = {}
	## parse args.time into six month
	for _ in range(6):
		## start_time and end_time need modify
		start_time = args.time -  (_+1)* 30
		end_time = args.time - _*30
		corpus[end_time] =  getNews(args.query,start_time,end_time)
	return corpus
def feature_select(corpus,k):
	### input params :
	###   corpus need to  be list of string
	###   corpus = ["a b c"," c d e"]
	###   k = return term num
	### output params:
	###  ans is list of tuple
	###  ans = [(doc_id,word,tfidf_val)]
	###  only return word
	vectorizer = TfidfVectorizer(sublinear_tf=False, stop_words=None, token_pattern="(?u)\\b\\w+\\b", smooth_idf=True)
	coo_matrix = vectorizer.fit_transform(corpus).tocoo()
	features = vectorizer.get_feature_names()
	vocab = [features[wid] for wid in coo_matrix.col]
	c_tuples =  zip(coo_matrix.row, vocab, coo_matrix.data)
	ans = sorted(c_tuples, key=lambda x:x[2],reverse = True)
	return ans[:k][1]
def news_select(corpus,k):
	#TODO
	pass
	return