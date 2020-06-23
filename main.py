from utils import *


def main():
	while True:
		args =  init_args()
		if args.finish:
			break
		# all_corpus has six small corpus,is a dict{}
		all_corpus = create_corpus(args)
		for month,m_corpus in all_corpus.items():
			topk_term = feature_select(m_corpus,k = 20)
			topk_rel_news = news_select(m_corpus,k = 3)
			print("most_rel_term in month:\n%s | most_rel_news:\n%s"%
				(str(topk_term),topk_rel_news))
		

	return
if __name__ == '__main__':
	main()