from newsplease import NewsPlease
import requests

class News:
    '''
    def __init__(self, title, mainText, date, link):
        self.setContent(title, mainText, date, link)
    '''

    def __init__(self, raw_news):

        mainText = self.get_mainText(raw_news['link'])

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

    def isRedirected(self, url):
        '''
        response = requests.get(url, allow_redirects=True)
        if len(response.history) == 0:
            return True
        if response.url != url:
            return True
        return False
        '''
        try:
            response = requests.get(url, allow_redirects=True)
            if reponse.url != url:
                return True
        except:
            return True
        return False

    def get_mainText(self, url):
        #if self.isRedirected(url):
        #    return 'failr'
        article = NewsPlease.from_url(url)
        if article.maintext == 'None':
            return 'failnp'
        return article.title + article.maintext
