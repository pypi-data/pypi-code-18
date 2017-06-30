from .base import BaseRepresentation
from ..schema import UserSchema


class UserRepresentation(BaseRepresentation):
    SCHEMA = UserSchema

    def _search_api_for_duplicates(self):
        print('unable to determine if users exist through api')
        return []

    def determine_dependencies(self, candidates):
        self._dependencies = []

    def __repr__(self):
        return f'<{self.__class__.__name__}(filename={self.filename}, username={self.document["spec"]["username"]}>'
