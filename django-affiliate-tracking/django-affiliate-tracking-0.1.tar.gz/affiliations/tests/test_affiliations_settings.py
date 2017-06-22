from django.test import TestCase


class TestAffiliateTrackingSettings(TestCase):

    def test_import_default_settings(self):
        from affiliations.affiliations_settings import (
            AFFILIATE_SESSION_KEY,
            AFFILIATE_QUERY_STRING_KEY,
        )

        self.assertEqual(
            AFFILIATE_SESSION_KEY,
            'affiliate_visitor_id'
        )
        self.assertEqual(
            AFFILIATE_QUERY_STRING_KEY,
            'affiliate_id'
        )
