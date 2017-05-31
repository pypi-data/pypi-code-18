from soccerpy.modules.Competition.base_competition import BaseCompetition
from soccerpy.modules.Fundamentals.competitions import Competition


class CompetitionSpecific(BaseCompetition):
    def __init__(self, data, headers, request):
        super().__init__(headers, request)
        self.competition = Competition(data, self.r)
