# -*- encoding: utf-8 -*-
import logging
import json

from django.db import models

from django.conf import settings
from urllib2 import HTTPError


from datetime import date

# sendgrid
from sendgrid.helpers.mail import Mail, Email, OpenTracking, TrackingSettings, ClickTracking
from sendgrid.helpers.mail import Personalization, MailSettings, SandBoxMode
import sendgrid


sendgrid_api_client = sendgrid.SendGridAPIClient(
    apikey=settings.SENDGRID_API_KEY
).client


class ContactSendgridQuerySet(models.QuerySet):

    def sendgrid_upload(self):
        """
        Upload and up updates de contact Queryset to senddgrid
        Returns:
            QuerySet: A querySet of Contacts
        """
        request_body = [contact.email_data() for contact in self]
        response = sendgrid_api_client.contactdb.recipients.post(
            request_body=request_body
        )

        response = json.loads(response.body)

        for contact in self.exclude(sendgrid_id__in=response['persisted_recipients']):
            logging.error("Correo {} no valido".format(contact.email))

        return self.all()


class ContactList(models.Model):

    name = models.CharField(
        max_length=255,
    )

    sendgrid_id = models.CharField(
        max_length=255,
        unique=True,
        db_index=True,
        editable=False,
        null=True
    )

    def __unicode__(self):
        return u"{}".format(self.name)

    def save(self, *args, **kwargs):
        if self.name is u'':
            self.name = u"{}-{}".format(type(self).__name__, date.today())
        super(ContactList, self).save(*args, **kwargs)

    def contact_filter(self):
        """Filter the contacts that are going to be uploaded.

        Returns:
            QuerySet: Only the valid contacts
        """
        return self.contact_set

    def sendgrid_upload(self):
        if not self.sendgrid_check():
            try:
                response = sendgrid_api_client.contactdb.lists.post(
                    request_body={'name': self.name}
                )
                response = json.loads(response.body)
                self.sendgrid_id = response['id']
                self.save()
            except HTTPError as e:
                if e.code == 400:
                    logging.error('List all ready exists')
                else:
                    logging.error(e)
                raise e

    def sendgrid_check(self):
        if self.sendgrid_id:
            response = sendgrid_api_client.contactdb.lists._(self.sendgrid_id).get()
            response = json.loads(response.body)
            logging.debug(response)
            return self.name == response['name']
        return False

    def sendgrid_delete(self):
        if self.sendgrid_check():
            sendgrid_api_client.contactdb.lists._(self.sendgrid_id).delete()
            self.sendgrid_id = None
            self.save()

    def sendgrid_contact_upload(self):
        if self.contact_set.count() > 0:
            self.contact_set.sendgrid_upload()
            request_body = [contact.sendgrid_id for contact in self.contact_filter().all()]
            try:
                sendgrid_api_client.contactdb.lists._(self.sendgrid_id).recipients.post(
                    request_body=request_body
                )
            except HTTPError as e:
                logging.error(e)


class Contact(models.Model):
    """
    Base model for contact

    Attributes:
        contact_lists (TYPE): Description
        email (TYPE): Description
        objects (TYPE): Description
        sendgrid_id (CharField): should be the email encoded in base64
    """
    email = models.EmailField(max_length=255)
    contact_lists = models.ManyToManyField(ContactList)

    # This one should be the email encoded in base64
    sendgrid_id = models.CharField(
        max_length=255,
        unique=True,
        db_index=True,
        editable=False
    )

    objects = ContactSendgridQuerySet.as_manager()

    def __unicode__(self):
        return u"{} {}".format(self.email, self.sendgrid_id)

    def save(self, *args, **kwargs):
        self.email = self.email.lower()
        self.sendgrid_id = self.email.encode('base64')
        super(Contact, self).save(*args, **kwargs)

    def email_data(self):
        today = date.today().strftime('%s')

        return {
            'email': self.email,
            'upload_date': today,
        }

    def sendgrid_upload(self):
        type(self).objects.filter(id=self.id)\
            .sendgrid_upload()
        self.refresh_from_db()

    def sendgrid_check(self):
        logging.debug("{}:{}".format(self.email, self.sendgrid_id))
        if self.sendgrid_id == self.email.encode('base64'):
            try:
                response = sendgrid_api_client.contactdb.recipients._(self.sendgrid_id).get()
                response = json.loads(response.body)
                logging.debug("{} == {}".format(response['email'], self.email))
                return response['email'].lower() == self.email.lower()
            except HTTPError as e:
                logging.debug(e)
                if e.code == 400:
                    return False
                if e.code == 404:
                    return False
                else:
                    raise(e)
        return False

    def sendgrid_delete(self):
        if self.sendgrid_check():
            sendgrid_id = self.sendgrid_id
            try:
                sendgrid_api_client.contactdb.recipients._(sendgrid_id).delete()
                return sendgrid_id
            except HTTPError as e:
                logging.debug(e)
                if e.code == 400:
                    return sendgrid_id
                if e.code == 404:
                    return sendgrid_id
                else:
                    raise(e)


class Campaign(models.Model):

    template = models.IntegerField(null=True)

    title = models.CharField(
        max_length=100,
    )

    subject = models.CharField(
        max_length=500,
    )

    sender = models.IntegerField(null=True)

    html_content = models.TextField()

    plain_content = models.TextField()

    sendgrid_id = models.CharField(
        max_length=255,
        unique=True,
        db_index=True,
        editable=False,
        null=True
    )

    contact_list = models.ForeignKey(ContactList, null=True)

    def __unicode__(self):
        return u"{}".format(self.title)

    def save(self, *args, **kwargs):
        if self.title is u'':
            self.title = u"{}-{}".format(type(self).__name__, date.today())
        super(Campaign, self).save(*args, **kwargs)

    def sendgrid_check(self):
        if self.sendgrid_id:
            response = sendgrid_api_client.campaigns._(self.sendgrid_id).get()
            response = json.loads(response.body)
            return self.sendgrid_id == response['id']
        return False

    def sendgrid_data(self):
        if self.sendgrid_id:
            response = sendgrid_api_client.campaigns._(self.sendgrid_id).get()
            response = json.loads(response.body)
            return response
        return None

    def sendgrid_upload(self):
        if not self.sendgrid_check():
            campaign_data = {
                'title': self.title,
                'subject': self.subject,
                'sender': self.sender,
                'html_content': self.html_content,
                'plain_content': self.plain_content,
                'list_ids': []
            }
            if self.contact_list:
                campaign_data['list_ids'].append(self.contact_list.sendgrid_id)
            response = sendgrid_api_client.campaigns.post(
                request_body=campaign_data
            )
            response = json.loads(response.body)
            logging.debug(response)
            self.sendgrid_id = response['id']

    def sendgrid_send(self):
        if self.sendgrid_check():
            sendgrid_api_client.campaigns._(self.sendgrid_id).schedules.now.post()

    def sendgrid_delete(self):
        if self.sendgrid_check():
            sendgrid_api_client.campaigns._(self.sendgrid_id).delete()

    @classmethod
    def create_from_sendgrid_id(cls, sendgrid_id):
        response = sendgrid_api_client.campaigns._(sendgrid_id).get()
        response = json.loads(response.body)
        return cls.objects.create(
            template=sendgrid_id,
            title=response['title'],
            subject=response['subject'],
            sender=response['sender_id'],
            html_content=response['html_content'],
            plain_content=response['plain_content']
        )


class TransactionalEmail(models.Model):

    html_content = models.TextField()
    plain_content = models.TextField()
    template_id = models.CharField(max_length=255)
    recipient = models.ForeignKey(Contact)
    category = models.CharField(max_length=255)

    def email_data(self, sandbox=False):
        mail = Mail()

        mail.from_email = Email("no-reply@masaval.cl", "Masaval")

        personalization = Personalization()
        personalization.add_to(Email(self.recipient.email, "recipient.email"))
        mail.add_personalization(personalization)

        mail_settings = MailSettings()
        mail_settings.sandbox_mode = SandBoxMode(sandbox)
        mail.mail_settings = mail_settings

        mail.template_id = self.template_id
        tracking_settings = TrackingSettings()
        tracking_settings.click_tracking = ClickTracking(True, True)
        tracking_settings.open_tracking = OpenTracking(True)
        mail.tracking_settings = tracking_settings

        return mail

    def sendgrid_send(self, sandbox=False):
        try:
            response = sendgrid_api_client.mail.send.post(
                request_body=self.email_data(sandbox).get()
            )
            return True
        except HTTPError as e:
            logging.error(e)
            return False
