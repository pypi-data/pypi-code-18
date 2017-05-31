from soccerpy.modules.Fundamentals.players import Players
from soccerpy.modules.Fundamentals.links.team_links import TeamLinks
from soccerpy.modules.Team.base_team import BaseTeam


class TeamPlayers(BaseTeam):
    def __init__(self, data, headers, request):
        super().__init__(headers, request)
        self.links = TeamLinks(data['_links'], self.r)
        self.count = data['count']
        self.players = Players(data['players'], self.r)
