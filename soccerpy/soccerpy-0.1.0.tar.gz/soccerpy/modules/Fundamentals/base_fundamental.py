from soccerpy.modules.Fundamentals.searchable import Searchable


class BaseFundamental(Searchable):
    def __init__(self, data, request):
        super(BaseFundamental, self).__init__()
        self.data = data
        self.r = request
