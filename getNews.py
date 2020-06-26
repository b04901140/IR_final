from GoogleNews import GoogleNews
from newsplease import NewsPlease
import requests
import urllib

def isRedirect(url):
    print("start")
    print(url)
    response = requests.get(url, allow_redirects=True)
    print(response.url)
    print('done')
    if (len(response.history) == 0):
        return True
    if response.url != url:
        return True
    return False
def get_content(result):
    ret = []
    for i, news in enumerate(result):
        url = news['link']
        if isRedirect(url): continue 
        response = requests.get(url)
        article = NewsPlease.from_url(url)
        if (article.maintext == 'None'): continue
        else:
            ret.append(article.title+article.maintext)
    return ret

def getNews(topic, start_time, end_time):
    googlenews = GoogleNews(start_time, end_time)
    result = []
    for i in range(1,10):
        googlenews.clear()
        googlenews.search(topic)
        googlenews.getpage(i)
        tmp = googlenews.result()
        #result  += [x["title"]+x["desc"] for x in tmp]
        result += get_content(tmp)
         

    return result


