from django.apps import AppConfig
from django.test import TestCase
from django.test.utils import override_settings

import affiliations
from affiliations.apps import AffiliateTrackingConfig
from affiliations.models import Partner


class TestAffiliateTrackingConfig(TestCase):

    @override_settings(
        AFFILIATE_TRIGGERS=[
            (
                'Partner updated',
                'django.db.models.signals.post_save',
                'affiliations.tests.utils.partner_updated',
                'affiliations.models.Partner',
            )
        ]
    )
    def setUp(self):
        self.affiliate_tracking_config = AffiliateTrackingConfig(
            'affiliations',
            affiliations
        )
        self.affiliate_tracking_config.ready()

    def test_name(self):
        self.assertEqual(
            self.affiliate_tracking_config.name,
            'affiliations'
        )
        self.assertTrue(issubclass(AffiliateTrackingConfig, AppConfig))

    def test_ready(self):
        partner = Partner.objects.create()
        partner.name = 'Partner updated'
        partner.save()

        partner.refresh_from_db()
        # The active = True is set by the receiver that was created for this
        # test
        self.assertTrue(partner.active)
