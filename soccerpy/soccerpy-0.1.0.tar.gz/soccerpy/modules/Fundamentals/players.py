from soccerpy.modules.Fundamentals.base_fundamental import BaseFundamental
from collections.abc import Sequence
from soccerpy.modules.Fundamentals.master import Master


class Players(BaseFundamental, Sequence):
    def __len__(self):
        return len(self.players)

    def __getitem__(self, index):
        return self.players[index]

    def __init__(self, data, request):
        super(Players, self).__init__(data, request)
        self.players = []
        self.process()

    def process(self):
        for player in self.data:
            self.players.append(Player(player, self.r))

    def explicit_search(self, players, query):
        status = self.finder.search_for_player_by_name(players, query=query)
        if status:
            return status
        return "Not Found"

    def search_by_name(self, query):
        dataset = self.players
        return self.explicit_search(dataset, query=query)


class Player(Master):
    def __init__(self, player, request):
        super().__init__(request)
        self.name = player['name']
        self.position = player['position']
        self.jersey_number = player['jerseyNumber']
        self.date_of_birth = player['dateOfBirth']
        self.nationality = player['nationality']
        self.contract_until = player['contractUntil']
        self.market_value = player['marketValue']
