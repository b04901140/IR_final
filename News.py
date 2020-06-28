from newsplease import NewsPlease
import requests

class News:

    def __init__(self, raw_news):

        mainText = self.get_mainText(raw_news['link'])
        self.relv = 0

        self.setContent(raw_news['title'],
                        mainText,
                        raw_news['date'],
                        raw_news['link'])

        #print(self.title, self.mainText)

    def __str__(self):
        return f'{self.title}\n{self.mainText}\n{self.date}\n{self.link}'


    def setContent(self, title, mainText, date, link):
        self.title = title
        self.mainText = mainText
        self.date = date
        self.link = link
    def set_relv(self):
        self.relv = 1

    def isRedirected(self, url):
        try:
            response = requests.get(url, allow_redirects=True)
            if response.url != url:
                return True
        except:
            return True
        return False

    def get_mainText(self, url):
        if self.isRedirected(url):
            return 'fail'
        
        response = requests.get(url)
        if response.status_code != 200:
            return 'fail'

        try:
            article = NewsPlease.from_url(url)
        except:
            return 'fail'

        if article.maintext == None or article.title == None:
            return 'fail'

        return article.maintext
