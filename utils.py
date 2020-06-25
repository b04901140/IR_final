import numpy as np
from argparse import ArgumentParser
from datetime import datetime as dt
from sklearn.feature_extraction.text import TfidfVectorizer
from dateutil.relativedelta import relativedelta
from getSentSimilarity import get_sent_similarity
from getNews import getNews
def init_args():
	# you can add any args as you need here
	parser = ArgumentParser()
	parser.add_argument('--query',default='Trump')
	parser.add_argument('--time',default='12/10/2019')
	parser.add_argument('--finish',default = False)
	return parser.parse_args()
def create_corpus(args):
	corpus = {}
	## parse args.time into six month
	for _ in range(6):
		## start_time and end_time need modify
		start_time = subtract_month(args.time,_+1)
		end_time = subtract_month(args.time,_)
		corpus[end_time] =  getNews(args.query,start_time,end_time)
	return corpus
def subtract_month(time,k):
	#time = '02/01/2020'
	dte = dt.strptime(time, '%m/%d/%Y').date()
	result = dte + relativedelta(months=-k)
	result.strftime("%m/%d/%Y")
	return result

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
	ans = sorted(c_tuples, key=lambda x:x[2],reverse = True)[:k]
	word = [tup[1] for tup in ans]
	return word,c_tuples
def news_select(query,corpus,c_tuples,k):
	Total_news_num = len(corpus)
	news_relv = []
	for news_index in range(Total_news_num):
		fake_doc = ""
		tfidf_vals = []
		for doc_id,word,tfidf_val in c_tuples:
			if doc_id == news_index:
				fake_doc += (word+" ")
				tfidf_vals.append(tfidf_val)
		norm_tfidf = [float(i)/sum(raw) for i in tfidf_vals]		
		relv_val = get_sent_similarity(query,fake_doc,norm_tfidf)
		news_relv.append(relv_val)
	news_relv = np.array(news_relv)
	ans = news_relv.argsort()[-k:][::-1]
	return ans
