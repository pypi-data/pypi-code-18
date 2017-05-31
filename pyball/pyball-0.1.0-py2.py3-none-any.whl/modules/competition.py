from pyball.modules.base_module import BaseModule
from pyball.fundamentals.competition_stats import CompetitionStats
from pyball.fundamentals.competition_news import CompetitionNews


class Competition(BaseModule):
    def __init__(self, requester):
        super(Competition, self).__init__(requester)

    def get_top_scorer(self, league_name, season):
        soup = self.requester.request(endpoint_name="competition_stats",
                                      endpoint_format=(league_name, season))
        return CompetitionStats(soup)

    def get_news(self, league_name):
        soup = self.requester.request(endpoint_name="competition_news",
                                      endpoint_format=league_name)
        return CompetitionNews(soup)
