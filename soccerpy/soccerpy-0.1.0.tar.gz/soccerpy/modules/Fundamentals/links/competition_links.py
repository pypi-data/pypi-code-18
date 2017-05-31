from soccerpy.modules.Fundamentals.links.base_links import BaseLinks
# from soccerpy.modules.Competition.competition_specific import CompetitionSpecific


class CompetitionLinks(BaseLinks):
    def __init__(self, links, request):
        super(CompetitionLinks, self).__init__(request)
        self.url = links['self']['href']
        self.competition = links['competition']['href']
    #
    # def get_competition(self):
    #     data, headers = self.r.request(raw_url=self.competition)
    #     return CompetitionSpecific(data, headers)
