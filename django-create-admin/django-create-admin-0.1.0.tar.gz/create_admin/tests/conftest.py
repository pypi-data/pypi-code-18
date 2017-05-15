import os

import pytest


@pytest.fixture
def os_env():
    """
    Fixture for environment variables.

    The environment is rolled back to its previous state after each
    test.

    Yields:
        The current os environment.
    """
    old_env = os.environ.copy()

    yield os.environ

    os.environ = old_env
