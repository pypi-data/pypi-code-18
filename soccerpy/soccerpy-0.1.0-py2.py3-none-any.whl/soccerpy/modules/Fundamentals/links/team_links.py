from soccerpy.modules.Fundamentals.links.base_links import BaseLinks
# from soccerpy.modules.Team.team_specific import TeamSpecific


class TeamLinks(BaseLinks):
    def __init__(self, links, request):
        super(TeamLinks, self).__init__(request)
        if "self" in links:
            self.url = links['self']['href']
        self.team = links['team']['href']

    # def get_team(self):
    #     data, headers = self.r.request(raw_url=self.team)
    #     return TeamSpecific(data, headers)
