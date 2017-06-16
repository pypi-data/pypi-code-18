import json
from django.test import Client, TestCase
from .models import Contact, ContactList, Campaign, Click, Open, Delivered, TransactionalEmail
from datetime import date


# Create your tests here.

import logging


class ContactTests(TestCase):
    def test_sengrid_check(self):
        contact = Contact.objects.create(email="asdasd+789@asdf.cl")
        contact.sendgrid_delete()
        self.assertFalse(contact.sendgrid_check())

        contact.sendgrid_id = u"asd123sd"
        contact.save()
        self.assertFalse(contact.sendgrid_check())

        contact.sendgrid_id = contact.email.encode('base64')
        contact.save()
        contact.sendgrid_upload()
        self.assertTrue(contact.sendgrid_check())

        self.clean_up()

    def test_sendgrid_upload(self):
        contact = Contact.objects.create(email="asdasd@asdf.cl")
        # Contact.objects.get(email="asdasd@asdf.cl")
        contact.sendgrid_upload()

        self.assertTrue(contact.sendgrid_check())

        contact.sendgrid_delete()

    def test_sendgrid_delete(self):
        contact = Contact.objects.create(email="asdasd@asdf.cl")
        contact.sendgrid_upload()

        contact.sendgrid_delete()

        self.assertFalse(contact.sendgrid_check())

        self.clean_up()

    def test_sendgrid_upload_queryset(self):
        count = Contact.objects.all().sendgrid_upload().count()
        self.assertEqual(0, count, "If a don't have Contacts I can't updated them")

        Contact.objects.create(email="asd")

        contacts = Contact.objects.all()

        contacts = contacts.sendgrid_upload()

        self.assertEqual(
            1,
            len([contact for contact in contacts if not contact.sendgrid_check()])
        )

        self.assertEqual(
            0,
            len([contact for contact in contacts if contact.sendgrid_check()])
        )

        Contact.objects.create(email="asaavedra@masaval.cl")
        Contact.objects.create(email="asaavedra+123@masaval.cl")
        Contact.objects.create(email="asdasdasd")

        contacts = Contact.objects.all()

        contacts = contacts.sendgrid_upload()

        self.assertEqual(
            2,
            len([contact for contact in contacts if not contact.sendgrid_check()])
        )

        self.assertEqual(
            2,
            len([contact for contact in contacts if contact.sendgrid_check()])
        )

        # clean

        self.clean_up()

    def test_big_bulk_contact_creation(self):
        for index in range(20):
            Contact.objects.create(email="asdf{}@asdf.asd".format(index))

        contacts = Contact.objects.all()

        contacts = contacts.sendgrid_upload()

        self.assertEqual(20, contacts.exclude(sendgrid_id=None).count())
        for valid in contacts:
            self.assertTrue(
                valid.sendgrid_check(),
                "{} marked as wrong sendgrid id!".format(valid.email)
            )
        self.clean_up()

    @staticmethod
    def clean_up():
        for contact in Contact.objects.all():
            contact.sendgrid_delete()


class ContactListTest(TestCase):
    def setUp(self):
        self.contact_list = ContactList.objects.create()

    def tearDown(self):
        [contact.sendgrid_delete() for contact in self.contact_list.contact_set.all()]
        self.contact_list.sendgrid_delete()

    def test_creation_name(self):
        self.assertEqual(self.contact_list.name, 'ContactList-{}'.format(date.today()))

    def test_sendgrid_check(self):
        self.assertFalse(self.contact_list.sendgrid_check())

    def test_sendgrid_upload(self):
        self.contact_list.sendgrid_upload()
        self.assertTrue(self.contact_list.sendgrid_check())

    def test_sendgrid_contact_upload(self):
        contacts = [
            Contact.objects.create(email="asdf{}@asdf.asd".format(index))
            for index in range(20)
        ]
        self.contact_list.contact_set = contacts
        self.contact_list.sendgrid_upload()
        self.assertTrue(self.contact_list.sendgrid_check())

        self.contact_list.sendgrid_contact_upload()


class CampaignTest(TestCase):
    def setUp(self):
        self.uploaded_campaign = Campaign.objects.create(
            title='test',
            subject='test subject',
            html_content="<html></html>"
        )
        self.contact_list = ContactList.objects.create()
        self.campaign = Campaign.objects.create(
            contact_list=self.contact_list)

    def tearDown(self):
        self.uploaded_campaign.sendgrid_delete()
        if self.uploaded_campaign.contact_list:
            self.uploaded_campaign.contact_list.sendgrid_delete()
            for contact in self.uploaded_campaign.contact_list.contact_set.all():
                contact.sendgrid_delete()

        if self.campaign.contact_list:
            for contact in self.campaign.contact_list.contact_set.all():
                contact.sendgrid_delete()
            self.campaign.sendgrid_delete()
            self.campaign.contact_list.sendgrid_delete()

    def test_title(self):
        campaign = Campaign.objects.create()
        self.assertEqual(campaign.title, "Campaign-{}".format(date.today()))

    def test_sendgrid_check(self):
        self.uploaded_campaign.sendgrid_upload()
        self.assertFalse(self.campaign.sendgrid_check())
        self.assertTrue(self.uploaded_campaign.sendgrid_check())

    def test_create_from_sendgrid_id(self):
        self.uploaded_campaign.sendgrid_upload()
        sendgrid_id = self.uploaded_campaign.sendgrid_id
        campaign = Campaign.create_from_sendgrid_id(sendgrid_id)
        self.assertEqual(campaign.title, 'test')
        self.assertEqual(campaign.subject, 'test subject')

    def test_sendgrid_data(self):
        self.uploaded_campaign.sendgrid_upload()
        data = self.uploaded_campaign.sendgrid_data()
        logging.debug(data)
        self.assertEqual(len(data['list_ids']), 0)

    def test_sendgrid_upload(self):
        campaign = self.uploaded_campaign
        campaign.contact_list = self.contact_list
        contacts = [
            Contact.objects.create(email="asdf{}@asdf.asd".format(index))
            for index in range(20)
        ]
        campaign.contact_list.contact_set = contacts
        campaign.contact_list.sendgrid_contact_upload()
        campaign.contact_list.sendgrid_upload()
        campaign.sendgrid_upload()
        self.assertTrue(campaign.sendgrid_id is not None)


class EventTest(TestCase):
    def setUp(self):
        self.email = 'asdasd+789@asdf.cl'
        self.data = {
            'email': self.email,
            'timestamp': '145000',
            'sg_message_id': '1231ss',
            'category': 'asdasd',
            'url': 'http://asdasddasd/',
            'ip': '192.168.1.1',
            'useragent': 'EvilCorp',
            'smtp-id': 'asd123'
        }

        self.contact = Contact.objects.create(email=self.email)

    def test_click_factory(self):
        click = Click.factory(self.data)

        self.assertEqual(click.email, self.email)
        self.assertEqual(click.contact, self.contact)
        self.assertEqual(click.category, self.data['category'])

    def test_open_factory(self):
        open_event = Open.factory(self.data)

        self.assertEqual(open_event.email, self.email)
        self.assertEqual(open_event.contact, self.contact)
        self.assertEqual(open_event.ip, self.data['ip'])
        self.assertEqual(open_event.useragent, self.data['useragent'])

    def test_delivered_factory(self):
        delivered = Delivered.factory(self.data)

        self.assertEqual(delivered.email, self.email)
        self.assertEqual(delivered.contact, self.contact)
        self.assertEqual(delivered.smtp_id, self.data['smtp-id'])


class TransactionalEmailTest(TestCase):
    def test_sendgrid_send(self):
        contact = Contact.objects.create(email="asdf@asdf.asd")
        email = TransactionalEmail.objects.create(
            template_id="13b8f94f-bcae-4ec6-b752-70d6cb59f932")
        email.recipients.add(contact)
        self.assertTrue(email.sendgrid_send(sandbox=True))


class ViewTest(TestCase):
    def setUp(self):
        self.email = 'asdasd+789@asdf.cl'
        self.contact = Contact.objects.create(email=self.email)
        self.data = [{
            'event': 'click',
            'email': self.email,
            'timestamp': '145000',
            'sg_message_id': '1231ss',
            'category': 'asdasd',
            'url': 'http://asdasddasd/',
            'ip': '192.168.1.1',
            'useragent': 'EvilCorp',
            'smtp-id': 'asd123'
        }, {
            'event': 'open',
            'email': self.email,
            'timestamp': '145000',
            'sg_message_id': '1231ss',
            'category': 'asdasd',
            'url': 'http://asdasddasd/',
            'ip': '192.168.1.1',
            'useragent': 'EvilCorp',
            'smtp-id': 'asd123'
        }, {
            'event': 'delivered',
            'email': self.email,
            'timestamp': '145000',
            'sg_message_id': '1231ss',
            'category': 'asdasd',
            'url': 'http://asdasddasd/',
            'ip': '192.168.1.1',
            'useragent': 'EvilCorp',
            'smtp-id': 'asd123'
        }, {
            'event': 'NonExistan',
            'email': self.email,
            'timestamp': '145000',
            'sg_message_id': '1231ss',
            'category': 'asdasd',
            'url': 'http://asdasddasd/',
            'ip': '192.168.1.1',
            'useragent': 'EvilCorp',
            'smtp-id': 'asd123'
        }, {
            'event': 'click',
            'email': 'asdasd+123123@asdf.cl',
            'timestamp': '145000',
            'sg_message_id': '1231ss',
            'category': 'asdasd',
            'url': 'http://asdasddasd/',
            'ip': '192.168.1.1',
            'useragent': 'EvilCorp',
            'smtp-id': 'asd123'
        }]

    def test_sendgrid_event(self):
        c = Client()
        self.data[0]['event'] = 'click'
        response = c.post(
            '/sendgrid/events/',
            data=json.dumps(self.data),
            content_type="application/json")
        self.assertEqual(response.status_code, 201)
