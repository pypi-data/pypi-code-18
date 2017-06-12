import mock
from django.core.management import call_command
from django.db.models.signals import post_save

from aa_intercom.models import IntercomEvent
from aa_intercom.signals import intercom_event_push_to_intercom_post_save
from aa_intercom.tests.test_utils import BaseTestCase


class TestCommands(BaseTestCase):
    def setUp(self):
        self.user_count = 5
        self.users = [self._new_user(i) for i in range(self.user_count)]

    def test_resend_intercom_events(self):
        # Disable post_save signal during the test to simulate that the events were not sent and the
        # resend_intercom_event command should be used
        post_save.disconnect(intercom_event_push_to_intercom_post_save, sender=IntercomEvent)
        intercom_events = [IntercomEvent.objects.create(user=self.users[i], type="generic")
                           for i in range(self.user_count)]
        for e in intercom_events:
            self.assertFalse(e.is_sent)

        with mock.patch("aa_intercom.tasks.upload_intercom_user") as upload_mocked:
            call_command("resend_intercom_events")
            calls = [mock.call(self.users[i].id) for i in range(self.user_count)]
            upload_mocked.assert_has_calls(calls)
