# coding: utf-8

from __future__ import print_function

import csv
import dateutil.parser
import ruamel.yaml


class CSV2YAML(object):
    def __init__(self, args=None):
        self.delimiter = getattr(args, 'delimiter', None)
        self.strip = getattr(args, 'strip', False)
        self.process = getattr(args, 'process', True)
        self.mapping = getattr(args, 'mapping', False)

    def __call__(self, csv_file_name):

        data = []
        header = None
        with open(csv_file_name) as inf:
            for line in csv.reader(inf, delimiter=self.delimiter):
                if self.strip:
                    line = [elem.strip() for elem in line]
                if self.process:
                    line = self.process_line(line, strip=self.strip)
                if not self.mapping:
                    data.append(line)
                    continue
                if header is None:
                    header = line
                    continue
                data.append(ruamel.yaml.comments.CommentedMap(zip(header, line)))
        print(ruamel.yaml.round_trip_dump(data))

    def process_line(self, line, strip=False):
        """convert lines, trying, int, float, date"""
        ret_val = []
        for elem in line:
            try:
                res = int(elem)
                ret_val.append(res)
                continue
            except ValueError:
                pass
            try:
                res = float(elem)
                ret_val.append(res)
                continue
            except ValueError:
                pass
            try:
                res = dateutil.parser.parse(elem)
                ret_val.append(res)
                continue
            except (ValueError, TypeError):  # used to throw the latter
                pass
            ret_val.append(elem)
        return ret_val
