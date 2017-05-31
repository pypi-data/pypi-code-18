from soccerpy.modules.Fixture.base_fixture import BaseFixture
from soccerpy.modules.Fundamentals.fixtures import Fixture
from soccerpy.modules.Fundamentals.head2head import Head2Head


class FixturesSpecific(BaseFixture):
    def __init__(self, data, headers, request):
        super().__init__(headers, request)
        self.fixture = Fixture(data['fixture'], self.r)
        self.head2head = Head2Head(data['head2head'], self.r)
