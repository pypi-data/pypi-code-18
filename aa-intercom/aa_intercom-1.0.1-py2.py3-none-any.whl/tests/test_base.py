# -*- coding: utf-8 -*-
import json
from datetime import datetime

import mock
import requests_mock
from django.core import mail
from django.test.utils import override_settings
from freezegun import freeze_time
from intercom.errors import IntercomError, MultipleMatchingUsersError, ServiceUnavailableError
from test_project.models import UserModel

from aa_intercom.models import IntercomEvent
from aa_intercom.tasks import (push_account_last_seen_task, push_account_task, push_intercom_event_task,
                               push_not_registered_user_data_task)
from aa_intercom.tests.test_utils import BaseTestCase
from aa_intercom.utils import upload_not_registered_user_data

EVENT_TYPE_EXAMPLE = "example"


class FakeIntercomUserService(object):
    def create(self, *args, **kwargs):
        raise ServiceUnavailableError


class FakeIntercom(object):
    @property
    def users(self):
        return FakeIntercomUserService()


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

            # test case in which user does not exist (was removed in the meantime)
            user_id = 8282
            with self.assertRaises(UserModel.DoesNotExist):
                UserModel.objects.get(pk=user_id)

            with mock.patch("aa_intercom.tasks.cache.delete") as mocked_delete:
                push_account_task.apply_async(args=[user_id])
                mocked_delete.assert_called()

    @freeze_time("2017-01-01")
    @override_settings(SKIP_INTERCOM=False)
    def test_not_registered_user_data_upload(self):
        with requests_mock.Mocker() as m:
            url = "https://api.intercom.io/users/"
            m.register_uri("POST", url, text=json.dumps(self.intercom_user))
            push_not_registered_user_data_task.apply_async(args=[{
                k: self.intercom_user[k] for k in ["email", "name", "pseudonym"]
            }])
            self.assertTrue(m.called)
            self.assertDictEqual(m.last_request.json(), {
                "email": self.intercom_user["email"],
                "name": self.intercom_user["name"],
                "last_request_at": datetime.now().strftime("%s"),
                "custom_attributes": {
                    "pseudonym": self.intercom_user["pseudonym"]
                }
            })

        # assure push_account task does not fail in case of ServiceUnavailableError
        with mock.patch("aa_intercom.utils.intercom", FakeIntercom()):
            self._create_user()
            last_api_response_timestamp = self.user.intercom_api_response_timestamp
            self.user.refresh_from_db()
            self.assertEqual(self.user.intercom_api_response_timestamp, last_api_response_timestamp)

        # make sure cache is deleted in case of an error
        with mock.patch("aa_intercom.tasks.upload_not_registered_user_data", side_effect=MultipleMatchingUsersError()):
            with mock.patch("aa_intercom.tasks.cache.delete") as mocked_delete:
                with self.assertRaises(MultipleMatchingUsersError):
                    push_not_registered_user_data_task.apply_async(args=[{
                        "email": "foo@bar.bar"
                    }])
                    mocked_delete.assert_called()

        # test sending data other than a dictionary
        with self.assertRaises(NotImplementedError):
            upload_not_registered_user_data(object())

        # test sending data without the "email" keyword
        with self.assertRaises(KeyError):
            upload_not_registered_user_data({"name": "n"})

    def test_intercom_example_event(self):
        self._create_user()
        mail.outbox = []
        self.assertEqual(IntercomEvent.objects.count(), 0)

        with override_settings(SKIP_INTERCOM=False):
            with requests_mock.Mocker() as endpoints:
                url_events = "https://api.intercom.io/events/"
                url_users = "https://api.intercom.io/users/"
                endpoints.register_uri("POST", url_events)
                endpoints.register_uri("POST", url_users)

                ie = IntercomEvent.objects.create(user=self.user, type=EVENT_TYPE_EXAMPLE, metadata={"abc": 1})
                self.assertFalse(ie.is_sent)
                ie.refresh_from_db()
                events = IntercomEvent.objects.all()

                for e in events:
                    self.assertEqual(e.type, EVENT_TYPE_EXAMPLE)

                self.assertTrue(ie.is_sent)

                # test resending event - already sent, should not be sent again
                last_api_response = self.user.intercom_last_api_response
                ie.save()
                self.assertEqual(last_api_response, self.user.intercom_last_api_response)

        # test sending event w/o user
        with mock.patch("aa_intercom.tasks.upload_not_registered_user_data") as mocked_upload:
            metadata = {"email": "foo@bar.foo"}
            IntercomEvent.objects.create(type=EVENT_TYPE_EXAMPLE, metadata=metadata)
            mocked_upload.assert_called_with(metadata)

        # test handling Intercom API errors
        with mock.patch("aa_intercom.tasks.upload_intercom_user") as mocked_upload:
            mocked_upload.side_effect = IntercomError("Unknown Error")
            with self.assertRaises(IntercomError):
                ie = IntercomEvent.objects.create(user=self.user, type=EVENT_TYPE_EXAMPLE)
                ie.refresh_from_db()
                self.assertFalse(ie.is_sent)

        # test case in which event was removed in meantime (before the task ran)
        # make sure the cache is deleted
        event_id = 8282
        with self.assertRaises(IntercomEvent.DoesNotExist):
            IntercomEvent.objects.get(pk=event_id)
        with mock.patch("aa_intercom.tasks.upload_not_registered_user_data", side_effect=IntercomEvent.DoesNotExist()):
            with mock.patch("aa_intercom.tasks.cache.delete") as mocked_delete:
                with self.assertRaises(IntercomEvent.DoesNotExist):
                    push_intercom_event_task(event_id)
                    mocked_delete.assert_called()

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
                push_account_last_seen_task.apply_async(args=[self.user.id])
                self.user.refresh_from_db()
                self.assertIsNotNone(self.user.intercom_last_api_response)
