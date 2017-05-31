from soccerpy.modules.Fundamentals.teams import Team
from soccerpy.modules.Team.base_team import BaseTeam


class TeamSpecific(BaseTeam):
    def __init__(self, data, headers, request):
        super().__init__(headers, request)
        self.team = Team(data, self.r)
