class ServiceNotAvailable(Exception):
    def __init__(self, exception):
        assert exception is not None
        self.exception = exception

    def message(self):
        return self.exception.message


class ServerException(Exception):
    def __init__(self, e):
        assert e is not None
        self.e = e

    def message(self):
        return self.e.message


class HTTPException(Exception):
    def __init__(self, e):
        assert e is not None
        self.e = e

    def message(self):
        return self.e.message