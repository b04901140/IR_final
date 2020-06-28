import numpy as np
import time
import csv
from argparse import ArgumentParser
from datetime import datetime as dt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import chi2
from dateutil.relativedelta import relativedelta
from getSentSimilarity import get_sent_similarity
from nltk  import word_tokenize,pos_tag
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords ,wordnet

#from getNews import getNews

from get_corpus import get_corpus_in_time_interval

from News import News

def init_args():
    # you can add any args as you need here
    parser = ArgumentParser()
    parser.add_argument('--query', default='Trump')
    parser.add_argument('--time', default='12/10/2019')
    parser.add_argument('--finish', default=False)
    parser.add_argument('--months', default=1)
    parser.add_argument('--pages', default=1)
    return parser.parse_args()

def create_corpus(args):
    all_corpus = dict()
    month_count = args.months

    for month in range(month_count):
        start_time  = subtract_month(args.time, month+1)
        end_time    = subtract_month(args.time, month)
        all_corpus[end_time] = get_corpus_in_time_interval(start_time, end_time, args)
    
    return all_corpus

def subtract_month(time,k):
	#time = '02/01/2020'
	dte = dt.strptime(time, '%m/%d/%Y').date()
	result = dte + relativedelta(months=-k)
	result = str(result.strftime("%m/%d/%Y"))
	return result

def feature_select(News,k):
	### input params :
	###   corpus need to  be list of string
	###   corpus = ["a b c"," c d e"]
	###   k = return term num
	### output params:
	###  ans is list of tuple
	###  ans = [(doc_id,word,tfidf_val)]
	###  only return word
	corpus = [x.mainText for x in News]
	vectorizer = TfidfVectorizer(sublinear_tf=True, stop_words="english", smooth_idf=True)
	coo_matrix = vectorizer.fit_transform(corpus).tocoo()
	features = vectorizer.get_feature_names()
	vocab = [features[wid] for wid in coo_matrix.col]
	c_tuples =  zip(coo_matrix.row, vocab, coo_matrix.data)
	ans = sorted(c_tuples, key=lambda x:x[2],reverse = True)
	word = list(set([tup[1] for tup in ans]))[:k]
	return word,c_tuples
def feature_select_with_chi2(News,k):
	lables = [x.relv for x in News]
	corpus = [x.title for x in News]
	vectorizer = TfidfVectorizer(max_features = 100000,sublinear_tf=True, stop_words="english", smooth_idf=True)
	tfidf = vectorizer.fit_transform(corpus)
	features = vectorizer.get_feature_names()

	chi2score = chi2(tfidf,lables)[0]
	scores = list(zip(features,chi2score))
	candidated  = sorted(scores,key = lambda x :x[1])
	all_ans = list(zip(*candidated))
	ans = all_ans[0][-k:]

	return ans
def news_select(query,News,k):
	Total_news_num = len(News)
	lables = np.array([x.relv for x in News])
	corpus = [x.title + x.mainText for x in News]
	rec_news = []
	vectorizer = TfidfVectorizer(max_features = 100000,sublinear_tf=True, stop_words="english", smooth_idf=True)
	tfidf = vectorizer.fit_transform(corpus)
	coo_matrix = tfidf.tocoo()
	features = vectorizer.get_feature_names()
	vocab = [features[wid] for wid in coo_matrix.col]
	c_tuples =  zip(coo_matrix.row, vocab, coo_matrix.data)
	for news_index in range(Total_news_num):
		fake_doc = ""
		tfidf_vals = []
		for doc_id,word,tfidf_val in c_tuples:
			if doc_id == news_index:
				fake_doc += (word+" ")
				tfidf_vals.append(tfidf_val)
		norm_tfidf = [float(i)/sum(tfidf_vals) for i in tfidf_vals]		
		relv_val = get_sent_similarity(query,fake_doc,norm_tfidf)
		rec_news.append(relv_val)
	rec_news = np.array(rec_news)
	ans_index = rec_news.argsort()[-k:][::-1]
	#ans = [corpus[i] for i in ans_index]
	return ans_index
 

def preprocess_all_corpus(all_corpus):
    porter = PorterStemmer()
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))
    for end_time, corpus in all_corpus.items():
        for news in corpus:
            preprocess(news, 'title', porter, lemmatizer, stop_words)
            preprocess(news, 'mainText', porter, lemmatizer, stop_words)

    return

def preprocess(news, attr, porter, lemmatizer, stop_words):
    if attr == 'mainText':
        tokens = word_tokenize(news.mainText)
    elif attr == 'title':
        tokens = word_tokenize(news.title)

    tags = pos_tag(tokens)
    tokens = [t for t in tokens if t not in stop_words and not t.isdigit()]
    tokens = [lemmatizer.lemmatize(w[0], pos=get_wordnet_pos(w[1]) or wordnet.NOUN) for w in tags]
    tokens = [porter.stem(w) for w in tokens]
            
    result = (" ".join(tokens))

    if attr == 'mainText':
        news.mainText = result
    elif attr == 'title':
        news.title = result

    return
 

    

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

def get_wordnet_pos(tag):
	if tag.startswith('J'):
		return wordnet.ADJ
	elif tag.startswith('V'):
		return wordnet.VERB
	elif tag.startswith('N'):
		return wordnet.NOUN
	elif tag.startswith('R'):
		return wordnet.ADV
	else:
		return None

