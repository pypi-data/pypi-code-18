import os
from basePhantom import _BasePhantom


class _PhantomApps(_BasePhantom):
    def __init__(self, host, username, password):
        _BasePhantom.__init__(self, host, username, password)
        self.endpoint_url = os.path.join(self.host, "app")

    def get_all_apps(self):
        url = self.endpoint_url + "?page_size=0"
        return self.__make_rest_request__(url, "GET")

    def get_app(self, app_id):
        if app_id is None:
            raise ValueError("app_id is required")

        url = os.path.join(self.endpoint_url, str(app_id))
        return self.__make_rest_request__(url, "GET")
