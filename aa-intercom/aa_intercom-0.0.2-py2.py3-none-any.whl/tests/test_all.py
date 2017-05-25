# -*- coding: utf-8 -*-
from aa_intercom.models import IntercomEvent
from aa_intercom.tasks import push_account_last_seen_task
from aa_intercom.tests.test_utils import BaseTestCase
from django.core import mail
from django.test.utils import override_settings

import json
import requests_mock


class TestIntercomAPI(BaseTestCase):

    intercom_user = {
        "type": "user",
        "id": "530370b477ad7120001d",
        "user_id": "25",
        "email": "wash@serenity.io",
        "phone": "+1123456789",
        "name": "Hoban Washburne",
        "updated_at": 1392734388,
        "last_seen_ip": "1.2.3.4",
        "unsubscribed_from_emails": False,
        "last_request_at": 1397574667,
        "signed_up_at": 1392731331,
        "created_at": 1392734388,
        "session_count": 179,
        "user_agent_data": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9",
        "pseudonym": None,
        "anonymous": False,
        "custom_attributes": {
            "paid_subscriber": True,
            "monthly_spend": 155.5,
            "team_mates": 1
        },
        "avatar": {
            "type": "avatar",
            "image_url": "https://example.org/128Wash.jpg"
        },
        "location_data": {
            "type": "location_data",
            "city_name": "Dublin",
            "continent_code": "EU",
            "country_code": "IRL",
            "country_name": "Ireland",
            "latitude": 53.159233,
            "longitude": -6.723,
            "postal_code": None,
            "region_name": "Dublin",
            "timezone": "Europe/Dublin"
        },
    }

    @override_settings(SKIP_INTERCOM=False)
    def test_upload(self):
        with requests_mock.Mocker() as m:
            url = "https://api.intercom.io/users/"
            m.register_uri("POST", url, text=json.dumps(self.intercom_user))
            self._create_user()
            self.user.refresh_from_db()
            self.assertIsNotNone(self.user.intercom_last_api_response)

    def test_intercom_example_event(self):
        """
            this test can be removed or fine tuned per project.
        """
        self._create_user()
        mail.outbox = []
        self.assertEqual(IntercomEvent.objects.count(), 0)

        with override_settings(SKIP_INTERCOM=False):
            with requests_mock.Mocker() as endpoints:
                url_events = "https://api.intercom.io/events/"
                url_users = "https://api.intercom.io/users/"
                endpoints.register_uri("POST", url_events)
                endpoints.register_uri("POST", url_users)

                ie = IntercomEvent.objects.create(
                    user=self.user,
                    type=IntercomEvent.TYPE_EXAMPLE_EVENT,
                )
                self.assertFalse(ie.is_sent)
                ie.refresh_from_db()
                events = IntercomEvent.objects.all()

                for e in events:
                    self.assertEqual(e.type, IntercomEvent.TYPE_EXAMPLE_EVENT)

                self.assertTrue(ie.is_sent)

    def test_intercom_user_last_seen(self):
        self._create_user()
        # # clearing intercom last API response as creating user sets this
        # Account.objects.filter(pk=self.user.pk).update(intercom_last_api_response=None)
        self.user.refresh_from_db()
        self.assertIsNone(self.user.intercom_last_api_response)

        with requests_mock.Mocker() as endpoints:
            url_users = "https://api.intercom.io/users/"
            endpoints.register_uri("POST", url_users, text=json.dumps(self.intercom_user))
            # login
            self._login()
            self.user.refresh_from_db()
            self.assertIsNone(self.user.intercom_last_api_response)
            with override_settings(SKIP_INTERCOM=False):
                # simulate authentication scenario (for example in authenticate_credentials() method)
                push_account_last_seen_task.apply_async(args=[self.user.id], countdown=100)
                self.user.refresh_from_db()
                self.assertIsNotNone(self.user.intercom_last_api_response)
