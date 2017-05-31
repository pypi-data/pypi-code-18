from soccerpy.base import Base
from soccerpy import Competition, Fixture, Team


class Soccer(Base):
    def __init__(self, API_KEY="", response_format="full"):
        super(Soccer, self).__init__(API_KEY, response_format)
        self.competition = Competition(requester=self.requester)
        self.fixture = Fixture(requester=self.requester)
        self.team = Team(requester=self.requester)


if __name__ == "__main__":
    # s = Soccer(API_KEY="05d52d8812a548c6a9f6f29ed60e8e00")
    # comps = s.competition.get_all()
    s = Fixture(API_KEY="05d52d8812a548c6a9f6f29ed60e8e00")
    comps = s.get_by_time_frame_and_league("n14", "PL")
    print(comps.fixtures[0].home_team().team.name)
