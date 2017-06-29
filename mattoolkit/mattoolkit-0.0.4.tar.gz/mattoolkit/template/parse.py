from pathlib import Path
import itertools

import yaml

from .representation import (
    StructureRepresentation, CalculationRepresentation,
    ClusterRepresentation, UserRepresentation
)
from ..api import CalculationResourceItem, StructureResourceItem


def read_yaml_files(path):
    filepath = Path(path)
    for yaml_file in itertools.chain(filepath.glob('**/*.yaml'),
                                     filepath.glob('**/*.yml')):
        for yaml_document in yaml.load_all(yaml_file.open()):
            yield (str(yaml_file), yaml_document)


def linearize_dependencies(documents):
    # Hack to linearize resolve order
    resolve_order = []
    while len(resolve_order) < len(documents):
        resolve_order_added = []
        for document in documents:
            if document in resolve_order:
                continue
            elif isinstance(document, (StructureKind, StructureResourceItem, CalculationResourceItem)):
                resolve_order_added.append(document)
                continue
            document_dependency_satisfied = True
            for dependency in document.dependencies:
                if isinstance(dependency, (StructureResourceItem, CalculationResourceItem)):
                    continue
                if dependency not in resolve_order:
                    document_dependency_satisfied = False
            if document_dependency_satisfied:
                resolve_order_added.append(document)
        if len(resolve_order_added) == 0:
            raise ValueError('Unable to linearize dependencies curently resolved list', resolve_order)
        resolve_order.extend(resolve_order_added)
    return resolve_order


def parse_yaml_files(paths, recursive, test, search_api=True):
    # TODO: listen to recursive argument
    # TODO: test make do something
    representations = []
    for path in paths:
        for filename, document in read_yaml_files(path):
            if 'kind' not in document:
                raise ValueError({
                    'filename': filename,
                    'errors': {'kind', 'must be specified'}
                })

            kinds_map = {
                'Structure': StructureRepresentation,
                'Calculation': CalculationRepresentation,
                'Cluster': ClusterRepresentation,
                'User': UserRepresentation
            }

            try:
                representation = kinds_map[document['kind']](document, filename, search_api=search_api)
                representations.append(representation)
            except ValueError as e:
                raise ValueError({'filename': filename, 'errors': e.args[0]})

    for representation in representations:
        representation.determine_dependencies(representations)
    # resolved_order = linearize_dependencies(representations)
    return representations, []
