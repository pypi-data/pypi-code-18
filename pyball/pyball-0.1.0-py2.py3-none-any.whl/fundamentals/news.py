from collections.abc import Sequence
from pyball.fundamentals.base_fundamental import BaseFundamental


class News(BaseFundamental):
    def __init__(self, soup):
        super(News, self).__init__(soup)
        self.news_list = []
        self.process()

    def process(self):
        news = self.soup.find_all("a", class_="list_rep")
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
        for d in self.data:
            self.news.append(NewsSingle(d))


class NewsSingle:
    def __init__(self, data):
        self.title = data.find("div", class_="list_rep_title").find("div").text
        self.text = data.text
        self.published_at = data.find("div", class_="timeago")['title']
