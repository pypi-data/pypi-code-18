from django.db import models
from django.conf import settings
from .exceptions import *
import requests

MAILGUN_V3_BASE = 'https://api.mailgun.net/v3'

MAIL_STATUSES = [
    (0, '')
]


class Mail(models.Model):
    sender = models.EmailField()
    sender_title = models.CharField(blank=True, null=True, default='', max_length=200)
    recipient = models.EmailField()
    subject = models.CharField(max_length=200)
    body = models.TextField(max_length=5000)
    delivered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Mail'

    def _send_mailgun_v3(self):
        if 'DOMAIN' not in settings.MAAS:
            raise MaasConfigurationException('MAAS.DOMAIN must be defined in settings')

        if 'API_KEY' not in settings.MAAS:
            raise MaasConfigurationException('MAAS.DOMAIN must be defined in settings')

        url = '{}/{}/messages'.format(MAILGUN_V3_BASE, settings.MAAS['DOMAIN'])
        auth = ('api', settings.MAAS['API_KEY'])
        data = {
            'from': '{} <{}>'.format(self.sender_title, self.sender),
            'to': [ self.recipient ],
            'subject': self.subject,
            'text': self.body
        }

        res = requests.post(url, auth=auth, data=data)

        if res.status_code == 400:
            raise MaasUnknownException('Mailgun reported a bad request was made. Please report this error to django-maas.')

        if res.status_code == 401:
            raise MaasConfigurationException('MAAS.API_KEY seems to be invalid.')

        if res.status_code == 402:
            raise MaasUnknownException('Mailgun reported that the parameters were valid but the request failed. It is unclear what this means. Please report this error to django-maas.')

        if res.status_code == 404:
            raise MaasConfigurationException('MAAS.DOMAIN seems to be invalid,')

        if res.status_code in [500, 502, 503, 504]:
            raise MaasProviderException('Mailgun encountered an error on their end')

        try:
            res.raise_for_status()
        except:
            raise MaasUnknownException('Mailgun returned an undocumented status code {}. Please report this error to django-maas.'.format(res.status_code))

        self.delivered = True
        self.save()


    def send(self):
        provider_methods = {
            'MAILGUN_V3': self._send_mailgun_v3
        }

        if not hasattr(settings, 'MAAS'):
            raise MaasConfigurationException('MAAS must be defined in settings')

        if 'PROVIDER' not in settings.MAAS:
            raise MaasConfigurationException('MAAS.PROVIDER must be set')

        if settings.MAAS['PROVIDER'] not in provider_methods:
            raise MaasConfigurationException('MAAS.PROVIDER is invalid')

        provider_methods[settings.MAAS['PROVIDER']]()