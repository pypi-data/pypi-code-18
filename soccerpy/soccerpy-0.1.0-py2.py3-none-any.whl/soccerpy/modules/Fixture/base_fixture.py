class BaseFixture:
    def __init__(self, headers, request):
        self.headers = headers
        self.r = request
