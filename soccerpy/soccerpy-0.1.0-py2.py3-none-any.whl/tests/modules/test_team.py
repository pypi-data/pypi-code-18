import unittest
from tests.modules.utils import *


class TestTeam(unittest.TestCase):
    def check_links(self, obj, key, value):
        temp_key = key[1:]
        for key2, value2 in value.items():
            sub_attribute = getattr(obj, temp_key)
            attribute_name = convert_to_snake_case(key2)
            if key2 == "self":
                attribute_name = convert_to_snake_case("url")
            attribute_value = getattr(sub_attribute, attribute_name)
            self.assertEqual(value2['href'], attribute_value)

    def check_location(self, obj, key, value):
        sub_attribute = getattr(obj, convert_to_snake_case(key))
        for key2, value2 in value.items():
            attribute_name = convert_to_snake_case(key2)
            attribute_value = getattr(sub_attribute, attribute_name)
            self.assertEqual(value2, attribute_value)

    def check_teams(self, obj, key, value):
        for key2, value2 in value.items():
            if key2 == "_links":
                self.check_links(obj, key2, value2)
            elif key2 == "squadMarketValue":
                continue
            elif key2 == "marketValue":
                continue
            elif key2 == "home" or key2 == "away":
                self.check_location(obj, key2, value2)
            elif key2 == "result":
                self.check_location(obj, key2, value2)
            else:
                attribute_name = convert_to_snake_case(key2)
                attribute_value = getattr(obj, attribute_name)
                self.assertEqual(value2, attribute_value)

    def test_team_fixtures(self):
        t = do_init(instance="team")
        team = t.get_fixtures_by_season_and_venue(66, 2015, "home")
        data = get_test_data("testingdata/team_tests_data.json")['team_fixtures']
        for key, value in data.items():
            if key == "_links":
                self.check_links(team, key, value)
            elif key == "fixtures":
                self.check_teams(team.fixtures[0], key, value[0])
            else:
                attribute_name = convert_to_snake_case(key)
                attribute_value = getattr(team, attribute_name)
                self.assertEqual(value, attribute_value)

    def test_team_specific(self):
        t = do_init(instance="team")
        team = t.get_specific(66)
        data = get_test_data("testingdata/team_tests_data.json")['team_specific']
        # for key, value in data.items():
        self.check_teams(team.team, "man i am being lazy as fuck right now", data)

    def test_team_players(self):
        t = do_init(instance="team")
        team = t.get_players(66)
        data = get_test_data("testingdata/team_tests_data.json")['team_players']
        for key, value in data.items():
            if key == "_links":
                self.check_links(team, key, value)
            elif key == "players":
                self.check_teams(team.players[0], key, value[0])
            else:
                attribute_name = convert_to_snake_case(key)
                attribute_value = getattr(team, attribute_name)
                self.assertEqual(value, attribute_value)


if __name__ == "__main__":
    unittest.main()
