from __future__ import absolute_import, unicode_literals
import distll_celery
import pytest
from distll_celery.app.task import Task as ModernTask
from distll_celery.task.base import Task as CompatTask


@pytest.mark.usefixtures('depends_on_current_app')
class test_MagicModule:

    def test_class_property_set_without_type(self):
        assert ModernTask.__dict__['app'].__get__(CompatTask())

    def test_class_property_set_on_class(self):
        assert (ModernTask.__dict__['app'].__set__(None, None) is
                ModernTask.__dict__['app'])

    def test_class_property_set(self, app):

        class X(CompatTask):
            pass
        ModernTask.__dict__['app'].__set__(X(), app)
        assert X.app is app

    def test_dir(self):
        assert dir(distll_celery.messaging)

    def test_direct(self):
        assert distll_celery.task

    def test_app_attrs(self):
        assert (distll_celery.task.control.broadcast ==
                distll_celery.current_app.control.broadcast)

    def test_decorators_task(self):
        @distll_celery.decorators.task
        def _test_decorators_task():
            pass

    def test_decorators_periodic_task(self):
        @distll_celery.decorators.periodic_task(run_every=3600)
        def _test_decorators_ptask():
            pass
