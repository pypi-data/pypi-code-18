import os
from basePhantom import _BasePhantom

class _PhantomActions(_BasePhantom):
    """
    Wrapper around the Phantom REST calls for Assets
    """
    def __init__(self, host, username, password):
        _BasePhantom.__init__(self, host, username, password)
        self.endpoint_url = os.path.join(self.host, "action_run")

    def query(self, query=None):
        url = self.endpoint_url
        if query is not None:
            url += "?%s" % query

        return self.__make_rest_request__(url, "GET")

    def trigger(self, data):
        raise NotImplementedError()
