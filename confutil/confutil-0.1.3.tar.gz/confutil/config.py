#!/usr/bin/env python
import os
from configobj import ConfigObj


def expand_path(path):
    new = os.path.expanduser(path)
    new = os.path.expandvars(new)
    return os.path.abspath(new)


def deep_update(dict1, update):
    for k, v in update.items():
        has = k in dict1
        dv = dict1.get(k)
        if not has:
            dict1[k] = v
            continue
        if not isinstance(v, dict):
            dict1[k] = v
            continue
        if not isinstance(dv, dict):
            dict1[k] = v
            continue
        deep_update(dv, v)


class Config(object):

    def __init__(self, name, use_env=True):
        self.__app_name__ = name
        self.__seq__ = self.__path_sequence__()
        self.__data__ = self.__load_data__()
        self.__use_env__ = use_env

    def __path_sequence__(self):
        seq = [
            './.%s.conf', './.%s.cfg',
            '~/.%s.conf', '~/.%s.cfg',
            '~/.config/.%s.conf', '~/.config/.%s.cfg',
            '~/.config/%s/config.conf', '~/.config/%s/config.cfg',
            '~/.config/%s/config',
            '/etc/.%s.conf', '/etc/.%s.cfg', '/etc/%s/config.conf',
            '/etc/%s/config.cfg', '/etc/%s/config',
        ]
        return [expand_path(p % self.__app_name__) for p in seq]

    def __load_data__(self):
        d = {}
        for path in self.__seq__[::-1]:
            if not os.path.isfile(path):
                continue
            obj = ConfigObj(path)
            deep_update(d, obj)
        return d

    def __getitem__(self, index):
        if index not in self.__data__:
            raise KeyError('Attribute not in configuration')
        if self.__use_env__:
            return os.getenv(index, self.__data__[index])
        else:
            return self.__data__[index]

    def __setitem__(self, index, val):
        self.__data__[index] = val

    def __contains__(self, obj):
        return obj in self.__data__

    def get(self, *args, **kwargs):
        return self.__data__.get(*args, **kwargs)

    def read(self, path):
        if not os.path.isfile(path):
            raise OSError('%s is not a file or does not exist' % path)
        obj = ConfigObj(path)
        deep_update(self.__data__, obj)
        return self.__data__

    def write(self, path):
        config = ConfigObj()
        for k, v in self.__data__.items():
            config[k] = v
        config.filename = path
        config.write()

    def __str__(self):
        return 'confutil.Config(%s)' % str(self.__data__)

    def __repr__(self):
        return 'confutil.Config(%s)' % repr(self.__data__)

    def get_in(self, attr, default=None):
        if not attr:
            return default
        keys = attr.split('.')
        d = self
        for key in keys:
            try:
                d = d[key]
            except:
                return default
        return d

    def get_as(self, attr, type=str):
        val = self.get_in(attr)
        if val is None:
            if type is bool:
                return False
            return None
        if type is str:
            return str(val)
        if type is int:
            return int(val)
        if type is float:
            return float(val)
        if type is bool:
            if isinstance(val, bool):
                return val
            if isinstance(val, str):
                return val.strip().lower() in ('true', 'yes', 'on', '1')
            if isinstance(val, (int, float)):
                return val > 0
            raise ValueError('trouble coercing {!r} to bool: {!r}'.format(
                attr, val))
        if type is list:
            if isinstance(val, (tuple, list, set)):
                return list(val)
            if isinstance(val, str):
                return val.split(',')
            if isinstance(val, (int, float, bool)):
                return [val]
            raise ValueError('trouble coercing {!r} to list: {!r}'.format(
                attr, val))
        if type is set:
            if isinstance(val, (tuple, list, set)):
                return set(val)
            if isinstance(val, str):
                return set(val.split(','))
            if isinstance(val, (int, float, bool)):
                return {val}
            raise ValueError('trouble coercing {!r} to set: {!r}'.format(
                attr, val))

        raise ValueError('cannot coerce {!r} to {!r}: {!r}'.format(
            attr, type, val))
