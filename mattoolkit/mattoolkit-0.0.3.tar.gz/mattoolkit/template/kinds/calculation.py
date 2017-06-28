# coding: utf-8

from .structure import StructureKind
from ..schemas import CalculationSchema
from ...api import (
    CalculationResourceItem, CalculationResourceList,
    StructureResourceList
)


class CalculationKind:
    def __init__(self, document, filename, search_api=True):
        document, errors = CalculationSchema().load(document)
        if errors:
            raise ValueError(errors)
        self.document = document
        self.filename = filename
        self._duplicates = None
        if search_api:
            self._duplicates = self._search_api_for_duplicates()
        self._dependencies = None

    def _search_api_for_duplicates(self):
        calculations = CalculationResourceList()
        calculations.query(name=self.name, labels=self.labels)
        return calculations.items

    def _search_api_for_dependencies(self):
        selector = self.document['spec']['structure']['selector']
        type_mapping = {
            'Structure': StructureResourceList,
            'Calculation': CalculationResourceList
        }
        dependencies = type_mapping[selector['type']]()
        print(selector['labels'])
        dependencies.query(labels=selector['labels'])
        return dependencies.items

    def determine_dependencies(self, candidates):
        selector = self.document['spec']['structure']['selector']
        type_mapping = {
            'Structure': StructureKind,
            'Calculation': CalculationKind
        }
        required_type = type_mapping[selector['type']]
        dependencies = []
        api_search_dependencies = self._search_api_for_dependencies()
        if api_search_dependencies:
            if len(api_search_dependencies) > 1 and selector['many'] == False:
                raise ValueError('Selector found multiple online dependencies but many was specified as False', api_search_dependencies)
            self._dependencies = api_search_dependencies
            return

        for candidate in candidates:
            if candidate is self:
                continue
            if isinstance(candidate, required_type):
                if set(selector['labels']) <= set(candidate.labels):
                    dependencies.append(candidate)
        if len(dependencies) > 1 and selector['many'] == False:
            raise ValueError('Selector found multiple dependencies but many was specified as False')
        elif len(dependencies) == 0:
            raise ValueError('Could not resolve dependencies for document', self)
        self._dependencies = dependencies

    @property
    def name(self):
        return self.document['metadata']['name']

    @property
    def labels(self):
        return self.document['metadata'].get('labels')

    @property
    def many(self):
        return self.document['spec']['structure']['selector']['many']

    @property
    def duplicates(self):
        return self._duplicates

    @property
    def dependencies(self):
        if self._dependencies is None:
            raise ValueError('Must call determine dependencies first!')
        return self._dependencies

    def __repr__(self):
        return f'<CalculationKind(filename={self.filename}, name={self.name}, labels={self.labels}>'

    def __str__(self):
        labels_string = '\n'.join('│    ├── %s' % label for label in self.labels)
        dependencies_string = '\n'.join('     ├── %s' % repr(dependency) for dependency in self.dependencies)
        return f'Calculation: {self.name}\n├── labels\n{labels_string}\n└── dependencies\n{dependencies_string}\n'
