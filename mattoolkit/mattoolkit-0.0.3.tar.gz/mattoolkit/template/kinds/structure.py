from pymatgen.io.cif import CifParser

from ..schemas import StructureSchema
from ...api.structure import StructureResourceItem, StructureResourceList


class StructureKind:
    def __init__(self, document, filename, search_api=True):
        document, errors = StructureSchema().load(document)
        if errors:
            raise ValueError(errors)
        self.document = document
        self.filename = filename
        if search_api:
            self._duplicate = self._search_api_for_duplicate()
        self._structure = self._parse_structure(self.document['spec']['data'], self.document['spec']['format'])

    def _search_api_for_duplicate(self):
        structures = StructureResourceList()
        structures.query(name=self.name, labels=self.labels)
        if len(structures.items) > 1:
            raise ValueError('Structure duplicates are one-to-one so not possible to have many', structures.items)
        elif len(structures.items) == 1:
            return structures.items[0]
        return None

    @property
    def name(self):
        return self.document['metadata']['name']

    @property
    def labels(self):
        return self.document['metadata'].get('labels')

    @property
    def duplicate(self):
        return self._duplicate

    @property
    def structure(self):
        return self._structure

    # @property
    # def structure_resource_item(self):
    #     return StructureResourceItem.from_structure(structure=self.structure, name=self.name, labels=self.labels)

    def _parse_structure(self, data, format):
        if format == 'cif':
            structure = (CifParser.from_string(data)).get_structures()[0]
        return structure

    def __repr__(self):
        return f'<StructureKind(filename={self.filename}, name={self.name}, labels={self.labels}>)'
