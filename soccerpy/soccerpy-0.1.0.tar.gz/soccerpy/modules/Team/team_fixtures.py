from soccerpy.modules.Fundamentals.fixtures import Fixtures
from soccerpy.modules.Fundamentals.links.team_links import TeamLinks
from soccerpy.modules.Team.base_team import BaseTeam


class TeamFixtures(BaseTeam):
    def __init__(self, data, headers, request):
        super().__init__(headers, request)
        self.links = TeamLinks(data['_links'], self.r)
        if 'timeFrameStart' in data:
            self.time_frame_start = data['timeFrameStart']
        if 'timeFrameEnd' in data:
            self.time_frame_end = data['timeFrameEnd']
        self.count = data['count']
        self.fixtures = Fixtures(data['fixtures'], self.r)
