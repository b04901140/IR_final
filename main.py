from utils import *
import json

def main():
	args =  init_args()
	# all_corpus has six small corpus,is a dict{}
	all_corpus = create_corpus(args)
	with open("Trump.json","w") as fp:
		json.dump(all_corpus,fp)
	with open("Trump.json","r") as fp:
		all_corpus = json.load(fp)
	for key,(m_corpus,labels) in all_corpus.items():
		all_corpus[key] = (preprocess(m_corpus),labels)
	for month,(m_corpus,labels) in all_corpus.items():
		#topk_term,c_tuple = feature_select(m_corpus,k = 20)
		topk_term,c_tuple = feature_select_with_chi2(m_corpus,labels,k = 20)
		topk_rel_news = news_select(args.query,m_corpus,c_tuple,k = 3)
		#write_to_csv(month,topk_term,topk_rel_news)
		print("month:%s| most_rel_term:\n%s | most_rel_news:\n%s"%
			(str(month),str(topk_term),topk_rel_news))
		

	return
if __name__ == '__main__':
	main()