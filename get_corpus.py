from GoogleNews import GoogleNews

from News import News

def get_corpus_in_time_interval(start_time, end_time, args):
    query = args.query
    page_count = args.pages
    
    gn = GoogleNews(start=start_time, end=end_time)
    corpus = list()

    gn.search(query)
    for i in range(1, page_count + 1):
        gn.clear()
        gn.getpage(i)
        all_rel_news = gn.result()
        for raw_news in all_rel_news:
            news = News(raw_news)
            if i == 1:
                news.set_relv()
            if news.mainText != 'fail':
                corpus.append(news)

    return corpus

