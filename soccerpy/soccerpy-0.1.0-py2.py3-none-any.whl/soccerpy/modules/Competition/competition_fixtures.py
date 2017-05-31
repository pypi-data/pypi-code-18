from soccerpy.modules.Competition.base_competition import BaseCompetition
from soccerpy.modules.Fundamentals.links.competition_links import CompetitionLinks
from soccerpy.modules.Fundamentals.fixtures import Fixtures


class CompetitionFixtures(BaseCompetition):
    def __init__(self, data, headers, request):
        super().__init__(headers, request)
        self.links = CompetitionLinks(data['_links'], self.r)
        self.count = data['count']
        self.fixtures = Fixtures(data['fixtures'], self.r)
