#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from flask_open_directory import OpenDirectory, Group, Query
from flask import Flask
# from flask_httpauth import HTTPDigestAuth, HTTPBasicAuth


@pytest.fixture
def flask_app():
    return Flask(__name__)


def test_base_dn_returns_empty_string():

    od = OpenDirectory()
    od.config['OPEN_DIRECTORY_BASE_DN'] = None
    od.config['OPEN_DIRECTORY_SERVER'] = None

    assert od.base_dn == ''


def test_query():
    od = OpenDirectory()
    assert isinstance(od.query(), Query)
    q = od.query(Group)
    assert q.model == Group
    assert q.open_directory == od


def test_init_with_flask_app(flask_app):

    open_directory = OpenDirectory(flask_app)
    assert open_directory.app == flask_app

    od_no_app = OpenDirectory()
    assert od_no_app.app is None
    od_no_app.init_app(flask_app)
    assert od_no_app.app is None
