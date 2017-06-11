"""
Abstract test cases for activities subclasses and surrounding models.

Subclasses must define a few required models and attributes::

    class Fixtures(ActivityFixtures):
        base_class = MyClass

    class TestMyClass(Fixtures, ActivityTests):
        def test_something_else(self, activity):
            assert activity.the_answer() == 45


Base Fixture classes
--------------------

.. autoclass:: ActivityFixtures
.. autoclass:: DbActivityFixtures


Patchers/mockers
----------------

.. autofunction:: wagtail_page
.. autofunction:: disable_commit
.. autofunction:: queryset_mock

"""

from codeschool.lms.activities.tests.mocks import wagtail_page, \
    disable_commit, queryset_mock
from codeschool.lms.activities.tests.fixtures import ActivityFixtures
from codeschool.lms.activities.tests.base import \
    ActivityTests, ProgressTests, ProgressTestsDb