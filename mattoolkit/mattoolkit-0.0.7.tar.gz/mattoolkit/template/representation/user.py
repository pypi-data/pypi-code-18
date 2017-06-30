from .base import BaseRepresentation
from ..schema import UserSchema
from ...api import UserResourceItem


class UserRepresentation(BaseRepresentation):
    SCHEMA = UserSchema
    RESOURCE = UserResourceItem

    def _search_api_for_duplicates(self):
        print('unable to determine if users exist through api')
        return []

    def determine_dependencies(self, candidates):
        self._dependencies = []

    def __repr__(self):
        return f'<{self.__class__.__name__}(filename={self.filename}, username={self.document["spec"]["username"]}>'
