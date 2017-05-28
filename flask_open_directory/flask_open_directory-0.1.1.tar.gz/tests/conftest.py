import pytest
import os
import base64

from flask_open_directory import OpenDirectory, Query, User, Group


OPEN_DIRECTORY_TEST_USERNAME = os.environ.get('OPEN_DIRECTORY_TEST_USERNAME',
                                              'testuser')

OPEN_DIRECTORY_TEST_USER_FULL_NAME = os.environ.get(
    'OPEN_DIRECTORY_TEST_USER_FULL_NAME',
    'Test User'
)

OPEN_DIRECTORY_TEST_USER_EMAIL = os.environ.get(
    'OPEN_DIRECTORY_TEST_USER_EMAIL',
    'test_user@example.com'
)

OPEN_DIRECTORY_TEST_GROUP = os.environ.get('OPEN_DIRECTORY_TEST_GROUP',
                                           'testgroup')


OPEN_DIRECTORY_TEST_WORKGROUP_USERNAME = os.environ.get(
    'OPEN_DIRECTORY_TEST_WORKGROUP_USERNAME',
    'testuser2'
)


@pytest.fixture
def open_directory():
    return OpenDirectory()


@pytest.fixture
def user_query(open_directory):
    return Query(open_directory, User)


@pytest.fixture
def group_query(open_directory):
    return Query(open_directory, Group)


@pytest.fixture
def username():
    return OPEN_DIRECTORY_TEST_USERNAME


@pytest.fixture
def user_full_name():
    return OPEN_DIRECTORY_TEST_USER_FULL_NAME


@pytest.fixture
def user_email():
    return OPEN_DIRECTORY_TEST_USER_EMAIL


@pytest.fixture
def group_name():
    return OPEN_DIRECTORY_TEST_GROUP


@pytest.fixture
def workgroup_username():
    return OPEN_DIRECTORY_TEST_WORKGROUP_USERNAME


@pytest.fixture
def user_id(user_query, username):
    return user_query.filter(username=username).first().id


@pytest.fixture
def headers():

    def create_headers(username, password):
        return {
            'Authorization': "Basic {}".format(
                base64.b64encode(bytes(username + ':' + password, 'utf-8'))
                .decode('ascii')
            )
        }

    return create_headers
