import numpy as np
import time
import csv
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from argparse import ArgumentParser
from datetime import datetime as dt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import chi2
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
		with Timer("crawling %s ,start_from %s , end in %s"%(args.query,start_time,end_time)):
			corpus[end_time] =  getNews(args.query,start_time,end_time) #(list of news,labels)
	return corpus
def subtract_month(time,k):
	#time = '02/01/2020'
	dte = dt.strptime(time, '%m/%d/%Y').date()
	result = dte + relativedelta(months=-k)
	result = str(result.strftime("%m/%d/%Y"))
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
	vectorizer = TfidfVectorizer(sublinear_tf=True, stop_words="english", smooth_idf=True)
	coo_matrix = vectorizer.fit_transform(corpus).tocoo()
	features = vectorizer.get_feature_names()
	vocab = [features[wid] for wid in coo_matrix.col]
	c_tuples =  zip(coo_matrix.row, vocab, coo_matrix.data)
	ans = sorted(c_tuples, key=lambda x:x[2],reverse = True)
	word = list(set([tup[1] for tup in ans]))[:k]
	return word,c_tuples
def feature_select_with_chi2(corpus,lables,k):
	vectorizer = TfidfVectorizer(max_features = 100000,sublinear_tf=True, stop_words="english", smooth_idf=True)
	tfidf = vectorizer.fit_transform(corpus)
	coo_matrix = tfidf.tocoo()
	features = vectorizer.get_feature_names()
	vocab = [features[wid] for wid in coo_matrix.col]
	c_tuples =  zip(coo_matrix.row, vocab, coo_matrix.data)

	chi2score = chi2(tfidf,lables)[0]
	scores = list(zip(features,chi2score))
	candidated  = sorted(scores,key = lambda x :x[1])
	all_ans = list(zip(*candidated))
	ans = all_ans[0][-k:]

	return ans,c_tuples

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
		norm_tfidf = [float(i)/sum(tfidf_vals) for i in tfidf_vals]		
		relv_val = get_sent_similarity(query,fake_doc,norm_tfidf)
		news_relv.append(relv_val)
	news_relv = np.array(news_relv)
	ans_index = news_relv.argsort()[-k:][::-1]
	#ans = [corpus[i] for i in ans_index]
	return ans_index
def preprocess(corpus):
	porter = PorterStemmer()
	lemmatizer = WordNetLemmatizer()
	stop_words = set(stopwords.words('english'))
	for index ,news in enumerate(corpus):
		token_words = word_tokenize(news)
		token_words = [w for w in token_words if w not in stop_words]
		token_words = [lemmatizer.lemmatize(w) for w in token_words]
		#token_words = [porter.stem(w) for w in token_words]

		corpus[index] = (" ".join(token_words))
	return corpus

def write_to_csv(month,topk_term,rel_news):
	with open('result.csv',"a",newline = "") as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(["Time","Hot_Term","News Title","News text"])
		for news in rel_news:
			writer.writerow([month,topk_term,news["title"],news["text"]])

class Timer(object):
	""" A quick tic-toc timer
	Credit: http://stackoverflow.com/questions/5849800/tic-toc-functions-analog-in-python
	"""

	def __init__(self, name=None, verbose=True):
		self.name = name
		self.verbose = verbose
		self.elapsed = None

	def __enter__(self):
		self.tstart = time.time()
		return self

	def __exit__(self, type, value, traceback):
		self.elapsed = time.time() - self.tstart
		if self.verbose:
			if self.name:
				print ('[%s]' % self.name,)
			print ('Elapsed: %s' % self.elapsed)