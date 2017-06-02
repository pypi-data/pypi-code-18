from __future__ import unicode_literals

import os
import json
import MySQLdb
import apache_beam as beam

from datetime import datetime

from dojo_beam.dataset import BeamDataset
from dojo_beam.transform import ConvertFrom, DistinctBy


class FetchMySQLRows(beam.DoFn):

    def __init__(self, config, secrets):
        self.config = config
        self.secrets = secrets
        self.conn = None

    def process(self, query):
        print(query)
        if self.conn is None:
            self.conn = MySQLdb.connect(host=self.config['connection']['host'],
                                        user=self.config['connection']['user'],
                                        passwd=self.secrets['connection']['password'],
                                        db=self.config['connection']['database'])
        cursor = self.conn.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query['sql'])
        rows = [self._decode_row(row) for row in cursor.fetchall()]
        return rows

    def _decode_row(self, row):
        for key, value in row.items():
            if isinstance(value, (str, unicode)):
                row[key] = value.decode('latin1')
        return row


class MySQLSource(BeamDataset):

    BATCH_SIZE = 1000

    def process(self, inputs):
        conn = MySQLdb.connect(host=self.config['connection']['host'],
                               user=self.config['connection']['user'],
                               passwd=self.secrets['connection']['password'],
                               db=self.config['connection']['database'])
        cursor = conn.cursor()
        cursor.execute(self.config['bounds_sql'])
        min_offset, max_offset = cursor.fetchone()
        batch_size = self.config.get('batch_size', self.BATCH_SIZE)
        print(json.dumps({'min_offset': min_offset, 'max_offset': max_offset, 'batch_size': batch_size}))

        queries = [self._build_part_query(offset, offset + batch_size) for offset in range(min_offset, max_offset, batch_size)]
        queries_path = os.path.join(self.output_path(), 'queries.json')
        self.store.write_file(queries_path, queries)
        queries = self.store.read_file(queries_path) | beam.ParDo(ConvertFrom())

        return (queries | beam.ParDo(FetchMySQLRows(self.config, self.secrets)))

    def _build_part_query(self, start_offset, end_offset):
        return {
            'start_offset': start_offset,
            'end_offset': end_offset,
            'sql': self.config['sql'].format(start_offset=start_offset, end_offset=end_offset)
        }
