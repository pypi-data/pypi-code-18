class BaseRepresentation:
    SCHEMA = None

    def __init__(self, document, filename, search_api=True):
        document, errors = self.SCHEMA().load(document)
        if errors:
            raise ValueError(errors)
        self.document = document
        self.filename = filename
        self._search_api = search_api
        self._duplicates = None
        if search_api:
            self._duplicates = self._search_api_for_duplicates()
        self._dependencies = None

    def _search_api_for_duplicates(self):
        raise NotImplementedError()

    def determine_dependencies(self, candidates):
        raise NotImplementedError()

    @property
    def dependencies(self):
        if self._dependencies is None:
            raise ValueError('Must call determine dependencies first')
        return self._dependencies

    @property
    def duplicates(self):
        if not self._search_api:
            raise ValueError('cannot search for duplicated without using api')
        return self._duplicates

    def __repr__(self):
        return f'<{self.__class__.__name__}(filename={self.filename}>'
