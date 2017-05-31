from collections.abc import Sequence
from pyball.fundamentals.base_fundamental import BaseFundamental


class CompetitionNews(BaseFundamental):
    def __init__(self, soup):
        super(CompetitionNews, self).__init__(soup)
        self.news_list = []
        self.process()

    def process(self):
        news = self.soup.find("div", class_="sport_top_list")
        self.news_list = NewsList(news)


class NewsList(Sequence):
    def __getitem__(self, index):
        return self.news[index]

    def __len__(self):
        return len(self.news)

    def __init__(self, data):
        self.data = data
        self.news = []
        self.process()

    def process(self):
        odds = self.data.find_all("a", class_="odd")
        evens = self.data.find_all("a", class_="even")
        news = odds + evens
        for d in news:
            self.news.append(NewsSingle(d))


class NewsSingle:
    def __init__(self, data):
        self.title = data.text
        self.text = data['title']
