from GoogleNews import GoogleNews 
from newsplease import NewsPlease
import requests

googlenews = GoogleNews(lang='en', start='01/01/2020',end='02/28/2020')
googlenews.search('covid')
result = googlenews.result()

import urllib

'''tmp = result[6]['link']
print(tmp)
response = requests.get(tmp, allow_redirects=True)
print(response.history[1].status_code)
url = response.url
print(url)
response = requests.get(url)
print(response.status_code)'''
def isRedirect(url):
    response = requests.get(url, allow_redirects=True)
    if response.url != url:
        return True
    return False
for i, news in enumerate(result):
    url = news['link']
    #if i == 6 or i == 7: continue
    if isRedirect(url): continue
    response = requests.get(url)
    #if response.history[0].status_code == 302: continue
    article = NewsPlease.from_url(url)
    print(i)
    print(article.title)
    print(article.maintext)
    print('\n\n\n')

