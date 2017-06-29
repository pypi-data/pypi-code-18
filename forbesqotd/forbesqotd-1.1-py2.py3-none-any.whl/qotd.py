from bs4 import BeautifulSoup
import requests
import re


class forbes():
    def __init__(self):
        self.url = "https://www.forbes.com/forbes/welcome/"
        self.page = requests.get(self.url)
        self.data = self.page.text
        self.soup = BeautifulSoup(self.data, 'html.parser')
        self.ans = self.soup.find_all(string=re.compile("Quote of the Day"))
        self.ans = self.ans[0]

    def get_quote(self):
        self.quote = self.ans[self.ans.find("description")+14:
                              self.ans.find("following")-3]
        return self.quote

    def get_by(self):
        self.by = self.ans[self.ans.find("byline")+9:
                           self.ans.find("bylineTitle")-4]
        return self.by
