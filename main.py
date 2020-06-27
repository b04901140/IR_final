#from utils import *

from utils import create_corpus, init_args

def main():
    args = init_args()

    all_corpus = create_corpus(args)

    test_result(all_corpus)


def test_result(all_corpus):
    for end_time, corpus in all_corpus.items():
        print(end_time, len(corpus))
        for _, news in enumerate(corpus):
            f = open(f'news{_}', 'w')
            f.write(news.__str__())
            f.close()


if __name__ == '__main__':
    main()
