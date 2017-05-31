class EndpointManager:
    def __init__(self):
        self.base_url = "http://www.sportsmole.co.uk/football"
        self.endpoints = self.get_endpoints()

    def get_endpoints(self):
        endpoints = {
            'news': self.base_url + '/news/',
            'transfer_talk': self.base_url + '/transfer-talk/',
            'competition_stats': self.base_url + '/{}/{}/',
            'competition_news': self.base_url + '/{}/',
            'fixtures': self.base_url + '/live-scores/',
            'team': self.base_url + '/{}/',
            'team_news': self.base_url + '/{}/news/',
            'team_fixtures': self.base_url + '/{}/{}/fixtures-and-results.html',
            'team_top_scorers': self.base_url + '/{}/{}/top-scorers.html',
            'team_transfer_talk': self.base_url + '/{}/transfer-talk/',
            'team_injury_news': self.base_url + '/{}/injury-news/',
        }
        return endpoints

    def get_endpoint(self, name):
        return self.endpoints[name]
