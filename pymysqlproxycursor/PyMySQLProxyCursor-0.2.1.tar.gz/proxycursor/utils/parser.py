# -*- coding: utf-8 -*-

import itertools
import sqlparse

from sqlparse.sql import IdentifierList, Identifier, Parenthesis, Comparison
from sqlparse.tokens import Keyword, DML


def is_subselect(parsed):
    if not parsed.is_group:
        return False
    for item in parsed.tokens:
        if item.ttype is DML and item.value.upper() == 'SELECT':
            return True
    return False


def extract_normal_part(parsed):
    for item in parsed.tokens:
        if item.is_group:
            for v in extract_normal_part(item):
                yield v

        if isinstance(item, Parenthesis):
            continue

        if isinstance(item.parent, Parenthesis):
            continue

        if isinstance(item.parent, Comparison):
            continue

        if not item.is_keyword and not item.is_whitespace:
            yield item


def extract_from_part(parsed):
    from_seen = False
    for item in parsed.tokens:
        if item.is_group:
            for v in extract_from_part(item):
                yield v
        if from_seen:
            if is_subselect(item):
                for v in extract_from_part(item):
                    yield v
            elif item.ttype in Keyword and item.value.upper() in ['ORDER', 'GROUP', 'BY', 'HAVING']:
                from_seen = False
                StopIteration
            else:
                yield item
        if item.ttype in Keyword and item.value.upper() == 'FROM':
            from_seen = True


def extract_table_identifiers(token_stream):
    for item in token_stream:
        if isinstance(item, IdentifierList):
            for identifier in item.get_identifiers():
                value = identifier.value.replace('"', '').lower()
                yield value
        elif isinstance(item, Identifier):
            value = item.value.replace('"', '').lower()
            yield value


def extract_tables(sql):
    extracted_tables = []
    statements = sqlparse.parse(sql)
    for statement in statements:
        dml_type = statement.get_type()
        if dml_type in ['INSERT', 'UPDATE']:
            stream = extract_normal_part(statement)
            extracted_tables.append(set(list(extract_table_identifiers(stream))))
        elif dml_type in ['SELECT', 'DELETE']:
            stream = extract_from_part(statement)
            extracted_tables.append(set(list(extract_table_identifiers(stream))))
    return dml_type, list(itertools.chain(*extracted_tables))
