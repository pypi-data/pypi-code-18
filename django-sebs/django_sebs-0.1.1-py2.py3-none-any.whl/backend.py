# -*- coding: utf-8 -*-
import boto3
import botocore
from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend


class SESEmailBackend(BaseEmailBackend):
    """
    A boto3 wrapper around the django mail backend, this allows to
    send your emails through amazon SES.
    """

    def __init__(self, fail_silently=False, **kwargs):
        super(SESEmailBackend, self).__init__(fail_silently=fail_silently, **kwargs)
        self.connection = None

    def open(self):
        self.connection = boto3.client('ses',
                                       aws_access_key_id=settings.SES_ACCESS_KEY,
                                       aws_secret_access_key=settings.SES_SECRET_KEY,
                                       region_name=settings.SES_REGION)

    def close(self):
        self.connection = None

    def send_messages(self, email_messages):
        self.open()
        num_sent = 0

        for message in email_messages:
            sent = self._send(message)
            if sent:
                num_sent += 1

        self.close()

        return num_sent

    def _send(self, message):
        try:
            self.connection.send_email(
                Source=message.from_email,
                Destination={'ToAddresses': message.to},
                Message={'Subject': {'Data': message.subject,
                                     'Charset': 'utf-8'},
                         'Body': {'Text': {'Data': message.body,
                                           'Charset': 'utf-8'},
                                  'Html': {'Data': message.body,
                                           'Charset': 'utf-8'}}}
            )
        except botocore.exceptions.ClientError:
            if not self.fail_silently:
                raise
            return False
        return True
