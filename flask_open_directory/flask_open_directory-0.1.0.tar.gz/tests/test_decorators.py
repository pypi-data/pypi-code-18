import pytest
from flask import Flask
from flask_open_directory.decorators import requires_group, DecoratorContext, \
    requires_all_groups, requires_any_group


@pytest.fixture
def flask_app(open_directory):
    app = Flask(__name__)
    open_directory.init_app(app)
    return app


def test_DecoratorContext():
    ctx = DecoratorContext(username='user')
    assert ctx['username'] == 'user'
    assert ctx.username == 'user'

    ctx.foo = 'bar'
    assert ctx['foo'] == 'bar'

    with pytest.raises(AttributeError):
        ctx.invalid


def test_requires_group_decorator(flask_app, headers, group_name, username):

    @flask_app.route('/restricted')
    @requires_group(group_name)
    def restricted():
        """Restricted doc string"""
        return "Hello from restricted"

    assert restricted.__doc__ == """Restricted doc string"""

    test_client = flask_app.test_client()
    resp = test_client.get('/restricted', headers=headers(username, 'pass'))
    assert resp.status_code == 200
    assert b"Hello from restricted" in resp.data

    resp = test_client.get('/restricted', headers=headers('invalid', 'pass'))
    assert resp.status_code == 401


def test_requires_group_decorator_fails_with_no_open_directory(group_name,
                                                               username,
                                                               headers):

    app = Flask(__name__)

    @app.route('/restricted')
    @requires_group(group_name)
    def restricted():
        return "Hello from restricted"

    test_client = app.test_client()

    resp = test_client.get('/restricted', headers=headers(username, 'pass'))
    assert resp.status_code == 500


def test_requires_groups_decorator(group_name, username, headers, flask_app,
                                   workgroup_username):

    @flask_app.route('/restricted')
    @requires_all_groups('workgroup', group_name)
    def restricted():
        return "Hello from restricted."

    test_client = flask_app.test_client()
    resp = test_client.get('/restricted', headers=headers(username, 'pass'))
    assert resp.status_code == 200
    assert b"Hello from restricted" in resp.data

    resp = test_client.get('/restricted', headers=headers('invalid', 'pass'))
    assert resp.status_code == 401

    resp = test_client.get('/restricted',
                           headers=headers(workgroup_username, 'pass'))
    assert resp.status_code == 401


def test_requires_any_group_decorator(group_name, username, headers, flask_app,
                                      workgroup_username):

    @flask_app.route('/restricted')
    @requires_any_group(group_name, 'workgroup')
    def restricted():
        return "Hello from restricted."

    @flask_app.route('/check')
    @requires_group(group_name)
    def check_workgroup_user_is_not_in_groupname():
        return "You should not be here!"

    test_client = flask_app.test_client()

    # verify the workgroup username is not in the test group, only in the
    # workgroup
    resp = test_client.get('/check',
                           headers=headers(workgroup_username, 'pass'))
    assert resp.status_code == 401

    resp = test_client.get('/restricted',
                           headers=headers(workgroup_username, 'pass'))
    assert resp.status_code == 200
    assert b"Hello from restricted" in resp.data
