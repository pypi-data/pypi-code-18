from soccerpy.modules.Fixture.base_fixture import BaseFixture
from soccerpy.modules.Fundamentals.fixtures import Fixtures


class FixturesAll(BaseFixture):
    def __init__(self, data, headers, request):
        super().__init__(headers, request)
        self.time_frame_start = data['timeFrameStart']
        self.time_frame_end = data['timeFrameEnd']
        self.count = data['count']
        self.fixtures = Fixtures(data['fixtures'], self.r)
