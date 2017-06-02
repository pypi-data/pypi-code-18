import os
from basePhantom import _BasePhantom


class _PhantomAssets(_BasePhantom):
    """
    Wrapper around the Phantom REST calls for Assets
    """
    def __init__(self, host, username, password):
        _BasePhantom.__init__(self, host, username, password)
        self.endpoint_url = os.path.join(self.host, "asset")

    def get_asset(self, asset_id):
        if asset_id is None:
            raise ValueError("asset_id is required")

        url = os.path.join(self.endpoint_url, str(asset_id))
        return self.__make_rest_request__(url, "GET")

    def get_all_assets(self):
        url = self.endpoint_url + "?page_size=0"
        return self.__make_rest_request__(url, "GET")

    def create_asset(self, data):
        url = self.endpoint_url
        return self.__make_rest_request__(url, "POST", data=data)
