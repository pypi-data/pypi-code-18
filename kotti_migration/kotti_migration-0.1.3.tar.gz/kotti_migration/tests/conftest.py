# -*- coding: utf-8 -*-

"""
Created on 2017-05-22
:author: Oshane Bailey (b4.oshany@gmail.com)
"""

pytest_plugins = "kotti"

from pytest import fixture


@fixture(scope='session')
def custom_settings():
    import kotti_migration.resources
    kotti_migration.resources  # make pyflakes happy
    return {
        'kotti.configurators': 'kotti_tinymce.kotti_configure '
                               'kotti_migration.kotti_configure'}
