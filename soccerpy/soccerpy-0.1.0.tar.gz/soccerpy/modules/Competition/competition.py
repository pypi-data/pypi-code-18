from soccerpy.modules.Competition.competition_fixtures import CompetitionFixtures
from soccerpy.modules.Competition.competition_specific import CompetitionSpecific
from soccerpy.modules.Competition.competition_league_table import CompetitionLeagueTable
from soccerpy.modules.Competition.competition_teams import CompetitionTeams
from soccerpy.modules.Competition.competitions_all import CompetitionsAll
from soccerpy.modules.base_module import BaseModule


class Competition(BaseModule):
    def __init__(self, API_KEY="", requester=None, response_format='full'):
        super(Competition, self).__init__(API_KEY, requester, response_format=response_format)

    def get(self, season=None, raw=False):
        data, headers = self.r.request('competitions', payload={"season": season})
        if raw:
            return data
        return CompetitionsAll(data, headers, self.r)

    def get_all(self):
        return self.get()

    def get_by_season(self, season):
        return self.get(season=season)

    def get_specific(self, competition_id):
        data, headers = self.r.request('competitions_specific', endpoint_format=competition_id)
        return CompetitionSpecific(data, headers, self.r)

    def get_teams(self, competition_id):
        data, headers = self.r.request('competition_teams', endpoint_format=competition_id)
        return CompetitionTeams(data, headers, self.r)

    def get_league_table(self, competition_id, matchday=None):
        data, headers = self.r.request('competition_league_table', endpoint_format=competition_id,
                                       payload={'matchday': matchday})
        return CompetitionLeagueTable(data, headers, self.r)

    def get_league_table_by_matchday(self, competition_id, matchday):
        return self.get_league_table(competition_id, matchday=matchday)

    def get_fixtures(self, competition_id, matchday=None, time_frame=None):
        data, headers = self.r.request('competition_fixtures', endpoint_format=competition_id,
                                       payload={'matchday': matchday,
                                                'timeFrame': time_frame})
        return CompetitionFixtures(data, headers, self.r)

    def get_fixtures_by_matchday(self, competition_id, matchday):
        return self.get_fixtures(competition_id, matchday=matchday)

    def get_fixtures_by_time_frame(self, competition_id, time_frame):
        return self.get_fixtures(competition_id, time_frame=time_frame)

    def get_fixtures_by_matchday_and_time_frame(self, competition_id, matchday, time_frame):
        return self.get_fixtures(competition_id, matchday=matchday, time_frame=time_frame)

    def explicit_search(self, competitions, query, searching_parameter="name"):
        if searching_parameter.lower() == "name":
            status = self.finder.search_for_competition_by_name(competitions, query=query)
        else:
            status = self.finder.search_for_competition_by_code(competitions, query=query)
        if status:
            return status
        return "Not Found"

    def search_by_name(self, query, competitions=None):
        if competitions:
            dataset = competitions
        else:
            dataset = self.get_all().competitions
        return self.explicit_search(dataset, query=query, searching_parameter="name")

    def search_by_code(self, query, competitions=None):
        if competitions:
            dataset = competitions
        else:
            dataset = self.get_all().competitions
        return self.explicit_search(dataset, query=query, searching_parameter="code")
