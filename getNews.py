from GoogleNews import GoogleNews
import pandas as pd
import nltk
#nltk.download()


def getNews(topic, start_time, end_time):
    googlenews = GoogleNews(start_time, end_time)
    googlenews.search(topic)
    result = googlenews.result()
    result = pd.DataFrame(result)

    for i in range(2,10):
        googlenews.getpage(i)
        tmp = googlenews.result()
        tmp = pd.DataFrame(tmp)
        result = pd.concat([result, tmp], ignore_index = True)

    return result

