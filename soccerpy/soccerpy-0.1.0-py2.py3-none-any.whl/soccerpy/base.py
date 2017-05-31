from soccerpy.requester import Requester


class Base:
    def __init__(self, API_KEY, response_format='full'):
        self.API_KEY = API_KEY
        self.response_format = response_format
        self.requester = Requester(API_KEY=API_KEY, response_format=response_format)
