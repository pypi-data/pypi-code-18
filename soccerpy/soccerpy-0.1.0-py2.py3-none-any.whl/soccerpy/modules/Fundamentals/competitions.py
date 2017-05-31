from soccerpy.modules.Fundamentals.base_fundamental import BaseFundamental
from soccerpy.modules.Fundamentals.master import Master
from collections.abc import Sequence


class Competitions(BaseFundamental, Sequence):
    def __len__(self):
        return len(self.competitions)

    def __getitem__(self, index):
        return self.competitions[index]

    def __init__(self, data, request):
        super(Competitions, self).__init__(data, request)
        self.competitions = []
        self.process()

    def process(self):
        for competition in self.data:
            self.competitions.append(Competition(competition, self.r))

    def explicit_search(self, competitions, query, searching_parameter="name"):
        if searching_parameter.lower() == "name":
            status = self.finder.search_for_competition_by_name(competitions, query=query)
        else:
            status = self.finder.search_for_competition_by_code(competitions, query=query)
        if status:
            return status
        return "Not Found"

    def search_by_name(self, query):
        dataset = self.competitions
        return self.explicit_search(dataset, query=query, searching_parameter="name")

    def search_by_code(self, query):
        dataset = self.competitions
        return self.explicit_search(dataset, query=query, searching_parameter="code")


class Competition(Master):
    def __init__(self, competition, request):
        super(Competition, self).__init__(request)
        self.links = Links(competition['_links'])
        self.id = competition['id']
        self.caption = competition['caption']
        self.league = competition['league']
        self.year = competition['year']
        self.current_matchday = competition['currentMatchday']
        self.number_of_matchdays = competition['numberOfMatchdays']
        self.number_of_teams = competition['numberOfTeams']
        self.number_of_games = competition['numberOfGames']
        self.last_updated = competition['lastUpdated']

    def get(self):
        data, headers = self.r.request(raw_url=self.links.url)
        return Competition(data, self.r)

    def teams(self):
        from soccerpy.modules.Team.team_specific import TeamSpecific
        data, headers = self.r.request(raw_url=self.links.teams)
        return TeamSpecific(data, headers, self.r)

    def fixtures(self):
        from soccerpy.modules.Fixture.fixtures_all import FixturesAll
        data, headers = self.r.request(raw_url=self.links.fixtures)
        return FixturesAll(data, headers, self.r)

    def league_table(self):
        from soccerpy.modules.Competition.competition_league_table import CompetitionLeagueTable
        data, headers = self.r.request(raw_url=self.links.league_table)
        return CompetitionLeagueTable(data, headers, self.r)


class Links:
    def __init__(self, links):
        self.url = links['self']['href']
        self.teams = links['teams']['href']
        self.fixtures = links['fixtures']['href']
        self.league_table = links['leagueTable']['href']
