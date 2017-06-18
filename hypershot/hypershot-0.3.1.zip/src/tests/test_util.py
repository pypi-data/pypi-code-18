# pylint: disable=wildcard-import, unused-wildcard-import, unused-import, missing-docstring, invalid-name
"""Test 'util' module."""
import json

import mock
import yaml
import pytest
from addict import Dict as attrdict

from hypershot import config
from hypershot.util import *


def test_smart_JSON_encoder_with_set():
    text = json.dumps({1, 2, 3}, indent=4, sort_keys=True, cls=SmartJSONEncoder)

    assert '1, 2, 3' in ' '.join(text.split())


def test_smart_JSON_raises_with_object():
    with pytest.raises(TypeError):
        json.dumps(object(), indent=4, sort_keys=True, cls=SmartJSONEncoder)


def test_dumb_JSON_raises_with_set():
    with pytest.raises(TypeError):
        json.dumps({1, 2, 3}, indent=4, sort_keys=True)


def test_bare_table_has_no_border():
    table = BareTable([['C1', 'C2'], [1, 2]])

    assert table.table == 'C1  C2  \n1   2   '


def test_bibytes_floating():
    assert bibytes('1.5K') == 1024 + 512
    assert bibytes(1.5) == 1


@pytest.mark.parametrize('value,expected', [
    (0, '   0 bytes'),
    (1, '   1 bytes'),
    (1.5, '   1 bytes'),
    (1024, '   1.0 KiB'),
    (1024**2, '   1.0 MiB'),
    (1024**3, '   1.0 GiB'),
    (1024**8, '   1.0 YiB'),
    (1024 + 512, '   1.5 KiB'),
])
def test_to_bibytes_returns_expected_value(value, expected):
    assert to_bibytes(value) == expected


def test_to_bibytes_knows_insanity():
    with pytest.raises(ValueError):
        to_bibytes(1024**9)


@pytest.mark.parametrize('value', [-1, 'xxx', '123X', '123KB'])
def test_to_bibytes_with_bad_value(value):
    with pytest.raises(ValueError):
        to_bibytes(value)


def test_coerce_called_with_None():
    assert coerce_to_default_type('test', None, object()) is None


def test_coerce_to_int():
    assert coerce_to_default_type('test', '42', 0) == 42


def test_coerce_to_bool():
    assert coerce_to_default_type('test', 'on', False)


def test_coerce_with_bad_value():
    with pytest.raises(ValueError):
        assert coerce_to_default_type('test', 'foo', False)


def test_fatal_raises_in_debug_mode():
    with mock.patch('hypershot.config.debug', True):
        with pytest.raises(ValueError):
            fatal(ValueError('test'))


def test_parse_yaml_reads_test_file(test_yaml_path):
    data = parse_yaml(open(test_yaml_path))
    assert data == dict(test=[1, 2, 3])


def test_logging_level_from_settings():
    root = logging.getLogger()

    logging_level(attrdict(debug=True))
    assert root.level == logging.DEBUG

    logging_level(attrdict(debug=False, verbose=True))
    assert root.level == logging.INFO

    logging_level(attrdict(debug=False, verbose=False))
    assert root.level == logging.WARNING


def test_logging_setup_with_no_config(mocker, empty_config_dir):
    basic_cfg = mocker.patch('logging.basicConfig')
    with empty_config_dir:
        logging_setup(attrdict(debug=True), config.config_dir, appname='test')

    basic_cfg.assert_called_once_with()


@pytest.mark.parametrize('debug', [False, True])
def test_logging_setup_with_yaml_config(mocker, examples_config_dir, debug):
    dict_cfg = mocker.patch('logging.config.dictConfig')
    with examples_config_dir:
        expected = parse_yaml(open(os.path.join(config.config_dir, 'logging.yaml')))
        logging_setup(attrdict(debug=debug), config.config_dir, appname='test')

    dict_cfg.assert_called_once_with(expected)


def test_logging_setup_with_bad_yaml_config(mocker, examples_config_dir):
    mocker.patch('hypershot.util.parse_yaml', side_effect=yaml.YAMLError('Bad!'))
    with examples_config_dir:
        with pytest.raises(RuntimeError):
            logging_setup(attrdict(debug=True), config.config_dir, appname='test')


def test_logging_setup_with_ini_config(mocker, filled_config_dir):
    file_cfg = mocker.patch('logging.config.fileConfig')
    with filled_config_dir:
        expected = os.path.join(config.config_dir, 'logging.ini')
        logging_setup(attrdict(debug=False, verbose=False), config.config_dir, appname='test')

    file_cfg.assert_called_once_with(expected)


def test_parse_config_with_yaml_file(examples_config_dir):
    with examples_config_dir:
        parse_config(attrdict(verbose=True, debug=True, config_dir=config.config_dir),
                     defaults=attrdict(no_progress=True, nested=dict(val=1)), init_logging=False)


def test_parse_config_with_bad_yaml_config(mocker, examples_config_dir):
    mocker.patch('hypershot.util.parse_yaml', side_effect=yaml.YAMLError('Bad!'))
    with examples_config_dir:
        with pytest.raises(RuntimeError):
            parse_config(attrdict(debug=True, config_dir=config.config_dir), init_logging=False)


@pytest.mark.parametrize('init', [False, True])
def test_parse_config_with_bad_value(examples_config_dir, init):
    os.environ['HYPERSHOT_NO_PROGRESS'] = 'foobar'
    try:
        with examples_config_dir:
            with pytest.raises(RuntimeError):
                parse_config(attrdict(debug=True, config_dir=config.config_dir), init_logging=init)
    finally:
        del os.environ['HYPERSHOT_NO_PROGRESS']


@pytest.mark.parametrize('json_data,kwargs', [
    (None, dict(no_progress=False)),
    ([42], dict()),
    (None, dict(files=[], no_progress=True)),
])
def test_http_post_without_progress(json_data, kwargs):
    post = mock.MagicMock(return_value=None)
    http_post_with_progress(mock.MagicMock(post=post), '', json=json_data, **kwargs)
    post.assert_called_once()


@pytest.mark.parametrize('label', ['short', '#'*99])
def test_http_post_with_progress(label):
    def post(url, data, **kwargs):
        assert url == 'FAKE-URL'
        assert 'labels' not in kwargs
        assert 'files' not in kwargs
        assert 'Content-Type' in kwargs.get('headers')

        data.read(1)

    http_post_with_progress(mock.MagicMock(post=post), 'FAKE-URL',
                            data=dict(foo='bar'), files=[], label=label)
