from collections.abc import Sequence
from pyball.fundamentals.base_fundamental import BaseFundamental


class Match:
    def __init__(self, match):
        self.time = self.process_time(match)
        self.home_team = match.find("div", class_="live_scores_full_part_two").text
        self.away_team = match.find("div", class_="live_scores_full_part_four").text

    @staticmethod
    def process_time(match):
        status = match.find("span", class_="live_scores_box").text
        if "FT" in status:
            return 1
        return status


class Fixture(Sequence):
    def __getitem__(self, index):
        return self.matches[index]

    def __len__(self):
        return len(self.matches)

    def __init__(self, fixture):
        self.league = fixture['league']
        self.matches = []
        self.process(fixture['matches'])

    def process(self, matches):
        for match in matches:
            self.matches.append(Match(match))


class FixturesList(Sequence):
    def __getitem__(self, index):
        return self.fixtures[index]

    def __len__(self):
        return len(self.fixtures)

    def __init__(self, data):
        self.data = data
        self.fixtures = []
        self.process()

    def process(self):
        status = True
        start = self.data.find("div", class_="live_scores_blocks")
        while status:
            league_name = ""
            matches = []
            if start.has_attr("class"):
                if "live_scores_block" in start['class']:
                    league_name = start.text
                    start = start.next_sibling
            if start.has_attr("id"):
                semi_status = True
                if "fx" in start['id']:
                    while semi_status:
                        matches.append(start)
                        start = start.next_sibling
                        if start.has_attr("id"):
                            continue
                        semi_status = False
            if league_name and matches:
                status = True
                fixture = {"league": league_name, "matches": matches}
                self.fixtures.append(Fixture(fixture))
            else:
                status = False


class FixturesAll(BaseFundamental):
    def __init__(self, soup):
        super(FixturesAll, self).__init__(soup)
        self.fixtures_list = []
        self.process()

    def process(self):
        data = self.soup.find_all("div", id="content")[0]
        self.fixtures_list = FixturesList(data)
