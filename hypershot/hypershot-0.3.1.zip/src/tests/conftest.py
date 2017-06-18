"""py.test configuration."""
import os
import logging

import mock
import pytest
from addict import Dict as attrdict


@pytest.fixture(scope='session')
def empty_config_dir():
    """Return mock object to set config dir to a path with no config files."""
    return mock.patch('hypershot.config.config_dir', os.path.dirname(__file__))


@pytest.fixture(scope='session')
def filled_config_dir():
    """Return mock object to set config dir to a path with some config files."""
    return mock.patch('hypershot.config.config_dir', os.path.join(os.path.dirname(__file__), 'data'))


@pytest.fixture(scope='session')
def examples_config_dir():
    """Return mock object to set config dir to a path with examples from 'docs'."""
    return mock.patch('hypershot.config.config_dir', os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'docs', 'examples'))


@pytest.fixture(scope='session')
def fake_netrc():
    """Return mock object for netrc.netrc() fake data."""
    return mock.patch('netrc.netrc', return_value=attrdict(authenticators=lambda x: ('foo',)*3))


@pytest.fixture(scope='session')
def test_yaml_path():
    """Return path to ``test.yaml`` file."""
    return os.path.join(os.path.dirname(__file__), 'data', 'test.yaml')


@pytest.fixture(scope='session')
def logger():
    """Return test logger instance."""
    logging.basicConfig(level=logging.DEBUG)
    return logging.getLogger('tests')
