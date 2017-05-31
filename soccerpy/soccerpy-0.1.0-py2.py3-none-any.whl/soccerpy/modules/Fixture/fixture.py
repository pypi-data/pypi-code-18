from soccerpy.modules.base_module import BaseModule
from soccerpy.modules.Fixture.fixtures_all import FixturesAll
from soccerpy.modules.Fixture.fixtures_specific import FixturesSpecific


class Fixture(BaseModule):
    def __init__(self, API_KEY="", requester=None, response_format='full'):
        super(Fixture, self).__init__(API_KEY, requester, response_format=response_format)

    def get(self, time_frame=None, league=None, raw=False):
        data, headers = self.r.request('fixtures', payload={"timeFrame": time_frame,
                                                            "league": league})
        if raw:
            return data
        return FixturesAll(data, headers, self.r)

    def get_by_time_frame(self, time_frame):
        return self.get(time_frame=time_frame)

    def get_by_league(self, league_code):
        return self.get(league=league_code)

    def get_by_time_frame_and_league(self, time_frame, league_code):
        return self.get(time_frame=time_frame, league=league_code)

    def get_specific(self, fixture_id, head2head=None):
        data, headers = self.r.request('fixture_specific', endpoint_format=fixture_id,
                                       payload={"head2head": head2head})
        return FixturesSpecific(data, headers, self.r)

    def get_specific_with_head2head(self, fixture_id, head2head):
        return self.get_specific(fixture_id=fixture_id, head2head=head2head)
