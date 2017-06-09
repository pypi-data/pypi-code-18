#!/usr/bin/env python
# -*- coding: utf-8 -*-

import abc
import ast
import copy
import json
import os
import os.path as op
import sys

from collections import OrderedDict

if sys.version_info < (3,):
    import ConfigParser as cp  # pragma: nocover
else:
    import configparser as cp  # pragma: nocover


class ImmutableAttributeError(AttributeError):
    ''' Custom exception that gets raised when you try to modify an existing
    attribute. '''
    pass


class WriteOnceContainer(object):
    ''' Base container class for all configs. This is write-once sort of thing
    that tries its very very best to not let you write to a variable more than
    once. It does so by limiting access to __dict__ and making sure that when
    you are setting an attribute on an instance, the attribute does not already
    exist. That does not mean that you cannot change any existing members, you
    can do that by simply using ``object.__setattr__``, but do try not to.
    '''

    def __init__(self, missing_value=None):
        self.__keys__ = []  # quick and dirty cache
        self.__missing_value__ = missing_value

    def __setattr__(self, name, value):
        # XXX: any reason to treat _* instance members specially?
        # XXX: this will NOT stop object.__setattr__. That is by design in the
        # language itself
        attr = getattr(self, name, None)
        if not attr:
            object.__setattr__(self, name, value)
            # only the usual suspects please
            if not name.startswith('__'):
                self.__keys__.append(name)
        else:
            raise ImmutableAttributeError('Attribute %s is immutable' % name)

    def __getattr__(self, name):
        # things that start with an _ are usually control variables, we really
        # do not want to get into a recursion there
        # __getattr__ is only called when nothing is found
        if not name.startswith('__') and self.__missing_value__:
            return self.__missing_value__

        raise AttributeError("'%s' object has no attribute '%s'" %
                             (self.__class__.__name__, name))

    def __delattr__(self, name):
        raise ImmutableAttributeError('Attribute %s is immutable' % name)

    def __getattribute__(self, name):
        if name == '__dict__':
            # let it fall through to __getattr__ and raise AttributeError
            raise AttributeError

        return object.__getattribute__(self, name)

    def __getitem__(self, name):
        try:
            return getattr(self, name)
        except AttributeError:
            raise KeyError(name)

    def __iter__(self):
        return self.__keys__.__iter__()

    def __copy__(self):
        _woc = WriteOnceContainer()
        for key, value in self.items():
            setattr(_woc, key, value)
        return _woc

    def __dir__(self):
        # because we outlaw __dict__ shit breaks
        return sorted(
            set((dir(type(self))) + self.__keys__))  # pragma: nocover

    def keys(self):
        # we do not want a backdoor into messing with the key cache
        return copy.copy(self.__keys__)

    def items(self):
        return [(key, getattr(self, key)) for key in self.__keys__]

    def to_dict(self):
        res = OrderedDict()
        for key, value in self.items():
            res[key] = value
            if isinstance(value, WriteOnceContainer):
                res[key] = value.to_dict()

        return res


class AutoDefaultSectionFD(object):
    ''' By default ConfigParser will barf if you have a raw option without a
    section. However to influence the behaviour of the loader we provide raw
    options at the top. For e.g env_var which will interpret sections as
    specifed in the env_var_values option and the value in ``os.environ``.

    This class behaves like a python context (with statement) aware file
    descriptor that inserts the default section [DEFAULT] at the top of a file.

    If a default section exists, configparser will simply merge it with the
    existing one instead of raising a DuplicateSection error.
    '''

    def __init__(self, fd):
        self.fd = fd
        self.default_section = '[%s]\n' % cp.DEFAULTSECT

    def readline(self):
        if self.default_section:
            try:
                return self.default_section
            finally:
                # we inserted the default section - dont do it anymore
                self.default_section = None
        else:
            return self.fd.readline()

    # for python3
    def __iter__(self):
        while True:
            line = self.readline()
            if not line:
                raise StopIteration
            yield line

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.fd.__exit__(exc_type, exc_value, traceback)


class FileHandler(object):
    '''Base class for all handlers that actually fo the loading and parsing'''

    __metaclass__ = abc.ABCMeta

    def __init__(self, path, **defaults):
        self.path = path
        self.defaults = {}
        if defaults:
            self.defaults.update(defaults)

    @abc.abstractmethod
    def load(self, node, **load_opts):
        pass  # pragma: nocover

    @classmethod
    def get_handler(cls, path, **defaults):
        if path.endswith('.ini'):
            return INIFileHandler(path, **defaults)
        elif path.endswith('.json'):
            return JSONFileHandler(path, **defaults)

        return None

    @staticmethod
    def get_env_vars(defaults):
        ''' Sometimes we want to use alternates for env variables ie for dev,
        staging and prod. to do something like that you can specify
        env_var to be a string that will be read off of the environment. Then
        you need to define what the legitimate values are. So you need at
        least the following:
        - env_var = <something>
        - env_var_values = [<comma-sep-python-strings>]

        .. note:: The first value in env_var_values is treated as the default
        '''
        use_env_var = False
        env_var_values = []
        cur_env = None
        env_var = defaults.get('env_var')

        if env_var:
            env_var_values = defaults.get('env_var_values', [])
            default = env_var_values[0] if env_var_values else None
            cur_env = os.environ.get(env_var, default)
            if cur_env not in env_var_values:
                raise ValueError('Invalid current env: %s' % cur_env)
            use_env_var = True

        return use_env_var, env_var_values, cur_env


class INIFileHandler(FileHandler):

    @staticmethod
    def _bool(value):
        value = str(value).lower().strip()
        bools = {'yes': True, 'true': True, 'on': True,
                 'no': False, 'false': False, 'off': False}
        if value in bools:
            return bools[value]
        raise ValueError('Invalid boolean: %s' % value)

    @staticmethod
    def parse_value(value):
        value = value.strip()
        # XXX: deviates from SafeConfigParser: 1|0 evaluate to int
        for func in [int, float, INIFileHandler._bool]:
            try:
                return func(value)
            except (ValueError, TypeError):
                pass
        try:
            # maybe its a dict, list or tuple
            # in case of python3 ast can now parse {'x'} as a set
            if value and value[0] in ['[', '{', '(']:
                return ast.literal_eval(value)
        except (ValueError, SyntaxError):
            pass

        return value

    def _get_parser(self, **load_opts):
        config_parser_args = {
            'defaults': self.defaults
        }
        if load_opts.get('dict_type'):
            config_parser_args['dict_type'] = load_opts['dict_type']
        if load_opts.get('allow_no_value'):
            config_parser_args['allow_no_value'] = load_opts['allow_no_value']

        parser = cp.SafeConfigParser(**config_parser_args)
        if load_opts.get('preserve_case', False):
            parser.optionxform = str

        return parser

    def load(self, node, **load_opts):
        get_parsed_value = INIFileHandler.parse_value
        if load_opts.get('no_parse_value', False):
            # pylint: disable=R0204
            get_parsed_value = lambda x: x  # flake8: noqa

        parser = self._get_parser(**load_opts)
        with AutoDefaultSectionFD(open(self.path)) as fd:
            parser.readfp(fd)

        # parse all default options first
        for option in parser.defaults().keys():
            self.defaults[option] = get_parsed_value(
                parser.get(cp.DEFAULTSECT, option))
        use_env_var, env_var_values, cur_env = FileHandler.get_env_vars(
            self.defaults)

        for section in parser.sections():
            # in use_env_var mode if section one of legitimate env var values
            # but is not the current env, we ignore it
            if use_env_var and \
               section in env_var_values and \
               section != cur_env:
                continue

            parent = node
            if not use_env_var or section not in env_var_values:
                # if not use_env_var or a non-env-var section the section is
                # also a container.
                setattr(parent, section, WriteOnceContainer())
                parent = getattr(parent, section)

            for option in parser.options(section):
                # skip defaults and control stuff
                if option not in self.defaults.keys():
                    value = get_parsed_value(parser.get(section, option))
                    setattr(parent, option, value)


class JSONFileHandler(FileHandler):

    @staticmethod
    def walk(node, data_dict, **load_opts):
        ''' Walk the json tree and if the node is a dict, create a container
        and walk down the dict else just assign it '''
        # TODO: env vars stuff - do we really need it here
        parent = node
        key_xform = unicode if sys.version_info[0] < 3 else str
        # by default in JSON keys preserve case, hence the strange construction
        # here. we only want to enable this if preserve_case is False
        if not load_opts.get('preserve_case', True):
            key_xform = unicode.lower if sys.version_info[0] < 3 else str.lower
        for key, value in data_dict.items():
            key = key_xform(key)
            if isinstance(value, dict):
                setattr(parent, key, WriteOnceContainer())
                JSONFileHandler.walk(getattr(parent, key), value)
            else:
                setattr(parent, key, value)

    def load(self, node, **load_opts):
        data = ''
        with open(self.path) as fd:
            data = fd.read()
        data = json.loads(data, encoding=load_opts.get('encoding', 'utf8'))
        data.update(self.defaults)

        JSONFileHandler.walk(node, data, **load_opts)


class Konfig(WriteOnceContainer):

    def __init__(self, base_path, missing_value=None, **defaults):
        super(Konfig, self).__init__(missing_value=missing_value)
        self.__base_path__ = op.abspath(base_path)
        self.__defaults__ = defaults

    @staticmethod
    def generate_path_node_tree(root, base_path, file_path):
        ''' Generate a object hierarchy based on the directories in a path to a
        configuration file. For e.g. if you have a file path /a/b/c/d/e.ini
        this will create an object tree like: ```a.b.c.d``

        If you provide a valid base path object it will remove it from the
        prefix before generating the tree.
        '''
        if not isinstance(root, WriteOnceContainer):
            raise TypeError('Invalid type of root node %s' %
                            root.__class__.__name__)

        # from the left only once
        fragment = file_path.replace(base_path, '', 1)
        # so empty strings are discarded
        parts = [part for part in fragment.split(os.sep) if part]
        if not parts:
            return root
        parts[-1] = op.splitext(parts[-1])[0]

        # start with yourself if root not provided
        node = root
        # create a hierarchy of objects based on how many : in there
        for part in parts:
            # need to do a getattr or else immutable error will be raised
            if not getattr(node, part, None):
                setattr(node, part, WriteOnceContainer())
            # go down the rabbit hole
            node = getattr(node, part)
        # node is now the leaf object
        return node

    def load(self, **load_opts):
        if not op.exists(self.__base_path__):
            raise IOError('Invalid base path: %s' % self.__base_path__)
        files_loaded = []
        for root, _, files in os.walk(self.__base_path__):
            for file_name in files:
                file_path = op.abspath(op.join(root, file_name))

                handler = FileHandler.get_handler(file_path,
                                                  **(self.__defaults__))
                if handler:
                    # so that we dont create nodes for files we cannot handle
                    node = Konfig.generate_path_node_tree(self,
                                                          self.__base_path__,
                                                          file_path)
                    handler.load(node, **load_opts)
                    files_loaded.append(file_path)

        return files_loaded
