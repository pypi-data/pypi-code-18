#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy
import os
import os.path as op
import sys

if sys.version_info[0] < 3:
    import ConfigParser as cp
else:
    import configparser as cp  # pylint: disable=F0401

import nose.tools as nt
import mock

from kon import AutoDefaultSectionFD
from kon import WriteOnceContainer
from kon import ImmutableAttributeError
from kon import FileHandler
from kon import INIFileHandler
from kon import JSONFileHandler
from kon import Konfig


class TestAutoDefaultSectionFD(object):

    VALUES = {
        'x': (cp.DEFAULTSECT, '2'),
        'y': (cp.DEFAULTSECT, '3'),
        'a': ('s', '1'),
        'b': ('s', '2'),
        'c': ('s', 'd'),
        'd': ('s', '3')
    }

    @staticmethod
    def _check_parser_results(filename, opts):
        parser = cp.SafeConfigParser()
        with AutoDefaultSectionFD(open(op.join('test-data', filename))) as fd:
            parser.readfp(fd)

        sections = parser.sections()
        # default section is not counted
        nt.eq_(len(sections), 1)
        nt.assert_in('s', sections)
        for opt in opts:
            section, value = TestAutoDefaultSectionFD.VALUES[opt]
            nt.eq_(parser.get(section, opt,), value)

    def test_load(self):
        for filename, opts in [
            ('auto_default_no_default_section.ini', ('a', 'b', 'c')),
            ('auto_default_with_default_section.ini', ('x', 'a', 'b', 'c')),
            ('auto_default_with_raw_default_section.ini',
                ('x', 'a', 'b', 'c')),
            ('auto_default_with_mixed_default_section.ini',
                ('x', 'y', 'a', 'b', 'c', 'd'))]:
            test_name = op.splitext(filename)[0]

            def checker(filename, opts):
                self._check_parser_results(filename, opts)

            checker.description = test_name
            yield checker, filename, opts

    # python2x does explicit readline in configparser, so we do need to test the
    # iterator for python2x
    def test_iterator(self):
        lines = []
        parser = cp.SafeConfigParser()
        with AutoDefaultSectionFD(
            open(op.join('test-data',
                         'auto_default_no_default_section.ini'))) as fd:
            for line in fd:
                lines.append(line.strip())

        nt.eq_(lines, ['[DEFAULT]', '[s]', 'a = 1', 'b = 2', 'c = d'])


class TestWriteOnceContainer(object):

    def setup(self):
        self.woc = WriteOnceContainer()

    def test_woc_get_ok(self):
        self.woc.a = 1
        nt.eq_(self.woc.a, 1)

    @nt.raises(AttributeError)
    def test_woc_get_no_missing_value_error(self):
        self.woc.a

    def test_woc_get_missing_value(self):
        woc2 = WriteOnceContainer(missing_value=12)
        nt.eq_(woc2.a, 12)
        nt.assert_not_in('a', woc2.keys())

    def test_woc_set_ok(self):
        self.woc.a = 1
        self.woc.b = 2
        nt.ok_(hasattr(self.woc, 'a'))
        nt.ok_(hasattr(self.woc, 'b'))
        nt.eq_(self.woc.a, 1)
        nt.eq_(self.woc.b, 2)

    @nt.raises(ImmutableAttributeError)
    def test_woc_attr_set_error(self):
        self.woc.a = 1
        self.woc.a = 2

    @nt.raises(ImmutableAttributeError)
    def test_woc_setattr_error(self):
        self.woc.a = 1
        setattr(self.woc, 'a', 2)

    @nt.raises(ImmutableAttributeError)
    def test_woc_attr_del_error(self):
        self.woc.a = 1
        del self.woc.a

    @nt.raises(ImmutableAttributeError)
    def test_woc_delattr_error(self):
        self.woc.a = 1
        delattr(self.woc, 'a')

    def test_woc_object___setattr___ok(self):
        self.woc.a = 1
        object.__setattr__(self.woc, 'a', 2)
        nt.ok_(hasattr(self.woc, 'a'))
        nt.eq_(self.woc.a, 2)

    def test_woc_object___delattr___ok(self):
        self.woc.a = 1
        object.__delattr__(self.woc, 'a')
        nt.ok_(not hasattr(self.woc, 'a'))

    def test_woc_getitem(self):
        self.woc.a = 1
        nt.eq_(self.woc['a'], 1)

    @nt.raises(KeyError)
    def test_woc_getitem_error(self):
        self.woc['a']

    def test_woc_iter(self):
        self.woc.a = 1
        self.woc.b = 2
        self.woc.c = 3
        nt.assert_in('a', self.woc)
        nt.assert_in('b', self.woc)
        nt.assert_in('c', self.woc)
        res = []
        for key in self.woc:
            res.append(key)
        nt.eq_(res, ['a', 'b', 'c'])

    def test_woc_keys(self):
        self.woc.a = 1
        self.woc.b = 2
        self.woc.c = 3
        nt.eq_(self.woc.keys(), ['a', 'b', 'c'])

    def test_woc_keys_different_object(self):
        self.woc.a = 1
        nt.assert_not_equal(id(self.woc.keys()), id(self.woc.__keys__))

    def test_woc_single_undescore_attr_in_keys(self):
        self.woc._a= 1
        self.woc._a_= 2
        nt.assert_in('_a', self.woc.keys())
        nt.assert_in('_a_', self.woc.keys())
        nt.eq_(self.woc._a, 1)
        nt.eq_(self.woc._a_, 2)

    def test_woc_double_undescore_attr_not_in_keys(self):
        # cannot test __a, its nominally private
        self.woc.__a__ = 1
        nt.assert_not_in('__a__', self.woc.keys())
        nt.eq_(self.woc.__a__, 1)

    def test_woc_items(self):
        self.woc.a = 1
        self.woc.b = 2
        self.woc.c = 3
        nt.eq_(self.woc.items(), [('a', 1), ('b', 2), ('c', 3)])

    def test_woc_single_undescore_attr_in_items(self):
        self.woc.a = 1
        self.woc._b = 2
        self.woc._c_ = 3
        nt.eq_(self.woc.items(), [('a', 1), ('_b', 2), ('_c_', 3)])

    def test_woc_double_undescore_attr_not_in_items(self):
        self.woc.a = 1
        self.woc.__b__ = 2
        nt.eq_(self.woc.items(), [('a', 1)])

    def test_woc_to_dict(self):
        self.woc.a = 1
        self.woc.b = 'a'
        self.woc.c = 3.0
        self.woc.d = True
        self.woc.e = [1, 'a', 3.0, True]
        self.woc.f = (1, 'a', 3.0, True)
        woc2 = WriteOnceContainer()
        woc2.a = 1
        woc2.b = 'a'
        woc2.c = 3.0
        woc2.d = True
        self.woc.g = woc2

        expected = {
            'a': 1,
            'b': 'a',
            'c': 3.0,
            'd': True,
            'e': [1, 'a', 3.0, True],
            'f': (1, 'a', 3.0, True),
            'g': {
                'a': 1,
                'b': 'a',
                'c': 3.0,
                'd': True
            }
        }
        nt.eq_(self.woc.to_dict(), expected)

    def test_woc_copy(self):
        self.woc.a = 1
        self.woc.b = 'a'
        self.woc.c = 3.0
        self.woc.d = True

        woc2 = copy.copy(self.woc)
        nt.eq_(self.woc.to_dict(), woc2.to_dict())

    @nt.raises(AttributeError)
    def test_woc___dict___access_error(self):
        self.woc.__dict__

    @nt.raises(AttributeError)
    def test_woc___dict___getattr_error(self):
        getattr(self.woc, '__dict__')


class TestFileHandler(object):

    class TestHandler(FileHandler):
        def load(self, node):
            self.a = 1

    def test_ctor(self):
        hnd = TestFileHandler.TestHandler('/tmp')
        nt.eq_(hnd.path, '/tmp')
        nt.eq_(hnd.defaults, {})

    def test_ctor_with_kwargs(self):
        hnd = TestFileHandler.TestHandler('/tmp', a=1, b=2)
        nt.eq_(hnd.path, '/tmp')
        nt.eq_(hnd.defaults, {'a': 1, 'b':2})

    def test_get_handler(self):
        hnd = FileHandler.get_handler('a.ini')
        nt.assert_is_instance(hnd, INIFileHandler)
        hnd = FileHandler.get_handler('a.json')
        nt.assert_is_instance(hnd, JSONFileHandler)
        hnd = FileHandler.get_handler('a')
        nt.assert_is_none(hnd)
        hnd = FileHandler.get_handler('a.exe')
        nt.assert_is_none(hnd)

    def test_get_handler_kwargs_passthrough(self):
        hnd = FileHandler.get_handler('a.ini', a=1)
        nt.assert_in('a', hnd.defaults)
        nt.eq_(hnd.defaults, {'a': 1})
        hnd = FileHandler.get_handler('a.json', a=1)
        nt.assert_in('a', hnd.defaults)
        nt.eq_(hnd.defaults, {'a': 1})

    def test_get_handler_load_called(self):
        hnd = TestFileHandler.TestHandler('/tmp', a=1, b=2)
        hnd.load(None)
        nt.ok_(hasattr(hnd, 'a'))
        nt.eq_(hnd.a, 1)

    def test_get_env_var_no_env_var(self):
        use, vals, cur = FileHandler.get_env_vars({})
        nt.eq_(use, False)
        nt.eq_(vals, [])
        nt.eq_(cur, None)

    def test_get_env_var_ok(self):
        os.environ['TEST_KON_ENV'] = 'dev'
        use, vals, cur = FileHandler.get_env_vars(
            {'env_var': 'TEST_KON_ENV',
             'env_var_values': ['dev']})
        nt.eq_(use, True)
        nt.eq_(vals, ['dev'])
        nt.eq_(cur, 'dev')
        del os.environ['TEST_KON_ENV']

    @nt.raises(ValueError)
    def test_get_env_var_err(self):
        os.environ['TEST_KON_ENV'] = 'dev'
        try:
            use, vals, cur = FileHandler.get_env_vars(
                {'env_var': 'TEST_KON_ENV'})
        except:
            del os.environ['TEST_KON_ENV']
            raise

    def test_get_env_var_multiple_ok(self):
        os.environ['TEST_KON_ENV'] = 'staging'
        use, vals, cur = FileHandler.get_env_vars(
            {'env_var': 'TEST_KON_ENV',
             'env_var_values': ['dev', 'staging', 'prod']})
        nt.eq_(use, True)
        nt.eq_(vals, ['dev', 'staging', 'prod'])
        nt.eq_(cur, 'staging')
        del os.environ['TEST_KON_ENV']

    def test_get_env_var_default(self):
        use, vals, cur = FileHandler.get_env_vars(
            {'env_var': 'TEST_KON_ENV',
             'env_var_values': ['dev', 'staging', 'prod']})
        nt.eq_(use, True)
        nt.eq_(vals, ['dev', 'staging', 'prod'])
        nt.eq_(cur, 'dev')


class TestINIFileHandler(object):

    def setup(self):
        self.base = WriteOnceContainer()

    def _load(self, path, **load_opts):
        hnd = FileHandler.get_handler(path)
        hnd.load(self.base, **load_opts)
        return hnd

    @nt.raises(IOError)
    def test_non_existant_path(self):
        self._load('/does/not/exist/test.ini')

    def test_section_object_creation(self):
        hnd = self._load('test-data/parse_values.ini')
        nt.ok_(hasattr(self.base, 'data'))

    def test_parse_values_int(self):
        hnd = self._load('test-data/parse_values.ini')
        nt.ok_(hasattr(self.base.data, 'a'))
        nt.assert_is_instance(self.base.data.a, int)
        nt.eq_(self.base.data.a, 1)

    def test_parse_values_float(self):
        hnd = self._load('test-data/parse_values.ini')
        nt.ok_(hasattr(self.base.data, 'b'))
        nt.assert_is_instance(self.base.data.b, float)
        nt.eq_(self.base.data.b, 1.1)

    def test_parse_values_bool(self):

        def checker(self, idx):
            # here because of setup issues
            hnd = self._load('test-data/parse_values.ini')
            name = 'c%d' % (idx)
            nt.ok_(hasattr(self.base.data, name))
            nt.assert_is_instance(getattr(self.base.data, name), bool)
            nt.eq_(getattr(self.base.data, name), idx % 2 != 0)

        for idx in [1, 2, 3, 4]:
            checker.description = 'test_parse_values_bool_%d' % idx
            checker.setup = self.setup()
            yield checker, self, idx

    def test_parse_values_bool_int_not_bool(self):
        hnd = self._load('test-data/parse_values.ini')
        nt.ok_(hasattr(self.base.data, 'c5'))
        nt.assert_is_instance(self.base.data.c5, int)

    def test_parse_values_list(self):
        hnd = self._load('test-data/parse_values.ini')
        nt.ok_(hasattr(self.base.data, 'd'))
        nt.assert_is_instance(self.base.data.d, list)
        nt.eq_(self.base.data.d, [1])

    def test_parse_values_dict(self):
        hnd = self._load('test-data/parse_values.ini')
        nt.ok_(hasattr(self.base.data, 'e'))
        nt.assert_is_instance(self.base.data.e, dict)
        nt.eq_(self.base.data.e, {'a': 1})

    def test_parse_values_tuple(self):
        hnd = self._load('test-data/parse_values.ini')
        nt.ok_(hasattr(self.base.data, 'f'))
        nt.assert_is_instance(self.base.data.f, tuple)
        nt.eq_(self.base.data.f, (1,))

    def test_parse_values_default(self):
        hnd = self._load('test-data/parse_values.ini')
        nt.ok_(hasattr(self.base.data, 'h'))
        nt.assert_is_instance(self.base.data.h, str)
        nt.eq_(self.base.data.h, 'string')

    def test_parse_values_invalid_fallthrough(self):
        hnd = self._load('test-data/parse_values.ini')
        nt.ok_(hasattr(self.base.data, 'g'))
        nt.ok_(hasattr(self.base.data, 'g3'))
        if sys.version_info[0] < 3:
            nt.assert_is_instance(self.base.data.g, str)
            nt.eq_(self.base.data.g, "{'hello'}")
        else:
            nt.assert_is_instance(self.base.data.g, set)
            nt.eq_(self.base.data.g, {'hello'})
        nt.assert_is_instance(self.base.data.g3, str)
        nt.eq_(self.base.data.g3, "'b")
        nt.assert_is_instance(self.base.data.g4, str)
        nt.eq_(self.base.data.g4, "{'hello")

    @nt.raises(ValueError)
    def test__bool_parsing_error_1(self):
        INIFileHandler._bool(1)

    @nt.raises(ValueError)
    def test__bool_parsing_error_str(self):
        INIFileHandler._bool('')

    @nt.raises(ValueError)
    def test__bool_parsing_error_None(self):
        INIFileHandler._bool(None)

    def test_load_sections(self):
        sb = self.base
        self._load('test-data/load.ini')

        nt.ok_(hasattr(sb, 'a'))
        nt.ok_(hasattr(sb, 'b'))
        nt.ok_(hasattr(sb, 'd'))

        nt.ok_(hasattr(sb.a, 'a'))
        nt.ok_(hasattr(sb.a, 'b'))
        nt.ok_(hasattr(sb.b, 'c'))
        nt.ok_(hasattr(sb.d, 'e'))
        nt.ok_(hasattr(sb.d, 'f'))
        nt.ok_(hasattr(sb.d, 'g'))

        nt.eq_(sb.a.a, 1)
        nt.eq_(sb.a.b, True)
        nt.eq_(sb.b.c, 2.3)
        nt.eq_(sb.d.e, [1, 'f', True, 2.1])
        nt.eq_(sb.d.f, ('a', 2))
        nt.eq_(sb.d.g, {'a': 1})

    def test_load_use_env_var(self):
        os.environ['TEST_KON_ENV'] = 'staging'
        sb = self.base
        self._load('test-data/use_env_var.ini')
        nt.ok_(hasattr(sb, 'a'))
        nt.ok_(hasattr(sb, 'c'))
        nt.eq_(sb.a, 2)
        nt.eq_(sb.c, 3)
        del os.environ['TEST_KON_ENV']

    def test_load_use_env_var_default(self):
        sb = self.base
        self._load('test-data/use_env_var.ini')
        nt.ok_(hasattr(sb, 'a'))
        nt.ok_(hasattr(sb, 'b'))
        nt.eq_(sb.a, 1)
        nt.eq_(sb.b, 2)

    def test_load_use_env_var_non_env_var(self):
        os.environ['TEST_KON_ENV'] = 'staging'
        sb = self.base
        self._load('test-data/use_env_var.ini')
        nt.ok_(hasattr(sb, 'a'))
        nt.ok_(hasattr(sb, 'c'))
        nt.ok_(hasattr(sb, 'nonenv'))
        nt.ok_(hasattr(sb.nonenv, 'a'))
        nt.ok_(hasattr(sb.nonenv, 'b'))
        nt.eq_(sb.nonenv.a, 1)
        nt.eq_(sb.nonenv.b, 2)
        del os.environ['TEST_KON_ENV']

    def test__get_parser_with_options(self):
        sb = self.base
        target_mod = 'ConfigParser' \
            if sys.version_info[0] < 3 else 'configparser'
        with mock.patch('%s.SafeConfigParser' % target_mod,
                        spec=cp.SafeConfigParser) as scp:
            hnd = self._load('test-data/use_env_var.ini',
                             dict_type=dict, allow_no_value=True)
            scp.assert_called_with(defaults=hnd.defaults,
                                   dict_type=dict, allow_no_value=True)

    def test_load_options_no_parse_value(self):
        sb = self.base
        self._load('test-data/load.ini', no_parse_value=True)

        nt.ok_(isinstance(sb.a.a, str))
        nt.ok_(isinstance(sb.a.b, str))
        nt.ok_(isinstance(sb.b.c, str))
        nt.ok_(isinstance(sb.d.e, str))
        nt.ok_(isinstance(sb.d.f, str))
        nt.ok_(isinstance(sb.d.g, str))

    def test_load_options_do_parse_value(self):
        sb = self.base
        self._load('test-data/load.ini', no_parse_value=False)

        nt.ok_(isinstance(sb.a.a, int))
        nt.ok_(isinstance(sb.a.b, bool))
        nt.ok_(isinstance(sb.b.c, float))
        nt.ok_(isinstance(sb.d.e, list))
        nt.ok_(isinstance(sb.d.f, tuple))
        nt.ok_(isinstance(sb.d.g, dict))

    def test_load_with_options_case_sensitive(self):
        sb = self.base
        self._load('test-data/case-sensitive.ini', preserve_case=True)
        nt.ok_(hasattr(sb.data, 'a'))
        nt.ok_(hasattr(sb.data, 'B'))
        nt.ok_(not hasattr(sb.data, 'b'))
        nt.eq_(sb.data.B, 'hello')

    def test_load_with_options_case_insensitive(self):
        sb = self.base
        self._load('test-data/case-sensitive.ini', preserve_case=False)
        nt.ok_(hasattr(sb.data, 'a'))
        nt.ok_(hasattr(sb.data, 'b'))
        nt.ok_(not hasattr(sb.data, 'B'))
        nt.eq_(sb.data.b, 'hello')


class TestJSONFileHandler(object):

    def setup(self):
        self.base = WriteOnceContainer()
        hnd = FileHandler.get_handler('test-data/data.json')
        hnd.load(self.base)

    def test_load(self):
        sb = self.base
        nt.ok_(hasattr(sb, 'a'))
        nt.ok_(hasattr(sb, 'b'))
        nt.ok_(hasattr(sb, 'c'))
        nt.ok_(hasattr(sb, 'd'))
        nt.ok_(hasattr(sb, 'e'))
        nt.ok_(hasattr(sb, 'f'))

        nt.eq_(sb.a, 1)
        nt.eq_(sb.b, 1.1)
        nt.eq_(sb.c, True)
        nt.eq_(sb.d, 'string')
        nt.eq_(sb.e, [1, 2, 3])
        nt.eq_(sb.G, 4)

    def test_load_dict_as_woc(self):
        sb = self.base
        nt.ok_(hasattr(sb, 'f'))
        nt.assert_is_instance(sb.f, WriteOnceContainer)

        nt.eq_(sb.f.a, 1)
        nt.eq_(sb.f.b, 2)
        nt.eq_(sb.f.c, 3)

    def test_load_with_options_case_sensitive(self):
        node = WriteOnceContainer()
        hnd = FileHandler.get_handler('test-data/data.json')
        hnd.load(node, preserve_case=True)

        nt.ok_(hasattr(node, 'a'))
        nt.ok_(hasattr(node, 'G'))
        nt.ok_(not hasattr(node, 'g'))
        nt.eq_(node.G, 4)

    def test_load_with_options_case_insensitive(self):
        node = WriteOnceContainer()
        hnd = FileHandler.get_handler('test-data/data.json')
        hnd.load(node, preserve_case=False)

        nt.ok_(hasattr(node, 'a'))
        nt.ok_(hasattr(node, 'g'))
        nt.ok_(not hasattr(node, 'G'))
        nt.eq_(node.g, 4)


class TestKonfig(object):

    def test_generate_path_node_tree(self):
        root = WriteOnceContainer()
        node = Konfig.generate_path_node_tree(root, '/a', '/a/b/c/d/e.ini')
        nt.ok_(hasattr(root, 'b'))
        nt.ok_(hasattr(root.b, 'c'))
        nt.ok_(hasattr(root.b.c, 'd'))
        nt.ok_(hasattr(root.b.c.d, 'e'))
        nt.eq_(node, root.b.c.d.e)

    def test_generate_path_node_tree_short_path_no_file(self):
        root = WriteOnceContainer()
        node = Konfig.generate_path_node_tree(root, '/a', '/a')
        nt.eq_(root, node)

    def test_generate_path_node_tree_short_path(self):
        root = WriteOnceContainer()
        node = Konfig.generate_path_node_tree(root, '/a', '/a/b.ini')
        nt.ok_(hasattr(root, 'b'))
        nt.eq_(node, root.b)

    def test_generate_path_node_tree_short_path_base_file(self):
        root = WriteOnceContainer()
        node = Konfig.generate_path_node_tree(root, '/a.ini', '/a.ini')
        nt.eq_(root, node)

    def test_generate_path_node_tree_unmatched_base(self):
        root = WriteOnceContainer()
        node = Konfig.generate_path_node_tree(root, '/a', '/k/b/c/d/e.ini')
        nt.ok_(hasattr(root, 'k'))
        nt.ok_(hasattr(root.k, 'b'))
        nt.ok_(hasattr(root.k.b, 'c'))
        nt.ok_(hasattr(root.k.b.c, 'd'))
        nt.ok_(hasattr(root.k.b.c.d, 'e'))
        nt.eq_(node, root.k.b.c.d.e)

    @nt.raises(TypeError)
    def test_generate_path_node_tree_bad_root(self):
        root = object()
        node = Konfig.generate_path_node_tree(root, '/a', '/a/b/c/d/e.ini')

    def test_load(self):
        kon = Konfig('test-data/a')
        files_loaded = kon.load()
        nt.eq_(len(files_loaded), 4)
        for idx in range(4):
            nt.assert_in('test-data/a', files_loaded[idx])
        nt.ok_(hasattr(kon, 'a'))
        nt.ok_(hasattr(kon, 'b'))
        nt.ok_(hasattr(kon, 'c'))
        nt.ok_(hasattr(kon.b, 'c'))
        nt.ok_(hasattr(kon.b.c, 'd'))

        for name in ['a', 'b', 'c']:
            nt.ok_(hasattr(getattr(kon, name), 'data'))
            data = getattr(getattr(kon, name), 'data')
            nt.ok_(hasattr(data, 'a'))
            nt.ok_(hasattr(data, 'b'))
            nt.ok_(hasattr(data, 'c'))
            nt.eq_(getattr(data, 'a'), 1)
            nt.eq_(getattr(data, 'b'), 'foo')
            nt.eq_(getattr(data, 'c'), True)

    @nt.raises(IOError)
    def test_load_bad_path(self):
        kon = Konfig('boom')
        kon.load()

    def test_load_merged_config(self):
        kon = Konfig('test-data/m')
        kon.load()
        nt.ok_(hasattr(kon, 'a'))
        nt.ok_(hasattr(kon.a, 'b'))
        nt.ok_(hasattr(kon.a, 'f'))
        nt.ok_(hasattr(kon.a.b, 'c'))
        nt.ok_(hasattr(kon.a.b, 'd'))
        nt.ok_(hasattr(kon.a.f, 'g'))
