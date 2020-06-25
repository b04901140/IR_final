from GoogleNews import GoogleNews


def getNews(topic, start_time, end_time):
    googlenews = GoogleNews(start_time, end_time)
    googlenews.search(topic)
    tmp = googlenews.result()
    result = [x["title"]+x["desc"] for x in tmp]
    for i in range(2,10):
        googlenews.clear()
        googlenews.getpage(i)
        tmp = googlenews.result()
        news = [x["title"]+x["desc"] for x in tmp]
        result += news

    return result

