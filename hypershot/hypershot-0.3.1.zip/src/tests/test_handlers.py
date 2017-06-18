# pylint: disable=wildcard-import, unused-wildcard-import, unused-import, missing-docstring, invalid-name
# pylint: disable=protected-access
"""Test 'handlers' module."""
import mock
import pytest
from addict import Dict as attrdict

from hypershot import handlers, config
from hypershot.handlers import *

ImgurHandler.DEFAULTS.update(dict(login='fake-id', password='fake-secret'))
IMAGE_FILE = 'docs/_static/hypershot-templates.png'
HANDLERS = [v for k, v in vars(handlers).items() if k.endswith('Handler')]


def netrc_netrc(*auth):
    """Return mocks for netrc.netrc delivering the given auth data."""
    auth_mock = mock.MagicMock(side_effect=auth)
    netrc_mock = attrdict(authenticators=auth_mock)
    return netrc_mock, auth_mock


@pytest.mark.parametrize('text,expected', [
    ('', ''),
    ('?', '_'),
    ('abc', 'abc'),
    ('A…Z', 'A_Z'),
    ('123€', '123_'),
])
def test_convert_to_pure_ascii(text, expected):
    assert handlers._pure_ascii(text) == expected


@pytest.mark.parametrize('handler_class', HANDLERS)
def test_upload_handler_init_with_empty_settings(handler_class):
    handler = handler_class({})
    assert handler.settings.enabled
    assert not handler.settings.thumbsize


@pytest.mark.parametrize('handler_class', HANDLERS)
def test_upload_handler_dry_run_upload(handler_class):
    handler = handler_class(dict(types={'PNG'}))
    with mock.patch('hypershot.config.dry_run', True):
        handler.upload(IMAGE_FILE)


def test_imgur_handler_with_netrc(mocker):
    netrc_mock, auth_mock = netrc_netrc(('fake-id', None, 'fake-secret'))
    mocked_netrc = mocker.patch('netrc.netrc', return_value=netrc_mock)
    handler = ImgurHandler(dict(login='.netrc'))

    mocked_netrc.assert_called_once_with()
    auth_mock.assert_called_once_with('hypershot:api.imgur.com')
    assert handler.settings.login == 'fake-id'
    assert handler.settings.password == 'fake-secret'


@pytest.mark.parametrize('auth', [None, (None, None, 'fake-secret')])
def test_imgur_handler_with_bad_netrc_data(mocker, auth):
    netrc_mock, _ = netrc_netrc(auth, auth)
    mocker.patch('netrc.netrc', return_value=netrc_mock)
    with pytest.raises(ValueError):
        ImgurHandler(dict(login='.netrc'))


@pytest.mark.parametrize('auth', [('fake-id', None, None)])
def test_imgur_handler_with_no_password_in_netrc_data(mocker, auth):
    netrc_mock, _ = netrc_netrc(auth, auth)
    mocker.patch('netrc.netrc', return_value=netrc_mock)
    with pytest.raises(AssertionError):
        ImgurHandler(dict(login='.netrc'))


def test_imgur_handler_with_netrc_lookup_fallback(mocker):
    netrc_mock, auth_mock = netrc_netrc(None, ('fake-id', None, 'fake-secret'))
    mocked_netrc = mocker.patch('netrc.netrc', return_value=netrc_mock)
    handler = ImgurHandler(dict(login='.netrc'))

    mocked_netrc.assert_called_once_with()
    #auth_mock.assert_called_with('hypershot:api.imgur.com')
    auth_mock.assert_called_with('api.imgur.com')
