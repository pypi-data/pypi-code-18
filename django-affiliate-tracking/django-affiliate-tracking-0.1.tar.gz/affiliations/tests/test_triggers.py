"""For testing the triggers module"""

from django.test import (
    TestCase,
    RequestFactory,
)
from django.contrib.auth import get_user_model

from mock import mock

from affiliations.triggers import (
    complete_trigger,
    object_created,
    object_saved,
)
from affiliations.models import (
    Visitor,
    Partner,
    Subscription,
)
from affiliations.affiliations_settings import (
    AFFILIATE_SESSION_KEY,
)


User = get_user_model()
tls_request = RequestFactory().get('/')


class TestTriggers(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.affiliate_trigger_name = 'Partner updated'
        self.trigger_name_object_created = 'object_created trigger name'
        self.trigger_name_object_saved = 'object_saved trigger name'

    def test_complete_trigger_affiliate_visitor_not_in_request(self):
        visitors_successful_on_none_before_complete_trigger_count = (
            Visitor.objects.filter(
                successful_on__isnull=True
            ).count()
        )
        request = self.factory.get('/')
        complete_trigger(request, self.affiliate_trigger_name)

        # Check whether the affiliate_visitor of the request has a value.
        # If the visitor is not found do not proceed.
        self.assertNotIn('affiliate_visitor', request.__dict__.keys())
        self.assertEqual(
            visitors_successful_on_none_before_complete_trigger_count,
            Visitor.objects.filter(
                successful_on__isnull=True
            ).count()
        )

    def test_complete_trigger_affiliate_visitor_in_request_visitor_not_found(
            self
    ):
        visitors_successful_on_none_before_complete_trigger_count = (
            Visitor.objects.filter(
                successful_on__isnull=True
            ).count()
        )
        request = self.factory.get('/')
        request.affiliate_visitor = Visitor(pk=12345)
        complete_trigger(request, self.affiliate_trigger_name)

        # Check whether the affiliate_visitor of the request has a value.
        # If the visitor is not found do not proceed.
        self.assertIn('affiliate_visitor', request.__dict__.keys())
        self.assertEqual(
            visitors_successful_on_none_before_complete_trigger_count,
            Visitor.objects.filter(
                successful_on__isnull=True
            ).count()
        )

    def test_complete_trigger_affiliate_visitor_in_request_partner_not_active(
            self
    ):
        partner = Partner.objects.create()
        user = User.objects.create_user(
            username='test_user',
            email='test@test.com',
            password='StrongPass123**'
        )
        visitor = Visitor.objects.create(
            partner=partner,
            user=user
        )
        visitors_successful_on_none_before_complete_trigger_count = (
            Visitor.objects.filter(
                successful_on__isnull=True
            ).count()
        )
        request = self.factory.get('/')
        request.affiliate_visitor = visitor
        complete_trigger(request, self.affiliate_trigger_name)

        # If the visitor is found, check that the partner of the visitor is
        # active.
        # If not, do not proceed.
        self.assertIn('affiliate_visitor', request.__dict__.keys())
        self.assertEqual(
            visitors_successful_on_none_before_complete_trigger_count,
            Visitor.objects.filter(
                successful_on__isnull=True
            ).count()
        )

    def test_complete_trigger_affiliate_visitor_in_request_not_subscribed(
            self
    ):
        partner = Partner.objects.create(active=True)
        user = User.objects.create_user(
            username='test_user',
            email='test@test.com',
            password='StrongPass123**'
        )
        visitor = Visitor.objects.create(
            partner=partner,
            user=user
        )
        visitors_successful_on_none_before_complete_trigger_count = (
            Visitor.objects.filter(
                successful_on__isnull=True
            ).count()
        )
        request = self.factory.get('/')

        request.affiliate_visitor = visitor
        complete_trigger(request, self.affiliate_trigger_name)

        # If the visitor is found, check that the partner of the visitor is
        # active, and that it is subscribed to the trigger with the provided
        # name.
        # If not, do not proceed.
        self.assertIn('affiliate_visitor', request.__dict__.keys())
        self.assertEqual(
            visitors_successful_on_none_before_complete_trigger_count,
            Visitor.objects.filter(
                successful_on__isnull=True
            ).count()
        )

    def test_complete_trigger_all_conditions_met(self):
        partner = Partner.objects.create(active=True)
        user = User.objects.create_user(
            username='test_user',
            email='test@test.com',
            password='StrongPass123**'
        )
        new_user = User.objects.create_user(
            username='new_test_user',
            email='test@test.com',
            password='StrongPass123**'
        )
        visitor = Visitor.objects.create(
            partner=partner,
            user=user
        )
        Subscription.objects.create(
            partner=partner,
            callback_url='http://example.com/?{}'.format(
                Subscription.CALLBACK_URL_PLACEHOLDER
            ),
            trigger=self.affiliate_trigger_name
        )
        visitors_successful_on_none_before_complete_trigger_count = (
            Visitor.objects.filter(
                successful_on__isnull=True
            ).count()
        )
        request = self.factory.get('/')
        request.affiliate_visitor = visitor
        request.session = {
            AFFILIATE_SESSION_KEY: visitor.pk
        }
        request.user = new_user
        complete_trigger(request, self.affiliate_trigger_name)

        # If the visitor is found, check that the partner of the visitor is
        # active, and that it is subscribed to the trigger with the provided
        # name. If so:
        #
        # - Do a callback to the partner subscription callback_url, after
        # properly substituting the visitor_id on the URL.
        # - Call succeed on the visitor, with the user of the request as an
        # argument,
        # - Unset the AFFILIATE_SESSION_KEY in the request session, as we now
        # consider the affiliate reference business done.
        self.assertEqual(
            visitors_successful_on_none_before_complete_trigger_count - 1,
            Visitor.objects.filter(
                successful_on__isnull=True
            ).count()
        )
        visitor.refresh_from_db()
        self.assertEqual(visitor.user, request.user)
        self.assertNotIn(
            AFFILIATE_SESSION_KEY,
            request.session.keys()
        )

    @mock.patch(
        'affiliations.triggers.tls_request',
        tls_request
    )
    def test_object_created(self):
        partner = Partner.objects.create(active=True)
        user = User.objects.create_user(
            username='test_user',
            email='test@test.com',
            password='StrongPass123**'
        )
        new_user = User.objects.create_user(
            username='new_test_user',
            email='test@test.com',
            password='StrongPass123**'
        )
        visitor = Visitor.objects.create(
            partner=partner,
            user=user
        )
        Subscription.objects.create(
            partner=partner,
            callback_url='http://example.com/?{}'.format(
                Subscription.CALLBACK_URL_PLACEHOLDER
            ),
            trigger=self.trigger_name_object_created
        )
        tls_request.affiliate_visitor = visitor
        tls_request.session = {
            AFFILIATE_SESSION_KEY: visitor.pk
        }
        tls_request.user = new_user

        visitors_successful_on_none_before_object_created_count = (
            Visitor.objects.filter(
                successful_on__isnull=True
            ).count()
        )

        object_created(
            Visitor,
            Visitor.objects.first(),
            affiliate_trigger_name=self.trigger_name_object_created,
            created=True
        )

        # If the visitor is found, check that the partner of the visitor is
        # active, and that it is subscribed to the trigger with the provided
        # name. If so:
        #
        # - Do a callback to the partner subscription callback_url, after
        # properly substituting the visitor_id on the URL.
        # - Call succeed on the visitor, with the user of the request as an
        # argument,
        # - Unset the AFFILIATE_SESSION_KEY in the request session, as we now
        # consider the affiliate reference business done.
        self.assertEqual(
            visitors_successful_on_none_before_object_created_count - 1,
            Visitor.objects.filter(
                successful_on__isnull=True
            ).count()
        )
        visitor.refresh_from_db()
        self.assertEqual(visitor.user, tls_request.user)
        self.assertNotIn(
            AFFILIATE_SESSION_KEY,
            tls_request.session.keys()
        )

    @mock.patch(
        'affiliations.triggers.tls_request',
        tls_request
    )
    def test_object_saved(self):
        partner = Partner.objects.create(active=True)
        user = User.objects.create_user(
            username='test_user',
            email='test@test.com',
            password='StrongPass123**'
        )
        new_user = User.objects.create_user(
            username='new_test_user',
            email='test@test.com',
            password='StrongPass123**'
        )
        visitor = Visitor.objects.create(
            partner=partner,
            user=user
        )
        Subscription.objects.create(
            partner=partner,
            callback_url='http://example.com/?{}'.format(
                Subscription.CALLBACK_URL_PLACEHOLDER
            ),
            trigger=self.trigger_name_object_saved
        )
        tls_request.affiliate_visitor = visitor
        tls_request.session = {
            AFFILIATE_SESSION_KEY: visitor.pk
        }
        tls_request.user = new_user

        visitors_successful_on_none_before_object_saved_count = (
            Visitor.objects.filter(
                successful_on__isnull=True
            ).count()
        )

        object_saved(
            Visitor,
            Visitor.objects.first(),
            affiliate_trigger_name=self.trigger_name_object_saved
        )

        # If the visitor is found, check that the partner of the visitor is
        # active, and that it is subscribed to the trigger with the provided
        # name. If so:
        #
        # - Do a callback to the partner subscription callback_url, after
        # properly substituting the visitor_id on the URL.
        # - Call succeed on the visitor, with the user of the request as an
        # argument,
        # - Unset the AFFILIATE_SESSION_KEY in the request session, as we now
        # consider the affiliate reference business done.
        self.assertEqual(
            visitors_successful_on_none_before_object_saved_count - 1,
            Visitor.objects.filter(
                successful_on__isnull=True
            ).count()
        )
        visitor.refresh_from_db()
        self.assertEqual(visitor.user, tls_request.user)
        self.assertNotIn(
            AFFILIATE_SESSION_KEY,
            tls_request.session.keys()
        )
