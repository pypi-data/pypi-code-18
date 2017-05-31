import unittest
from tests.modules.utils import *


class TestFixture(unittest.TestCase):
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

    def check_fixtures(self, obj, key, value):
        for key2, value2 in value.items():
            if key2 == "_links":
                self.check_links(obj, key2, value2)
            elif key2 == "squadMarketValue":
                continue
            elif key2 == "home" or key2 == "away":
                self.check_location(obj, key2, value2)
            elif key2 == "result":
                self.check_location(obj, key2, value2)
            else:
                attribute_name = convert_to_snake_case(key2)
                attribute_value = getattr(obj, attribute_name)
                self.assertEqual(value2, attribute_value)

    def test_fixtures_all(self):
        f = do_init(instance="fixture")
        fixt = f.get_by_time_frame_and_league("n14", "PL")
        data = get_test_data("testingdata/fixture_tests_data.json")['fixtures_all']
        for key, value in data.items():
            if key == "_links":
                self.check_links(fixt, key, value)
            elif key == "fixtures":
                self.check_fixtures(fixt.fixtures[0], key, value[0])
            else:
                attribute_name = convert_to_snake_case(key)
                attribute_value = getattr(fixt, attribute_name)
                self.assertEqual(value, attribute_value)

    def test_fixtures_specific(self):
        f = do_init(instance="fixture")
        fixt = f.get_specific(155299)
        data = get_test_data("testingdata/fixture_tests_data.json")['fixtures_specific']
        for key, value in data.items():
            if key == "_links":
                self.check_links(fixt, key, value)
            elif key == "fixture":
                self.check_fixtures(fixt.fixture, key, value)
            else:
                pass

if __name__ == "__main__":
    unittest.main()
