# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-28 21:23
from __future__ import unicode_literals

from django.db import migrations


def migrate_from_oscar_accounts(apps, schema_editor):
    from ..security import encrypt_account_number
    TransferMetadata = apps.get_model("wellsfargo", "TransferMetadata")
    for meta in TransferMetadata.objects.all():
        meta.amount = meta.transfer.amount
        meta.merchant_reference = meta.transfer.merchant_reference
        meta.user = meta.transfer.user
        meta.last4_account_number = meta.transfer.source.wfrs_metadata.account_number[-4:]
        meta.encrypted_account_number = encrypt_account_number(meta.transfer.source.wfrs_metadata.account_number)
        meta.created_datetime = meta.transfer.date_created
        meta.modified_datetime = meta.transfer.date_created
        meta.save()

    USCreditApp = apps.get_model("wellsfargo", "USCreditApp")
    USJointCreditApp = apps.get_model("wellsfargo", "USJointCreditApp")
    CACreditApp = apps.get_model("wellsfargo", "CACreditApp")
    CAJointCreditApp = apps.get_model("wellsfargo", "CAJointCreditApp")
    for AppType in (USCreditApp, USJointCreditApp, CACreditApp, CAJointCreditApp):
        for app in AppType.objects.all():
            account_number = None
            if app.account:
                app.last4_account_number = app.account.wfrs_metadata.account_number[-4:]
                app.save()


class Migration(migrations.Migration):

    dependencies = [
        ('wellsfargo', '0009_drop_oscar_accounts_1'),
    ]

    operations = [
        # Copy field data from oscar_accounts over to new fields on our model
        migrations.RunPython(migrate_from_oscar_accounts),
    ]
