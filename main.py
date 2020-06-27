#from utils import *

from utils import create_corpus, init_args

def main():
    args = init_args()

    month_count = 1
    all_corpus = create_corpus(args, month_count)

    for end_time, corpus in all_corpus.items():
        print(end_time, len(corpus))
        for _, news in enumerate(corpus):
            f = open(f'news{_}', 'w')
            f.write(news.__str__())
            f.close()



if __name__ == '__main__':
    main()
