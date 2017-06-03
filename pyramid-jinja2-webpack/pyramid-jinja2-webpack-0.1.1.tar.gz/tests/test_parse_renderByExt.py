import pytest

import pyramid_jinja2_webpack
from pyramid_jinja2_webpack import parse_multiline, parse_renderByExt

FOO = object()
BAR = object()
BAZ = object()
FUBAR = object()


@pytest.fixture()
def no_imports(monkeypatch):
    mapping = {'foo': FOO, 'bar': BAR, 'baz': BAZ, 'foo.bar': FUBAR}

    def resolve(name):
        try:
            return mapping[name]
        except KeyError:
            raise ImportError

    monkeypatch.setattr(pyramid_jinja2_webpack, 'resolve_dotted', resolve)


def test_parse_multiline():
    v = parse_multiline("""
        foo=bar
        bar=baz
        foo.bar=baz
    """)

    assert v == {'foo': 'bar', 'bar': 'baz', 'foo.bar': 'baz'}


def test_parse_multiline_empty():
    v = parse_multiline('')
    assert v == {}


def test_parse_renderByExt(no_imports):
    v = parse_renderByExt("""
        foo=foo
        bar=bar
        fubar=foo.bar
    """)

    assert v == {'foo': FOO, 'bar': BAR, 'fubar': FUBAR}


def test_parse_renderByExt_invalid_import(no_imports):
    with pytest.raises(ImportError):
        parse_renderByExt("""
            this_import=fubar
        """)
