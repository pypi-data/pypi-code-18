from collections.abc import Sequence
from soccerpy.modules.Fundamentals.base_fundamental import BaseFundamental
from soccerpy.modules.Fundamentals.master import Master


class Fixtures(BaseFundamental, Sequence):
    def __len__(self):
        return len(self.fixtures)

    def __getitem__(self, index):
        return self.fixtures[index]

    def __init__(self, data, request):
        super(Fixtures, self).__init__(data, request)
        self.fixtures = []
        self.process()

    def process(self):
        for fixture in self.data:
            self.fixtures.append(Fixture(fixture, self.r))


class Fixture(Master):
    def __init__(self, fixture, request):
        super(Fixture, self).__init__(request)
        self.links = FixtureLinks(fixture['_links'])
        self.id = int(self.links.url.split("/")[-1])
        self.date = fixture['date']
        self.status = fixture['status']
        self.matchday = fixture['matchday']
        self.home_team_name = fixture['homeTeamName']
        self.away_team_name = fixture['awayTeamName']
        self.result = Result(fixture['result'])
        if fixture['odds']:
            self.odds = Odds(fixture['odds'])
        self.odds = fixture['odds']

    def get(self):
        data, headers = self.r.request(raw_url=self.links.url)
        return Fixture(data, self.r)

    def competition(self):
        from soccerpy.modules.Competition.competition_specific import CompetitionSpecific
        data, headers = self.r.request(raw_url=self.links.competition)
        return CompetitionSpecific(data, headers, self.r)

    def home_team(self):
        from soccerpy.modules.Team.team_specific import TeamSpecific
        data, headers = self.r.request(raw_url=self.links.home_team)
        return TeamSpecific(data, headers, self.r)

    def away_team(self):
        from soccerpy.modules.Team.team_specific import TeamSpecific
        data, headers = self.r.request(raw_url=self.links.away_team)
        return TeamSpecific(data, headers, self.r)


class FixtureLinks:
    def __init__(self, links):
        self.url = links['self']['href']
        self.competition = links['competition']['href']
        self.home_team = links['homeTeam']['href']
        self.away_team = links['awayTeam']['href']


class Result:
    def __init__(self, result):
        self.goals_home_team = result['goalsHomeTeam']
        self.goals_away_team = result['goalsAwayTeam']
        if 'halfTime' in result:
            self.half_time = HalfTime(result['halfTime'])
        if 'extraTime' in result:
            self.extra_time = ExtraTime(result['extraTime'])
        if 'penaltyShootout' in result:
            self.penalty_shootout = PenaltyShootout(result['penaltyShootout'])


class HalfTime:
    def __init__(self, result):
        self.goals_home_team = result['goalsHomeTeam']
        self.goals_away_team = result['goalsAwayTeam']


class ExtraTime:
    def __init__(self, result):
        self.goals_home_team = result['goalsHomeTeam']
        self.goals_away_team = result['goalsAwayTeam']


class PenaltyShootout:
    def __init__(self, result):
        self.goals_home_team = result['goalsHomeTeam']
        self.goals_away_team = result['goalsAwayTeam']


class Odds:
    def __init__(self, bets):
        self.home_win = bets['homeWin']
        self.draw = bets['draw']
        self.away_win = bets['awayWin']
