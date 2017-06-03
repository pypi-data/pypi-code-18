import pyramid.testing
import pytest

from pyramid_jinja2_webpack import Jinja2EnvironmentMissingException, includeme


@pytest.fixture()
def config():
    return pyramid.testing.setUp()


@pytest.fixture()
def empty_manifest(tmpdir):
    tmpdir.chdir()
    manifest = tmpdir.join('webpack-manifest.json')
    manifest.write('{}')


@pytest.fixture()
def jinja2(config):
    config.include('pyramid_jinja2')
    config.commit()


@pytest.fixture()
def loaded_config(config, jinja2, empty_manifest):
    config.include(includeme)
    return config


def test_includeme_raises_exception(config):
    with pytest.raises(IOError):
        config.include(includeme)


def test_includeme_with_manifest_needs_jinja2(config, empty_manifest):
    with pytest.raises(Jinja2EnvironmentMissingException):
        config.include(includeme)


def test_includes_ok_with_manifest_and_jinja2(config, jinja2, empty_manifest):
    config.include(includeme)


def test_get_env_from_config(loaded_config):
    assert loaded_config.get_webpack_environment()
