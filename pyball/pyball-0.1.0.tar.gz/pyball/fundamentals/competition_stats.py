from collections.abc import Sequence
from pyball.fundamentals.base_fundamental import BaseFundamental


class Scorer:
    def __init__(self, data):
        self.name = data.find("a", class_="bold").text
        self.team = data.find("span", class_="top_scorer_team").find("a").text
        self.goals = data.find("div", class_="top_goalers_goals").text


class TopScorers(Sequence):
    def __getitem__(self, index):
        return self.scorers[index]

    def __len__(self):
        return len(self.scorers)

    def __init__(self, data):
        self.data = data
        self.scorers = []
        self.process()

    def process(self):
        self.scorers.append(Scorer(self.data))


class CompetitionStats(BaseFundamental):
    def __init__(self, soup):
        super(CompetitionStats, self).__init__(soup)
        self.top_scorers = TopScorers(self.soup.find_all("div", class_="top_goalers_row"))
