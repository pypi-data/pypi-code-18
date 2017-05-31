from collections.abc import Sequence
from pyball.fundamentals.base_fundamental import BaseFundamental


class Scorer:
    def __init__(self, player):
        self.name = player.find("a", class_="bold").text
        self.goals = player.find("div", class_="top_goalers_goals").text.split()[0]
        self.matches = player.find("div", class_="top_goalers_goals").text.split()[1]


class TeamTopScorers(Sequence, BaseFundamental):
    def __getitem__(self, index):
        return self.scorers[index]

    def __len__(self):
        return len(self.scorers)

    def __init__(self, soup):
        super(TeamTopScorers, self).__init__(soup)
        self.scorers = []
        self.process()

    def process(self):
        data = self.soup.find_all("div", class_="top_goalers_row")
        for player in data:
            self.scorers.append(Scorer(player))
