"""
Email processor
"""
import json
import os

from django.conf import settings
from django.core.mail import EmailMessage
from django.utils.timezone import now

from .constants import STATUS_
from .models import Message


def handle_status(status, message_ids=None):
    id_string = "{}|{}".format(os.getpid(), now().isoformat())[:32]
    filter_kwargs = {
        'process_after__lte': now(),
        'status': status,
    }
    if message_ids:
        if not isinstance(message_ids, (list, tuple, set)):
            message_ids = [
                message_ids,
            ]

        filter_kwargs['id__in'] = message_ids

    query = Message.objects.filter(**filter_kwargs)
    query.update(processor=id_string, status=STATUS_['PROCESSING'])

    # Making sure we work atmic on the messages
    filter_kwargs['processor'] = id_string
    filter_kwargs['status'] = STATUS_['PROCESSING']
    query = Message.objects.filter(**filter_kwargs)

    for message in query:
        process(message)


def process(message):
    "Actually send the email."
    # Now check if we have a recipient, unlikely this is missing but it is
    # possible if the template tag is used on an email field that is empty.
    # Instead of failing loudly we silently discard.
    if not message.recipient.email or message.recipient.email.strip() == '':
        message.status = STATUS_['INVALID']
        message.save()
        return

    # Time to process, we are keeping a log of the return value of the send
    # function.
    if message.returned:
        message_returned = json.loads(message.returned)
    else:
        message_returned = []

    try:
        mail_kwargs = {
            'subject': message.subject,
            'body': message.message,
            'from_email': settings.DEFAULT_FROM_EMAIL,
            'to': (message.recipient.email,),
            'reply_to': (message.sender.email,),
        }
        mail = EmailMessage(**mail_kwargs)
        message_returned.insert(0, mail.send(fail_silently=False))
        message.status = STATUS_['SENT']
    except Exception as exception_instance:
        message_returned.insert(0, str(exception_instance))
        message.status = STATUS_['ERROR']

    message.returned = json.dumps(message_returned)
    message.save()
