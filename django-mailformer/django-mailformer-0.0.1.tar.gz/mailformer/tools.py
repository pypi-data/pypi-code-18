"Various supporting tools"

from collections import OrderedDict
from urllib.parse import urlencode

from django.core.urlresolvers import reverse
from django.template import Context, Template
from django.template.loader import TemplateDoesNotExist, select_template

from .constants import STATUS_, TEMPLATES, URL_NAME
from .models import Message, Recipient, Sender


def get_email_form_url(email_address, **kwargs):
    recipient = Recipient.objects.get_or_create(email=email_address)[0]
    url = reverse(URL_NAME['form'])
    kwargs['identifier'] = recipient.identifier
    return url + '?' + urlencode(kwargs)


def get_smtp_email_template():
    fallback = (
        "{% autoescape off %}"
        "{% for label, value in contact.items %}{{ label }}: {{ value }}\n"
        "{% endfor %}\n"
        "{% for label, value in other.items %}{{ label }}: {{ value }}\n"
        "{% endfor %}\n"
        "Message:\n"
        "{{ message }}\n"
        "{% endautoescape %}"
    )
    try:
        template = select_template(TEMPLATES['email'])
    except TemplateDoesNotExist:
        template = Template(fallback)

    return template


def create_message(form):
    sender_kwargs = {
        'name': form.data['name'],
        'phone': form.data['phone_number'],
        'email': form.data['email_address']
    }
    sender = Sender.objects.get_or_create(**sender_kwargs)[0]
    recipient = Recipient.objects.get(identifier=form.data['identifier'])

    template = get_smtp_email_template()
    template_context = Context()

    contact = OrderedDict()
    contact['Name'] = form.data['name']
    contact['Phone'] = form.data['phone_number']
    contact['E-mail'] = form.data['email_address']

    other = {}
    exclude = [
        'name',
        'phone_number',
        'email_address',
        'message',
        'subject',
        'csrfmiddlewaretoken',
    ]
    for key, value in form.data.items():
        if key not in exclude:
            other[key] = value

    template_context_data = {
        'contact': contact,
        'message': form.data['message'],
        'other': other,
    }
    template_context.update(template_context_data)

    message_body = template.render(template_context)
    message_kwargs = {
        'recipient': recipient,
        'sender': sender,
        'subject': form.data['subject'],
        'status': STATUS_['NEW'],
        'message': message_body,
    }
    message = Message(**message_kwargs)
    message.save()
