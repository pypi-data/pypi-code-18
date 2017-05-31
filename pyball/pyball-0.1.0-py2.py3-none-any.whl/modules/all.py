from pyball.modules.base_module import BaseModule
from pyball.fundamentals.news import News
from pyball.fundamentals.fixtures_all import FixturesAll


class All(BaseModule):
    def __init__(self, *args):
        super(All, self).__init__(*args)

    def get_news(self):
        soup = self.requester.request("news")
        return News(soup)

    def get_fixtures(self):
        soup = self.requester.request("fixtures")
        return FixturesAll(soup)
