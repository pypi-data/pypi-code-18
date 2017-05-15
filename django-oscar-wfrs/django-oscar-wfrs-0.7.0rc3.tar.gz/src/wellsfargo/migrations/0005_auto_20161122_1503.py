# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-11-22 15:03
from __future__ import unicode_literals

from django.db import migrations


def add_missing_billing_addresses(apps, schema_editor):
    Country = apps.get_model("address", "Country")
    BillingAddress = apps.get_model("order", "BillingAddress")
    USCreditApp = apps.get_model("wellsfargo", "USCreditApp")
    USJointCreditApp = apps.get_model("wellsfargo", "USJointCreditApp")
    CACreditApp = apps.get_model("wellsfargo", "CACreditApp")
    CAJointCreditApp = apps.get_model("wellsfargo", "CAJointCreditApp")

    for AppType in (USCreditApp, USJointCreditApp, CACreditApp, CAJointCreditApp):
        applications = AppType.objects\
            .exclude(account=None)\
            .filter(account__wfrs_metadata__billing_address=None)\
            .all()
        for application in applications:
            billing_address = BillingAddress(**{
                'first_name': application.main_first_name or '',
                'last_name': application.main_last_name or '',
                'line1': application.main_address_line1 or '',
                'line2': application.main_address_line2 or '',
                'line4': application.main_address_city or '',
                'state': application.main_address_state or '',
                'postcode': application.main_address_postcode or '',
                'country': Country.objects.get(iso_3166_1_a2=application.region),
            })
            billing_address.save()
            wfrs_metadata = application.account.wfrs_metadata
            wfrs_metadata.billing_address = billing_address
            wfrs_metadata.save()


def add_missing_billing_addresses_reverse(apps, schema_editor):
    # no op
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('wellsfargo', '0004_auto_20161122_1357'),
    ]

    operations = [
        migrations.RunPython(add_missing_billing_addresses, add_missing_billing_addresses_reverse),
    ]
