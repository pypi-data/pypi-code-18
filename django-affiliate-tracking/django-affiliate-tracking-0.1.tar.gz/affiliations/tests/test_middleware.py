from django.test import (
    TestCase,
    RequestFactory,
)
from django.contrib.auth import get_user_model
from django.http import (
    HttpResponse,
)

from affiliations.models import (
    Visitor,
    Partner,
)
from affiliations.middleware import (
    AffiliateVisitorsRegistrationMiddleware,
)
from affiliations.affiliations_settings import (
    AFFILIATE_QUERY_STRING_KEY,
    AFFILIATE_SESSION_KEY,
)

User = get_user_model()


class TestMiddleware(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_affiliate_visitor_property_is_set(self):
        """
        Will check that the affiliate_visitor property is set on the request
        after the process_request is called for the middleware.
        """
        request = self.factory.get('/')
        request.session = {}
        AffiliateVisitorsRegistrationMiddleware().process_request(
            request
        )

        self.assertIn('affiliate_visitor', request.__dict__.keys())

    def test_affiliate_visitor_property_session_key_not_set(self):
        """
        Will check that the affiliate_visitor property is None after the
        process_request is called for the middleware.
        """
        request = self.factory.get('/')
        request.session = {}
        AffiliateVisitorsRegistrationMiddleware().process_request(request)

        # - If AFFILIATE_SESSION_KEY is not set in the session, assign a
        # value of None to the property.
        self.assertIsNone(request.affiliate_visitor)

    def test_affiliate_visitor_property_session_key_set_visitor_not_found(
            self
    ):
        """
        Will unset the session value because the visitor was not found, which
        means it is broken.
        """
        visitor = Visitor(pk=123)
        request = self.factory.get('/')
        request.session = {
            AFFILIATE_SESSION_KEY: visitor
        }

        # - If it is set, look up the visitor by its id. If a visitor is
        #   found, assign this instance as the value of the property.
        #   Otherwise, unset the session value, as it is obviously broken.
        self.assertIn(
            AFFILIATE_SESSION_KEY,
            request.session.keys()
        )
        AffiliateVisitorsRegistrationMiddleware().process_request(request)
        self.assertIsNone(request.affiliate_visitor)

    def test_affiliate_visitor_property_session_key_set_visitor_found(
            self
    ):
        """
        Will set the visitor to the property because the visitor was found.
        """
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
        request = self.factory.get('/')
        request.session = {
            AFFILIATE_SESSION_KEY: visitor
        }
        # - If it is set, look up the visitor by its id. If a visitor is
        #   found, assign this instance as the value of the property.
        self.assertIn(
            AFFILIATE_SESSION_KEY,
            request.session.keys()
        )
        AffiliateVisitorsRegistrationMiddleware().process_request(request)

        self.assertEqual(request.affiliate_visitor, visitor)

    def test_affiliate_query_not_found(self):
        """
        Check for the existence of the AFFILIATE_QUERY_STRING_KEY in the
        query string, return properly for a middleware if not.
        """
        request = self.factory.get('/')
        request.session = {}
        self.assertNotIn(
            AFFILIATE_QUERY_STRING_KEY,
            request.get_full_path()
        )
        original_response = HttpResponse()
        response = AffiliateVisitorsRegistrationMiddleware().process_response(
            request,
            original_response
        )

        self.assertEqual(response, original_response)

    def test_affiliate_query_found_not_uid_match_for_partner(self):
        """
        Check whether the AFFILIATE_QUERY_STRING_KEY matches the uid of an
        active partner. If not, strip away the affiliate part of the URL and
        do a redirect to the resulting URL.
        """
        original_response = HttpResponse()
        request = self.factory.get(
            '/?{}={}'.format(
                AFFILIATE_QUERY_STRING_KEY,
                'abcd1234'
            )
        )
        self.assertIn(
            AFFILIATE_QUERY_STRING_KEY,
            request.get_full_path()
        )
        response = AffiliateVisitorsRegistrationMiddleware().process_response(
            request,
            original_response
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')

    def test_affiliate_query_found_uid_match_for_partner_get_request(self):
        """
        If an active partner is found:
            - Create a new visitor instance, set the entry_point to the URL of
            the request stripped from the affiliation part.
            - Set the value for AFFILIATE_SESSION_KEY in the session to the id
            of the visitor instance.
            - Set the value of the affiliate_visitor request property to the
            new visitor instance.
            - Strip away the affiliate part of the URL and do a redirect to the
            resulting URL.

        Redirects must only happen for GET requests.
        POST requests must pass for further processing.
        """
        partner = Partner.objects.create(active=True)
        original_response = HttpResponse()
        user = User.objects.create_user(
            username='visitor_user',
            email='test@test.com',
            password='StrongPass123**'
        )
        request = self.factory.get(
            '/?{}={}'.format(
                AFFILIATE_QUERY_STRING_KEY,
                partner.uid
            )
        )
        request.user = user
        request.session = {}
        self.assertIn(
            AFFILIATE_QUERY_STRING_KEY,
            request.get_full_path()
        )
        response = AffiliateVisitorsRegistrationMiddleware().process_response(
            request,
            original_response
        )

        visitor = Visitor.objects.filter(user=user, partner=partner).first()
        # - Create a new visitor instance, set the entry_point to the URL of
        #     the request stripped from the affiliation part.
        self.assertIsNotNone(visitor)
        self.assertEqual(visitor.entry_point, '/')

        # - Set the value for AFFILIATE_SESSION_KEY in the session to the id
        # of the visitor instance.
        self.assertEqual(
            request.session[AFFILIATE_SESSION_KEY],
            visitor.pk
        )

        # - Set the value of the affiliate_visitor request property to the
        # new visitor instance.
        self.assertEqual(
            request.affiliate_visitor,
            visitor
        )

        # - Strip away the affiliate part of the URL and do a redirect to the
        # resulting URL. Redirects must only happen for GET requests.
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')

    def test_affiliate_query_post_request(self):
        """
        Redirects must only happen for GET requests.
        POST requests must pass for further processing.
        """
        original_response = HttpResponse()
        request = self.factory.post(
            '/?{}={}'.format(
                AFFILIATE_QUERY_STRING_KEY,
                'abcd1234'
            )
        )
        response = AffiliateVisitorsRegistrationMiddleware().process_response(
            request,
            original_response
        )

        self.assertEqual(response, original_response)
