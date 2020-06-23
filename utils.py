from argparse import ArgumentParser
from getNews import getNews

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
	#TODO
	pass
	return
def news_select(corpus,k):
	#TODO
	pass
	return