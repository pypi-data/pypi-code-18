import trafaret as t

from .configus import config, config_with_error, maybe_get_argv, parse_envfile


def test_basic():
    env = {'var': 'hallo', 'another_var': 'holla'}
    expected = {'var': 'hallo'}
    assert config(t.Dict(var=t.String), env) == expected
    data, err = config_with_error(t.Dict(var=t.String), dict(var=1))
    assert data is None
    assert isinstance(err, t.DataError)


def test_warn():
    env = {'VAR': 'hallo'}
    expected = {'var': 'hallo'}
    assert config(t.Dict(var=t.String), env) == expected

    env = {'VAR': 'hallo'}
    expected = {'VAR': 'hallo'}
    assert config(t.Dict(VAR=t.String), env) == expected


def test_argv():
    assert maybe_get_argv(['--rate=1', '--backoff=2', 'debug=1']) == {'backoff': '2', 'debug': '1', 'rate': '1'}


def test_envfile():
    contents = [
                "One=one   ",
                "\texport Two=two\n\n\n \n",
                "\n\n\n \n",
                "None \n\n\n \n",
                "=",
                ]

    expected = [
        {'One': 'one'},
        {'Two': 'two'},
        {},
        {},
        {},
    ]
    for given, expected in zip(contents, expected):
        assert parse_envfile([given]) == expected
