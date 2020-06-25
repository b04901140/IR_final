from GoogleNews import GoogleNews


def getNews(topic, start_time, end_time):
    googlenews = GoogleNews(start_time, end_time)
    result = []
    for i in range(1,10):
        googlenews.clear()
        googlenews.search(topic)
        googlenews.getpage(i)
        tmp = googlenews.result()
        result  += [x["title"]+x["desc"] for x in tmp]
        for x in tmp:
        	print(x["desc"])
        

    return result

