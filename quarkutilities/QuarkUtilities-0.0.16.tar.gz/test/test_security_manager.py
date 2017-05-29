import os
import sys
import jwt
import datetime
from calendar import timegm

import pytest
from unittest import mock

from flasky import InvalidTokenError

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__ + "/../")))

from quark_utilities import jwt_security

mock_app = mock.MagicMock()
mock_handler = mock.MagicMock()
secret = "secret"
manager = jwt_security.SecurityManager(mock_app, secret, issuer="Quark-CMS")

@pytest.mark.asyncio
async def test_should_raise_none_when_method_definition_is_not_contain_secure_field():
    ret = await manager._before_request_hook(mock_handler, {})
    assert ret is None

@pytest.mark.asyncio
async def test_should_raise_not_authorized_exc_when_auth_header_not_found():
    mock_handler.request.headers = {}
    try:
        ret = await manager._before_request_hook(mock_handler, {"secure":["admin"]})
    except jwt_security.AgentIsNotAuthorized as e:
        assert e.message.startswith("Authorization header is")
        return

    assert False


@pytest.mark.asyncio
async def test_should_raise_not_authorized_exc_when_auth_header_is_not_bearer_typ():
    mock_handler.request.headers = {"Authorization": "Basic vıdıvıdı"}

    try:
        ret = await manager._before_request_hook(mock_handler, {"secure":["admin"]})
    except jwt_security.AgentIsNotAuthorized as e:
        assert e.message.startswith("Authorization token is not")
        return

    assert False, "Exc is not thrown"


@pytest.mark.asyncio
async def test_should_raise_not_authorized_error_when_token_is_expired():
    mock_handler.request.headers = {"Authorization": "Bearer: " + get_token(exp_minus=1000)}
    try:
        ret = await  manager._before_request_hook(mock_handler, {"secure": ["admin"]})
    except InvalidTokenError:
        assert True
        return
    assert False

@pytest.mark.asyncio
async def test_should_raise_invalid_token_error_when_token_issuer_not_match():
    mock_handler.request.headers = {"Authorization": "Bearer: " + get_token()}

    try:
        await  manager._before_request_hook(mock_handler, get_method_def())
    except InvalidTokenError:
        assert True
        return
    assert False, "Exception is not raised"


@pytest.mark.asyncio
async def test_should_not_raise_any_exception_when_issuer_is_match():
    mock_handler.request.headers = {"Authorization": "Bearer: " + get_token(issuer="Quark-CMS")}

    await  manager._before_request_hook(mock_handler, get_method_def())
    assert True, "No exception is not raised"


def test_partify_should():
    assert len(jwt_security.partify("application:create")) == 2
    assert len(jwt_security.partify("application,user_group:create")[0]) == 2
    assert len(jwt_security.partify("application:create:1,2,3")) == 3

def test_implies():
    assert jwt_security.implies("*", "application:read")
    assert not jwt_security.implies("application:read", "*")
    assert jwt_security.implies("application:*", "application:read")
    assert jwt_security.implies("application:read,write", "application:read")
    assert jwt_security.implies("one,two", "two")
    assert not jwt_security.implies("two", "one,two")
    assert jwt_security.implies("one,two:three,four,five:six", "one:three:six")
    assert not jwt_security.implies("one:three:six", "one,two:three,four,five:six")

def get_method_def():
    return {
        "secure": ["admin"]
    }


def get_token(exp_minus=0, issuer=None):
    jwt_payload = dict(
        exp=timegm(datetime.datetime.utcnow().utctimetuple()) - exp_minus,
        roles=["admin"],
        prn="hyurtseven"
    )

    if issuer:
        jwt_payload['iss'] = issuer

    return jwt.encode(jwt_payload, key=secret).decode("utf-8")



