import requests

from .assets_service import AssetsService
from .kyc_service import KycService
from .profile_service import ProfileService
from .transactions_service import TransactionsService
from .user_service import UserService


class Client:
    def __init__(self, base_uri="https://sandbox.paycash.eu/paycash-server/v3/api"):
        self.base_url = base_uri
        self.session = requests.Session()

        self.assets = AssetsService(self)
        self.kyc = KycService(self)
        self.profile = ProfileService(self)
        self.transactions = TransactionsService(self)
        self.user = UserService(self)

    def is_goraml_class(self, data):
        # check if a data is go-raml generated class
        # we currently only check the existence
        # of as_json method
        op = getattr(data, "as_json", None)
        if callable(op):
            return True
        return False

    def set_auth_header(self, val):
        ''' set authorization header value'''
        self.session.headers.update({"Authorization": val})

    def get(self, uri, headers, params, content_type, **kwargs):
        self.session.headers.update({"Content-Type": content_type})
        res = self.session.get(uri, headers=headers, params=params, **kwargs)
        res.raise_for_status()
        return res

    def post(self, uri, data, headers, params, content_type, **kwargs):
        self.session.headers.update({"Content-Type": content_type})
        if self.is_goraml_class(data):
            data = data.as_json()

        if content_type == "multipart/form-data":
            res = self.session.post(uri, files=data, headers=headers, params=params, **kwargs)
        elif type(data) is str:
            res = self.session.post(uri, data=data, headers=headers, params=params, **kwargs)
        else:
            res = self.session.post(uri, json=data, headers=headers, params=params, **kwargs)
        res.raise_for_status()
        return res

    def put(self, uri, data, headers, params, content_type, **kwargs):
        self.session.headers.update({"Content-Type": content_type})
        if self.is_goraml_class(data):
            data = data.as_json()

        if content_type == "multipart/form-data":
            res = self.session.put(uri, files=data, headers=headers, params=params, **kwargs)
        elif type(data) is str:
            res = self.session.put(uri, data=data, headers=headers, params=params, **kwargs)
        else:
            res = self.session.put(uri, json=data, headers=headers, params=params, **kwargs)
        res.raise_for_status()
        return res

    def patch(self, uri, data, headers, params, content_type, **kwargs):
        self.session.headers.update({"Content-Type": content_type})
        if self.is_goraml_class(data):
            data = data.as_json()

        if content_type == "multipart/form-data":
            res = self.session.patch(uri, files=data, headers=headers, params=params, **kwargs)
        elif type(data) is str:
            res = self.session.patch(uri, data=data, headers=headers, params=params, **kwargs)
        else:
            res = self.session.patch(uri, json=data, headers=headers, params=params, **kwargs)
        res.raise_for_status()
        return res

    def delete(self, uri, headers, params, content_type, **kwargs):
        self.session.headers.update({"Content-Type": content_type})
        res = self.session.delete(uri, headers=headers, params=params, **kwargs)
        res.raise_for_status()
        return res
