from GoogleNews import GoogleNews

from News import News

def get_corpus_in_time_interval(query, start_time, end_time):
    
    gn = GoogleNews(start_time, end_time)
    corpus = list()
    
    page_count = 1

    gn.search(query)
    for i in range(1, page_count + 1):
        gn.clear()
        gn.getpage(i)
        all_rel_news = gn.result()
        for raw_news in all_rel_news:
            news = News(raw_news)
            if news.mainText != 'fail':
                corpus.append(news)

    return corpus

