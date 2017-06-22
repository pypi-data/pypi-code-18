"""The middleware regarding the affiliations application will live here."""

from __future__ import absolute_import
try:
    import urllib.parse as urlparse
except ImportError:
    import urlparse
try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode

from django.http import HttpResponseRedirect

from .models import (
    Visitor,
    Partner,
)
from .utils import (
    strip_affiliate_part_from_url,
    convert_url_query_string_to_dict,
)
from .affiliations_settings import (
    AFFILIATE_QUERY_STRING_KEY,
    AFFILIATE_SESSION_KEY,
)


class AffiliateVisitorsRegistrationMiddleware(object):
    """Middleware class to handle the affiliate visitors registrations."""

    def process_request(self, request):
        """
        Set an affiliate_visitor property on the request object.

        following these rules:
        - If AFFILIATE_SESSION_KEY is not set in the session, assign a
            value of None to the property.
        - If it is set, look up the visitor by its id. If a visitor is
            found, assign this instance as the value of the property.
        Otherwise, unset the session value, as it is obviously broken.
        """
        visitor = request.session.get(AFFILIATE_SESSION_KEY)
        if not visitor:
            request.affiliate_visitor = None
        else:
            visitor = Visitor.objects.filter(pk=visitor.pk).first()
            if visitor:
                request.affiliate_visitor = visitor
            else:
                del(request.session[AFFILIATE_SESSION_KEY])
                request.affiliate_visitor = None

    def process_response(self, request, response):
        """
        Process the response.

        following these rules:
        - Check for the existence of the AFFILIATE_QUERY_STRING_KEY in the
        query string, return properly for a middleware if not.
        - Check whether the value matches the uid of an active partner.
         If not, strip away the affiliate part of the URL and do a redirect to
         the resulting URL.
        - If an active partner is found, create a new visitor instance, set
        the entry_point to the URL of the request stripped from the
        affiliation part.
        - Set the value for AFFILIATE_SESSION_KEY in the session to the id of
        the visitor instance.
        - Set the value of the affiliate_visitor request property to the new
        visitor instance.
        - Strip away the affiliate part of the URL and do a redirect to the
        resulting URL.

        Redirects must only happen for GET requests.
        POST requests must pass for further processing.
        """
        url_requested_path = request.get_full_path()
        # - Check for the existence of the AFFILIATE_QUERY_STRING_KEY in the
        # query string, return properly for a middleware if not.
        # Redirects must only happen for GET requests.
        if (AFFILIATE_QUERY_STRING_KEY not in url_requested_path or
           request.method != 'GET'):
            return response
        else:
            active_partner = Partner.objects.filter(
                active=True,
                uid=convert_url_query_string_to_dict(
                    url_requested_path
                )[AFFILIATE_QUERY_STRING_KEY]
            ).first()
            stripped_url = strip_affiliate_part_from_url(url_requested_path)
            # An active partner found
            if active_partner:
                # Create a new visitor instance, set the entry_point to the URL
                # of the request stripped from the affiliation part.
                visitor = Visitor.objects.create(
                    partner=active_partner,
                    user=request.user,
                    entry_point=stripped_url
                )
                # Set the value for AFFILIATE_SESSION_KEY in the session to the
                # id of the visitor instance.
                request.session[AFFILIATE_SESSION_KEY] = visitor.pk
                # Set the value of the affiliate_visitor request property to
                # the new visitor instance.
                request.affiliate_visitor = visitor

            return HttpResponseRedirect(stripped_url)
