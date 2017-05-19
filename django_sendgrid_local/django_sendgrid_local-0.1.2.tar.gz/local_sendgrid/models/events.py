# -*- encoding: utf-8 -*-
from django.db import models
from .models import Contact


class Event(models.Model):

    contact = models.ForeignKey(
        Contact,
        null=True,
        on_delete=models.SET_NULL
    )

    email = models.EmailField(
    )

    timestamp = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    sg_message_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    class Meta:
        abstract = True

    def __unicode__(self):
        return u'sg_message_id: {}, email: {}, category: {}.'.format(
            self.sg_message_id, self.email, self.category)

    def save(self, *args, **kwargs):
        if self.contact is None:
            self.contact = Contact.objects.get(email__iexact=self.email)
        super(Event, self).save(*args, **kwargs)

    @classmethod
    def factory(cls, data):
        """This is a factory that returns the instance that is required.

        Args:
            data (dict): A dictionary that includes the event,
                         and the data for creating it

        Returns:
            [Click(), Open(), Delivered()]: a instance of one of this class
        """
        classes = {
            'click': Click,
            'open': Open,
            'delivered': Delivered
        }

        event_class = classes.get(data['event'], None)
        if event_class:
            return event_class.factory(data)
        return None


class Click(Event):

    url = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    category = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    @classmethod
    def factory(cls, data):
        return cls.objects.create(
            email=data['email'],
            timestamp=data['timestamp'],
            sg_message_id=data['sg_message_id'],
            category=data.get('category'),
            url=data['url'],
        )


class Open(Event):
    # requiered fields

    ip = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    useragent = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    @classmethod
    def factory(cls, data):
        return cls.objects.create(
            email=data['email'],
            timestamp=data['timestamp'],
            sg_message_id=data['sg_message_id'],
            ip=data['ip'],
            useragent=data['useragent'],
        )


class Delivered(Event):
    # requiered fields

    smtp_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    @classmethod
    def factory(cls, data):
        return cls.objects.create(
            email=data['email'],
            timestamp=data['timestamp'],
            sg_message_id=data['sg_message_id'],
            smtp_id=data['smtp-id'],
        )
