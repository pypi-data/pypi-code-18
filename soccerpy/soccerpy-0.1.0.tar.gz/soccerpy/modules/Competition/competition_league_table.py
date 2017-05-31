from soccerpy.modules.Competition.base_competition import BaseCompetition
from soccerpy.modules.Fundamentals.links.competition_links import CompetitionLinks
from soccerpy.modules.Fundamentals.standing import Standing


class CompetitionLeagueTable(BaseCompetition):
    def __init__(self, data, headers, request):
        super().__init__(headers, request)
        self.links = CompetitionLinks(data['_links'], self.r)
        self.league_caption = data['leagueCaption']
        self.matchday = data['matchday']
        self.standing = Standing(data['standing'], self.r)
