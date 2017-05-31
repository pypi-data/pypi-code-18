import unittest
from soccerpy.soccer import Soccer

"""Real tests are written at modules sub package, this is just to let know everyone is in place."""


class TestSoccer(unittest.TestCase):
    @staticmethod
    def do_init():
        s = Soccer(API_KEY="05d52d8812a548c6a9f6f29ed60e8e00")
        return s

    def test_get_all_competition(self):
        s = self.do_init()
        comp = s.competition.get_all().competitions[0]
        self.assertEquals(comp.league, "EC")
        self.assertEquals(comp.id, 424)
        self.assertEquals(comp.year, '2016')
        self.assertEquals(comp.links.fixtures, 'http://api.football-data.org/v1/competitions/424/fixtures')

    def test_get_specific_competition(self):
        s = self.do_init()
        comp = s.competition.get_specific(424)
        self.assertEqual(comp.competition.league, "EC")
        self.assertEqual(comp.competition.year, "2016")
        self.assertEqual(comp.competition.current_matchday, 7)
        self.assertEqual(comp.competition.number_of_games, 51)
        self.assertEqual(comp.competition.number_of_teams, 24)
        self.assertEqual(comp.competition.links.teams, "http://api.football-data.org/v1/competitions/424/teams")

    def test_get_teams_competition(self):
        s = self.do_init()
        comp = s.competition.get_teams(426)
        self.assertEqual(len(comp.teams), 20)
        self.assertEqual(comp.teams[0].code, "HUL")
        self.assertEqual(comp.teams[0].short_name, "Hull")
        #
        # def test_get_league_table_competition(self):
        #     s = self.do_init()
        #     league_table = s.competition.get_league_table(424)
        #     self.assertEqual()


if __name__ == "__main__":
    unittest.main()
