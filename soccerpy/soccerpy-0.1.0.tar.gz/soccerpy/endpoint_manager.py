class EndpointManager:
    def __init__(self):
        self.base_url = "http://api.football-data.org"
        self.endpoints = self.get_endpoints()

    def get_endpoints(self):
        endpoints = {
            'competitions': self.base_url + '/v1/competitions/',
            'competitions_specific': self.base_url + '/v1/competitions/{}',
            'competition_teams': self.base_url + '/v1/competitions/{}/teams',
            'competition_league_table': self.base_url + '/v1/competitions/{}/leagueTable',
            'competition_fixtures': self.base_url + '/v1/competitions/{}/fixtures',
            'fixtures': self.base_url + '/v1/fixtures/',
            'fixture_specific': self.base_url + '/v1/fixtures/{}',
            'team': self.base_url + '/v1/teams/{}',
            'team_fixtures': self.base_url + '/v1/teams/{}/fixtures/',
            'team_players': self.base_url + '/v1/teams/{}/players',
        }
        return endpoints

    def get_endpoint(self, name):
        return self.endpoints[name]
