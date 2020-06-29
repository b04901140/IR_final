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
    #args.query = "vietnam"
    all_terms = []
    for month,News in all_corpus.items():
        topk_term = feature_select_with_chi2(News,k = 20)
        topk_rel_news = news_select(args.query,News,k = 3)
        #write_to_csv(month,topk_term,topk_rel_news)
        print("month:%s| most_rel_term:\n%s"% (str(month),str(topk_term)))
        print("most_rel_news:")
        all_terms.append(topk_term)
        for i in topk_rel_news:
            print('Title: {}\n'.format(News[i].rawTitle))
            print('Link: {}'.format(News[i].link))
            print('-------------------------------------------------------')
    #test_result(all_corpus)

    while(1):
        print("Followings is all the terms combined from all months")
        print(all_terms)
        args.query = input('Input a keyword that you are interested in:  ')
        for month,News in all_corpus.items():
            #topk_term = feature_select_with_chi2(News,k = 20)
            topk_rel_news = news_select(args.query,News,k = 3)
            #write_to_csv(month,topk_term,topk_rel_news)
            print("month:%s"% (str(month)))
            print("most_rel_news:")
            for i in topk_rel_news:
                print('Title: {}\n'.format(News[i].rawTitle))
                print('Link: {}'.format(News[i].link))
                print('-------------------------------------------------------')
    #return

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
