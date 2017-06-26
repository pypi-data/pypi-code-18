from django.db import models
from django.utils.timezone import now

from . import constants
from .models_tools import make_hash, random_salt


class Recipient(models.Model):
    identifier = models.CharField(max_length=64, editable=False, unique=True)
    email = models.EmailField()
    salt = models.BinaryField(default=random_salt, editable=False)

    def __str__(self):
        return self.email

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.identifier = make_hash(self.salt, self.email)
        return super().save(force_insert, force_update, using, update_fields)


class Sender(models.Model):
    name = models.CharField(max_length=64)
    email = models.EmailField()
    phone = models.CharField(max_length=32, blank=True)

    def __str__(self):
        return "{} ({} - {})".format(self.name, self.email, self.phone)


class Message(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    recipient = models.ForeignKey(Recipient)
    sender = models.ForeignKey(Sender)
    subject = models.CharField(max_length=998)
    message = models.TextField()

    process_after = models.DateTimeField(auto_now_add=True)
    processor = models.CharField(max_length=32, null=True, editable=False)
    returned = models.TextField(editable=False)

    status = models.PositiveSmallIntegerField(choices=constants.STATUS.items())

    def __str__(self):
        string = "[{}] - {} > {}: {}"
        args = (constants.STATUS[self.status], self.sender, self.recipient, self.subject,)
        return string.format(*args)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.updated_at = now()
        return super().save(force_insert, force_update, using, update_fields)
