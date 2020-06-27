from GoogleNews import GoogleNews
from newsplease import NewsPlease
import requests
import urllib
import numpy as np
def isRedirect(url):
	try:
		response = requests.get(url, allow_redirects=True)
		if response.url != url:
			return True
	except Exception as e:
		return True
	return False
def get_content(result):
	ret = []
	for i, news in enumerate(result):
		url = news['link']
		if isRedirect(url): continue 
		response = requests.get(url)
		if response.status_code != 200: continue
		article = NewsPlease.from_url(url)
		if (article.maintext == 'None'): continue
		else:
			#data = {"title":article.title,"text":article.maintext}
			ret.append(article.title + article.maintext)
	return ret

def getNews(topic, start_time, end_time):
	googlenews = GoogleNews(start = start_time, end = end_time)
	result = []
	labels = []
	for i in range(1,2):
		googlenews.clear()
		googlenews.search(topic)
		googlenews.getpage(i)
		tmp = googlenews.result()

		#result  += [x["title"]+x["desc"] for x in tmp]
		tmp_result = get_content(tmp)
		result += tmp_result
		if i == 1:
			labels += [1 for _ in range(len(tmp_result))]
		else:
			labels += [0 for _ in range(len(tmp_result))]
	labels = np.array(labels)
	return (result , labels)


