from soccerpy.modules.Fundamentals.fixtures import Fixtures, Fixture
from soccerpy.modules.Fundamentals.master import Master


class Head2Head(Master):
    def __init__(self, head, request):
        super().__init__(request)
        self.count = head['count']
        self.time_frame_start = head['timeFrameStart']
        self.time_frame_emd = head['timeFrameEnd']
        self.home_team_wins = head['homeTeamWins']
        self.away_team_wins = head['awayTeamWins']
        self.draws = head['draws']
        if head['lastHomeWinHomeTeam']:
            self.last_home_win_home_team = Fixture(head['lastHomeWinHomeTeam'], self.r)
        if head['lastWinHomeTeam']:
            self.last_win_home_team = Fixture(head['lastWinHomeTeam'], self.r)
        if head['lastAwayWinAwayTeam']:
            self.last_away_win_away_team = Fixture(head['lastAwayWinAwayTeam'], self.r)
        if head['lastWinAwayTeam']:
            self.last_win_away_team = Fixture(head['lastWinAwayTeam'], self.r)
        self.fixtures = Fixtures(head['fixtures'], self.r)
