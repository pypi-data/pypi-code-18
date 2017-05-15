from django.utils.translation import ugettext_lazy as _
from oscar.defaults import OSCAR_DASHBOARD_NAVIGATION


def insert_nav_item(after_name, label, url_name):
    new_entry = {
        'label': label,
        'url_name': url_name,
    }
    for i, section in enumerate(OSCAR_DASHBOARD_NAVIGATION):
        for j, entry in enumerate(section.get('children', [])):
            if entry.get('url_name') == after_name:
                OSCAR_DASHBOARD_NAVIGATION[i]['children'].insert(j + 1, new_entry)


insert_nav_item('dashboard:offer-list', _('Benefits'), 'dashboard:benefit-list')
insert_nav_item('dashboard:benefit-list', _('Conditions'), 'dashboard:condition-list')
insert_nav_item('dashboard:benefit-list', _('Offer Groups'), 'dashboard:offergroup-list')



BLUELIGHT_BENEFIT_CLASSES = [
    ('oscarbluelight.offer.benefits.BluelightPercentageDiscountBenefit', _("Discount is a percentage off of the product's value")),
    ('oscarbluelight.offer.benefits.BluelightAbsoluteDiscountBenefit', _("Discount is a fixed amount off of the product's value")),
    ('oscarbluelight.offer.benefits.BluelightMultibuyDiscountBenefit', _("Discount is to give the cheapest product for free")),
    ('oscarbluelight.offer.benefits.BluelightFixedPriceBenefit', _("Get the products in the range for a fixed price")),
    ('oscarbluelight.offer.benefits.BluelightShippingAbsoluteDiscountBenefit', _("Discount is a fixed amount of the shipping cost")),
    ('oscarbluelight.offer.benefits.BluelightShippingFixedPriceBenefit', _("Get shipping for a fixed price")),
    ('oscarbluelight.offer.benefits.BluelightShippingPercentageDiscountBenefit', _("Discount is a percentage off of the shipping cost")),
]


BLUELIGHT_CONDITION_CLASSES = [
    ('oscarbluelight.offer.conditions.BluelightCountCondition', _("Depends on number of items in basket that are in condition range")),
    ('oscarbluelight.offer.conditions.BluelightValueCondition', _("Depends on value of items in basket that are in condition range")),
    ('oscarbluelight.offer.conditions.BluelightCoverageCondition', _("Needs to contain a set number of DISTINCT items from the condition range")),
]
