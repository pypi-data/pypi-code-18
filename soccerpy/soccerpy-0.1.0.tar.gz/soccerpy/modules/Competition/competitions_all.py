from soccerpy.modules.Competition.base_competition import BaseCompetition
from soccerpy.modules.Fundamentals.competitions import Competitions


class CompetitionsAll(BaseCompetition):
    def __init__(self, data, headers, request):
        super().__init__(headers, request)
        self.competitions = Competitions(data, self.r)
