from __future__ import absolute_import, unicode_literals
import distll_celery
import pytest


def test_version():
    assert distll_celery.VERSION
    assert len(distll_celery.VERSION) >= 3
    distll_celery.VERSION = (0, 3, 0)
    assert distll_celery.__version__.count('.') >= 2


@pytest.mark.parametrize('attr', [
    '__author__', '__contact__', '__homepage__', '__docformat__',
])
def test_meta(attr):
    assert getattr(distll_celery, attr, None)
