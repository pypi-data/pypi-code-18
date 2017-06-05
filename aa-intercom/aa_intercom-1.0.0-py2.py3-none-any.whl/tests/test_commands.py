import mock
from django.core.management import call_command
from django.db.models.signals import post_save

from aa_intercom.signals import intercom_event_push_to_intercom_post_save
from aa_intercom.tests.test_utils import BaseTestCase
from aa_intercom.utils import get_intercom_event_model

IntercomEvent = get_intercom_event_model()


class TestCommands(BaseTestCase):
    def setUp(self):
        self.user_count = 5
        self.users = [self._new_user(i) for i in range(self.user_count)]

    def test_resend_intercom_events(self):
        # Disable post_save signal during the test
        post_save.disconnect(intercom_event_push_to_intercom_post_save, sender=IntercomEvent)
        intercom_events = [IntercomEvent.objects.create(user=self.users[i], type=IntercomEvent.TYPE_GENERIC)
                           for i in range(self.user_count)]
        for e in intercom_events:
            self.assertFalse(e.is_sent)

        with mock.patch("aa_intercom.tasks.upload_intercom_user") as upload_mocked:
            call_command("resend_intercom_events")
            calls = [mock.call(self.users[i].id) for i in range(self.user_count)]
            upload_mocked.assert_has_calls(calls)
