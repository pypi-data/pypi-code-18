from pyball.base import Base
from pyball.modules.all import All
from pyball.modules.team import Team
from pyball.modules.competition import Competition


class Ball(Base):
    def __init__(self):
        super().__init__()
        self.all = All(self.requester)
        self.competition = Competition(self.requester)
        self.team = Team(self.requester, team_name='real-madrid')

if __name__ == "__main__":
    ball = Ball()
    print(ball.competition.get_news("premier-league").news_list[0].text)
