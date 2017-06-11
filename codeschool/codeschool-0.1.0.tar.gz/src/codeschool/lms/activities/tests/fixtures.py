import pytest
from lazyutils import delegate_to
from mock import patch, Mock

from codeschool.accounts.factories import UserFactory
from codeschool.lms.activities.models import Activity
from codeschool.lms.activities.tests.mocks import wagtail_page


class ActivityFixtures:
    """
    Expose an "activity" and a "progress" fixtures that do not access the
    database upon creation.

    Users of this class must define an activity_class class attribute with
    the class that should be tested.
    """

    activity_class = Activity
    submission_payload = {}
    use_db = False

    @pytest.fixture
    def activity(self):
        "An activity instance that does not touch the db."

        cls = self.activity_class
        with wagtail_page(cls):
            result = cls(title='Test', id=1)
        result.specific = result
        return result

    @pytest.fixture
    def activity_db(self):
        "A saved activity instance."

        result = self.activity_class(title='Test', id=1)
        result.specific = result
        return result

    @pytest.yield_fixture
    def progress(self, activity, user):
        "A progress instance for some activity."

        cls = self.progress_class

        if cls._meta.abstract:
            pytest.skip('Progress class is abstract')

        with patch.object(cls, 'user', user):
            progress = cls(activity_page=activity, id=1)
            yield progress

    @pytest.fixture
    def progress_db(self, progress):
        "A progress instance saved to the db."

        progress.user.save()
        progress.activity.save()
        progress.save()
        return progress

    @pytest.fixture
    def user(self):
        "An user"

        return UserFactory.build(id=2, username='user')

    # Properties
    progress_class = delegate_to('activity_class')
    submission_class = delegate_to('activity_class')
    feedback_class = delegate_to('activity_class')