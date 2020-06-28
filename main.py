from utils import *
import json

def main():
    args =  init_args()
	# all_corpus has six small corpus,is a dict{}
    all_corpus = create_corpus(args)
	# with open("Trump.json","w") as fp:
	# 	json.dump(all_corpus,fp)
	# with open("Trump.json","r") as fp:
	# 	all_corpus = json.load(fp)

    print('start preprocess', flush=True)
    preprocess_all_corpus(all_corpus)
    print('end preprocess', flush=True)

    for month,News in all_corpus.items():
	topk_term = feature_select_with_chi2(News,k = 20)
	topk_rel_news = news_select(args.query,News,k = 3)
        #write_to_csv(month,topk_term,topk_rel_news)
	print("month:%s| most_rel_term:\n%s | most_rel_news:\n%s"% (str(month),str(topk_term),topk_rel_news))
    test_result(all_corpus)
    return

def test_result(all_corpus):
    for end_time, corpus in all_corpus.items():
        print(end_time, len(corpus))
        for _, news in enumerate(corpus):
            f = open(f'news{_}', 'w')
            f.write(news.__str__())
            f.close()

    return

if __name__ == '__main__':
	main()
