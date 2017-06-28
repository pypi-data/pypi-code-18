from pathlib import Path
import itertools

import yaml

from .kinds import StructureKind, CalculationKind
from ..api.calculation import CalculationResourceItem
from ..api.structure import StructureResourceItem


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


def parse_yaml_files(paths, recursive, test):
    documents = []
    for path in paths:
        for filename, document in read_yaml_files(path):
            if 'kind' not in document:
                raise ValueError({
                    'filename': filename,
                    'errors': {'kind', 'must be specified'}
                })

            kinds = {
                'Structure': StructureKind,
                'Calculation': CalculationKind
            }

            try:
                document_kind = kinds[document['kind']](document, filename)
                if isinstance(document_kind, StructureKind) and document_kind.duplicate:
                    documents.append(document_kind.duplicate)
                else:
                    documents.append(document_kind)
            except ValueError as e:
                raise ValueError({'filename': filename, 'errors': e.args[0]})

    for document in documents:
        if isinstance(document, (CalculationKind)):
            document.determine_dependencies(documents)
    resolve_order = linearize_dependencies(documents)
    return documents, resolve_order
