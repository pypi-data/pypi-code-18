from soccerpy.modules.Competition.base_competition import BaseCompetition
from soccerpy.modules.Fundamentals.links.competition_links import CompetitionLinks
from soccerpy.modules.Fundamentals.teams import Teams


class CompetitionTeams(BaseCompetition):
    def __init__(self, data, headers, request):
        super().__init__(headers, request)
        self.links = CompetitionLinks(data["_links"], self.r)
        self.count = data['count']
        self.teams = Teams(data['teams'], self.r)
