# -*- coding: utf-8 -*-
import json
import os

from gapi import AdwordsFacade


class TestFacade(AdwordsFacade):
    fixture_dir = None

    def set_fixture_dir(self, path):
        self.fixture_dir = path

    def __call__(self, name, *args, **kwargs):
        full_file_name = self._get_full_file_name(name, args, kwargs)
        if full_file_name:
            saved_result = self._read_json(full_file_name)
            if saved_result:
                return saved_result
        result = super(TestFacade, self).__call__(name, *args, **kwargs)
        if full_file_name:
            self._write_json(full_file_name, result)
        return result

    def _read_json(self, full_file_name):
        if os.path.exists(full_file_name):
            with open(full_file_name, 'r') as ff:
                return json.load(ff)

    def _write_json(self, full_file_name, result):
        with open(full_file_name, 'w') as ff:
            json.dump(result, ff)

    def _get_full_file_name(self, name, args, kwargs):
        if self.fixture_dir:
            args_part = '_'.join([self._refine_value(v) for v in args])
            kwargs_part = '_'.join(['{}={}'.format(k, self._refine_value(kwargs[k]))
                                    for k in sorted(kwargs)])
            file_name = '_'.join([args_part, kwargs_part])
            full_file_name = os.path.join(self.fixture_dir, name, file_name + '.json')
            return full_file_name

    def _refine_value(self, value):
        if isinstance(value, (list, tuple, set)):
            res = ','.join([self._refine_value(v) for v in sorted(value)])
            return '[' + res + ']'
        if isinstance(value, dict):
            res = ['{}={}'.format(k, self._refine_value(value[k])) for k in sorted(value)]
            return '{' + ','.join(res) + '}'
        return value
