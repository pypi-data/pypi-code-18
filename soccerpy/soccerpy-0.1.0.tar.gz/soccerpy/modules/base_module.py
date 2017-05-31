from soccerpy.requester import Requester
from soccerpy.modules.search_module import SearchModule


class BaseModule:
    def __init__(self, API_KEY, requester, response_format):
        if API_KEY:
            self.r = Requester(API_KEY=API_KEY, response_format=response_format)
        else:
            self.r = requester
        self.finder = SearchModule()
