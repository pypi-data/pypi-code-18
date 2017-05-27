import pytest

from flask_open_directory import OpenDirectory


@pytest.fixture
def open_directory():
    return OpenDirectory()
