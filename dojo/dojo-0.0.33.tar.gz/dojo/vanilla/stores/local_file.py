from __future__ import absolute_import, print_function, unicode_literals

import os

from dojo.transforms import ConvertTo, ConvertFrom

from ..storage import Storage


class VanillaLocalFileStore(Storage):

    def read(self, path):
        if 'prefix' in self.config:
            path = os.path.join(self.config['prefix'], path)
        with open(path, 'r') as f:
            return [ConvertFrom().process(line) for line in f.read().decode('utf-8').split('\n') if line.strip()]

    def write(self, path, rows, format='json'):
        rows = [ConvertTo(format).process(row) for row in rows]
        output_path = '%s-00000-of-00001' % (path, )
        if 'prefix' in self.config:
            output_path = os.path.join(self.config['prefix'], output_path)
        output_dir = os.path.dirname(output_path)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        with open(output_path, 'w') as f:
            f.write('\n'.join(rows).encode('utf-8'))
