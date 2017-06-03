import pytest
from jinja2_webpack import DEFAULT_SETTINGS
from pyramid.exceptions import ConfigurationError

from pyramid_jinja2_webpack import webpack_settings_from_settings


def _(settings, **kw):
    return webpack_settings_from_settings(settings, **kw)


def test_manifest():
    settings = _({'webpack.manifest': 'manifest.json'})
    assert settings['manifest'] == 'manifest.json'


def test_useDefaultRenderByExt():
    settings = _({'webpack.useDefaultRenderByExt': 'False'})
    assert settings['useDefaultRenderByExt'] is False


def test_alternate_prefix():
    settings = _({'test_prefix_manifest': 'manifest.json'},
                 prefixes=['test_prefix_'])
    assert settings['manifest'] == 'manifest.json'


def test_multiple_prefixes():
    settings = _({'p1.manifest': 'a', 'p2.publicRoot': 'b'},
                 prefixes=['p1.', 'p2.'])
    assert settings['manifest']
    assert settings['publicRoot']


def test_error_on_invalid_setting():
    with pytest.raises(ConfigurationError):
        _({'webpack.fubar': True})


def test_error_on_invalid_setting_toggle():
    _({'webpack.fubar': True, 'webpack.errorOnInvalidSetting': False})


FOO = object()
BAR = object()


@pytest.fixture()
def no_imports(monkeypatch):
    import pyramid_jinja2_webpack
    mapping = {'foo.bar': FOO, 'bar.baz': BAR}
    monkeypatch.setattr(pyramid_jinja2_webpack, 'resolve_dotted', mapping.get)


def test_setting_renderByext(no_imports):
    settings = _({'webpack.renderByExt': '.js=foo.bar\n.css=bar.baz'})
    assert settings['renderByExt']['.js'] == FOO
    assert settings['renderByExt']['.css'] == BAR


def test_defaultRenderer(no_imports):
    settings = _({'webpack.defaultRenderer': 'foo.bar'})
    assert 'defaultRenderer' in DEFAULT_SETTINGS
    assert settings['defaultRenderer'] == FOO


def test_badRendererRaisesException():
    with pytest.raises(ImportError):
        _({'webpack.defaultRenderer': 'foo.bar'})
