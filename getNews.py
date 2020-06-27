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
	titles = []
	texts = []
	for i, news in enumerate(result):
		url = news['link']
		if isRedirect(url): continue 
		response = requests.get(url)
		if response.status_code != 200: continue
		try:
			article = NewsPlease.from_url(url)
		except Exception as e:
			continue
		if (article.maintext == None or article.title == None): continue
		else:
			#data = {"title":article.title,"text":article.maintext}
			titles.append(article.title)
			texts.append(article.maintext)
			#ret.append(article.title + article.maintext)
	return (titles,texts)

def getNews(topic, start_time, end_time):
	googlenews = GoogleNews(start = start_time, end = end_time)
	titles = []
	texts = []
	labels = []
	for i in range(1,2):
		googlenews.clear()
		googlenews.search(topic)
		googlenews.getpage(i)
		tmp = googlenews.result()

		#result  += [x["title"]+x["desc"] for x in tmp]
		(tmp_title , tmp_text) = get_content(tmp)
		titles += tmp_title
		texts += tmp_text
		if i == 1:
			labels += [1 for _ in range(len(tmp_text))]
		else:
			labels += [0 for _ in range(len(tmp_text))]
	#labels = np.array(labels)
	return (titles , texts , labels)


