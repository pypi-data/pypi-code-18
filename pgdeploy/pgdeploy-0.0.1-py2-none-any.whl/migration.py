# -*- coding: utf-8 -*-
import os
from pgdeploy.exceptions import RollbackUnsupportedException

class Migration(object):

    ROLLBACK_DELIMITER = '--//@UNDO'

    def __init__(self, migration_number, apply_sql, rollback_sql=None):
        self._migration_number = migration_number
        self._apply_sql = apply_sql
        self._rollback_sql = rollback_sql

    @property
    def number(self):
        return self._migration_number

    def apply(self, cursor):
        cursor.execute(self._apply_sql)

    def rollback(self, cursor):
        if not self._rollback_sql:
            raise RollbackUnsupportedException()
        cursor.execute(self._rollback_sql)

    @classmethod
    def from_file(cls, abspath):
        if not os.path.exists(abspath):
            raise IOError('Migration file %s not found % abspath')

        contents = None
        with open(abspath, 'r') as sql_file:
            contents = sql_file.read()

        # Parse the file out into an apply and optional rollback method
        (apply_sql, rollback_sql) = cls.parse_text(contents)

        # Extract the migration number from the filename
        file_name = abspath.split(os.path.sep)[-1]
        migration_number = int(file_name.split('_')[0])

        return cls(migration_number, apply_sql, rollback_sql)

    @classmethod
    def parse_text(cls, sql_text):
        try:
            delimiter_index = sql_text.index(cls.ROLLBACK_DELIMITER)
            apply_sql = sql_text[:delimiter_index]
            rollback_sql = sql_text[
                delimiter_index + len(cls.ROLLBACK_DELIMITER):
            ]
            return (apply_sql, rollback_sql)
        except ValueError:
            return (sql_text, None)
