from ..schemas import UserSchema


class UserKind:
    def __init__(self, document, filename=None):
        document, errors = UserSchema().load(document)
        if errors:
            raise ValueError(errors)
        self.document = document
        self.filename = filename

    @property
    def api_resource(self):
        raise NotImplementedError('Need User Api Resource First')
