from pyball.modules.base_module import BaseModule
from pyball.fundamentals.news import News
from pyball.fundamentals.team_top_scorers import TeamTopScorers


class Team(BaseModule):
    def __init__(self, *args, team_name):
        super(Team, self).__init__(*args)
        self.team_name = team_name

    def get_news(self):
        soup = self.requester.request(endpoint_name="team_news",
                                      endpoint_format=self.team_name)
        return News(soup)

    # def fixtures(self, season="2016/17"):
    #     soup = self.requester.request(endpoint_name="team_fixtures",
    #                                   endpoint_format=(self.team_name, season))
    #     return TeamFixture(soup)

    def top_scorers(self, season="2016/17"):
        soup = self.requester.request(endpoint_name="team_top_scorers",
                                      endpoint_format=(self.team_name, season))
        return TeamTopScorers(soup)

    def transfer_talk(self):
        soup = self.requester.request(endpoint_name="team_transfer_talk",
                                      endpoint_format=self.team_name)
        return News(soup)

    def injury_news(self):
        soup = self.requester.request(endpoint_name="team_injury_news",
                                      endpoint_format=self.team_name)
        return News(soup)
