from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone

from affiliations.models import (
    Partner,
    Subscription,
    Visitor,
)
from affiliations.exceptions import InvalidCallBackURL

User = get_user_model()


class TestPartner(TestCase):

    def test_create(self):
        partner = Partner.objects.create(
            name='partner'
        )

        self.assertIsNotNone(partner)

    def test_default_uid(self):
        partner = Partner.objects.create(
            name='partner'
        )

        self.assertEqual(len(partner.uid), 8)

    def test_update(self):
        partner = Partner.objects.create(
            name='partner'
        )
        partner.name = 'partner updated'
        partner.save()

        self.assertEqual(partner.name, 'partner updated')

    def test_delete(self):
        partner = Partner.objects.create(
            name='partner'
        )
        partner_pk = partner.pk
        partner.delete()

        self.assertFalse(Partner.objects.filter(pk=partner_pk).exists())

    def test__str__(self):
        partner = Partner.objects.create(
            name='partner'
        )

        self.assertEqual(str(partner), partner.name)


class TestSubscription(TestCase):

    def setUp(self):
        self.partner = Partner.objects.create()

    def test_create(self):
        subscription = Subscription.objects.create(
            partner=self.partner
        )

        self.assertIsNotNone(subscription)

    def test_partner(self):
        subscription = Subscription.objects.create(
            partner=self.partner
        )

        self.assertEqual(self.partner, subscription.partner)

    def test_update(self):
        subscription = Subscription.objects.create(
            partner=self.partner
        )
        subscription.trigger = 'trigger updated'
        subscription.save()

        self.assertEqual(subscription.trigger, 'trigger updated')

    def test_delete(self):
        subscription = Subscription.objects.create(
            partner=self.partner
        )
        subscription_pk = subscription.pk
        subscription.delete()

        self.assertFalse(
            Subscription.objects.filter(pk=subscription_pk).exists()
        )

    def test__str__(self):
        subscription = Subscription.objects.create(
            partner=self.partner
        )

        self.assertEqual(str(subscription), subscription.trigger)

    def test_validate_callback_url_field_empty(self):
        subscription = Subscription.objects.create(
            partner=self.partner
        )

        with self.assertRaises(InvalidCallBackURL):
            subscription.validate_callback_url()

    def test_validate_callback_url_field_wrong_value(self):
        # The callback_url does not contain the {visitor_id} placeholder
        with self.assertRaises(InvalidCallBackURL):
            Subscription.objects.create(
                partner=self.partner,
                callback_url='http://example.com'
            )

    def test_validate_callback_url_field_right_value(self):
        right_callback_url = 'http://example.com/?{}'.format(
            Subscription.CALLBACK_URL_PLACEHOLDER
        )
        subscription = Subscription.objects.create(
            partner=self.partner,
            callback_url=right_callback_url
        )

        self.assertEqual(subscription.callback_url, right_callback_url)


class TestVisitor(TestCase):

    def setUp(self):
        self.partner = Partner.objects.create()
        self.user = User.objects.create_user(
            username='test_user',
            email='test@test.com',
            password='StrongPass123**'
        )

    def test_create(self):
        visitor = Visitor.objects.create(
            partner=self.partner,
            user=self.user
        )

        self.assertIsNotNone(visitor)

    def test_partner(self):
        visitor = Visitor.objects.create(
            partner=self.partner,
            user=self.user
        )

        self.assertEqual(visitor.partner, self.partner)

    def test_user(self):
        visitor = Visitor.objects.create(
            partner=self.partner,
            user=self.user
        )

        self.assertEqual(visitor.user, self.user)

    def test_referred_on(self):
        visitor = Visitor.objects.create(
            partner=self.partner,
            user=self.user
        )

        self.assertIsNotNone(visitor.referred_on)

    def test_entry_point(self):
        visitor = Visitor.objects.create(
            partner=self.partner,
            user=self.user,
            entry_point='http://example.com'
        )

        self.assertEqual(visitor.entry_point, 'http://example.com')

    def test_successful_on(self):
        visitor = Visitor.objects.create(
            partner=self.partner,
            user=self.user
        )

        self.assertIsNone(visitor.successful_on)

    def test_update(self):
        visitor = Visitor.objects.create(
            partner=self.partner,
            user=self.user
        )
        visitor.entry_point = 'http://example.com'
        visitor.save()

        self.assertEqual(visitor.entry_point, 'http://example.com')

    def test__str__(self):
        visitor = Visitor.objects.create(
            partner=self.partner,
            user=self.user
        )

        self.assertEqual(str(visitor), visitor.entry_point)

    def test_delete(self):
        visitor = Visitor.objects.create(
            partner=self.partner,
            user=self.user
        )
        visitor_pk = visitor.pk
        visitor.delete()

        self.assertFalse(Visitor.objects.filter(pk=visitor_pk).exists())

    def test_succeed_no_user_specified(self):
        visitor = Visitor.objects.create(
            partner=self.partner,
            user=self.user
        )

        # this must only happen if the value of successful_on is None
        self.assertIsNone(visitor.successful_on)
        visitor.succeed()
        # succeed will set the successful_on to now()
        self.assertIsNotNone(visitor.successful_on)
        # if user is specified - set the user value for the visitor. This was
        # not specified so the user should not change for the visitor
        self.assertEqual(visitor.user, self.user)

    def test_succeed_user_specified(self):
        visitor = Visitor.objects.create(
            partner=self.partner,
            user=self.user
        )

        new_user = User.objects.create_user(
            username='test_new_user',
            email='test@test.com',
            password='StrongPass123**'
        )
        # this must only happen if the value of successful_on is None
        self.assertIsNone(visitor.successful_on)
        visitor.succeed(new_user)
        # succeed will set the successful_on to now()
        self.assertIsNotNone(visitor.successful_on)
        # if user is specified - set the user value for the visitor. This was
        # not specified so the user should not change for the visitor
        self.assertEqual(visitor.user, new_user)

    def test_succeed_successful_on_not_none(self):
        now = timezone.now()
        visitor = Visitor.objects.create(
            partner=self.partner,
            user=self.user,
            successful_on=now
        )

        new_user = User.objects.create_user(
            username='test_new_user_second',
            email='test@test.com',
            password='StrongPass123**'
        )
        visitor.succeed(new_user)

        # this must only happen if the value of successful_on is None, so
        # the user, and successful_on should not change
        self.assertEqual(visitor.successful_on, now)
        self.assertEqual(visitor.user, self.user)
