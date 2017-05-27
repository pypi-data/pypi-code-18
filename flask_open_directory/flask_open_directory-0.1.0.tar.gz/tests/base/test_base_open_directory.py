import pytest
import os
import ldap3
from flask import Flask

from flask_open_directory import BaseOpenDirectory, utils


@pytest.fixture
def config():
    return {
        'OPEN_DIRECTORY_SERVER': os.environ.get('OPEN_DIRECTORY_SERVER', None),
        'OPEN_DIRECTORY_BASE_DN': os.environ.get('OPEN_DIRECTORY_BASE_DN',
                                                 None),
    }


@pytest.fixture
def base_open_directory(config):
    return BaseOpenDirectory(**config)


@pytest.fixture
def flask_app():
    app = Flask(__name__)
    return app


def test_BaseOpenDirectory_server_url(base_open_directory):
    url = base_open_directory.server_url
    assert isinstance(url, str)

    env_url = os.environ.get('OPEN_DIRECTORY_SERVER', None)
    if env_url is not None:
        assert url == env_url

    default_od = BaseOpenDirectory()
    assert default_od.server_url == 'localhost'


def test_BaseOpenDirectory_base_dn(base_open_directory):
    base_dn = base_open_directory.base_dn
    assert isinstance(base_dn, str)

    env_dn = os.environ.get('OPEN_DIRECTORY_BASE_DN', None)
    if env_dn is not None:
        assert base_dn == utils.base_dn_from_url(base_open_directory.server_url)


def test_BaseOpenDirectory_create_server(base_open_directory):
    assert isinstance(base_open_directory.create_server(), ldap3.Server)


def test_BaseOpenDirectory_connect(base_open_directory):
    assert isinstance(base_open_directory.connect(), ldap3.Connection)


def test_BaseOpenDirectory_connection(base_open_directory, flask_app):
    assert base_open_directory.connection is None

    with flask_app.app_context() as ctx:
        assert base_open_directory.connection == ctx.open_directory_connection


def test_BaseOpenDirectory_connection_ctx(base_open_directory, flask_app):

    with base_open_directory.connection_ctx() as conn:
        assert isinstance(conn, ldap3.Connection)

    with flask_app.app_context() as ctx:
        with base_open_directory.connection_ctx() as conn:
            assert conn == ctx.open_directory_connection
