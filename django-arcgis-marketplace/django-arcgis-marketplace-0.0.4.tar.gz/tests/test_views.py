from django.test import TestCase
from django.urls import reverse

from arcgis_marketplace import factories


class ViewsTests(TestCase):

    def test_item_paypal_form_HTTP_200_OK(self):
        item = factories.ItemFactory()
        response = self.client.get(reverse(
            'arcgis-marketplace:item-paypal-form',
            args=(item.id.hex,)
        ))

        self.assertEqual(response.status_code, 200)
