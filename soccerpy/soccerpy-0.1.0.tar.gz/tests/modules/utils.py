import re
import os
import json
from soccerpy.soccer import Soccer


def do_init(instance="competition"):
    s = Soccer(API_KEY="05d52d8812a548c6a9f6f29ed60e8e00")
    # o = getattr(s, instance)
    if instance.lower() == "fixture":
        return s.fixture
    elif instance.lower() == "competition":
        return s.competition
    return s.team


def get_test_data(filename="testingdata/competition_tests_data.json"):
    # filename = os.path.abspath(filename)
    directory = os.path.dirname(__file__)
    filename = os.path.join(directory, filename)
    with open(filename) as jsonfile:
        data = json.load(jsonfile)
        jsonfile.close()
    return data


def convert_to_snake_case(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
