import pytest
from flask import Flask
from flask_open_directory.utils import username_from_request, \
    base_dn_from_url


@pytest.fixture
def flask_app():
    return Flask(__name__)


def test_base_dn_from_url():
    assert base_dn_from_url(None) is None
    assert base_dn_from_url('example.com') == 'dc=example,dc=com'


def test_username_from_request(headers):

    with pytest.raises(RuntimeError):
        username_from_request()

    app = Flask(__name__)

    @app.route('/')
    def index():
        return 'Username: {}'.format(username_from_request())

    test_client = app.test_client()

    resp = test_client.get('/', headers=headers('testuser', 'pass'))
    assert b'Username: testuser' in resp.data

    resp = test_client.get('/')
    assert b'Username: None' in resp.data
