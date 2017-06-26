from django import forms

from .models import Recipient
from .tools import create_message


class EmailForm(forms.Form):
    identifier = forms.CharField(max_length=64, widget=forms.widgets.HiddenInput())
    name = forms.CharField(max_length=64)
    email_address = forms.EmailField()
    phone_number = forms.CharField(max_length=32, required=False)
    subject = forms.CharField(max_length=998)
    message = forms.CharField(widget=forms.Textarea)

    def clean_identifier(self):
        data = self.cleaned_data['identifier']
        try:
            Recipient.objects.get(identifier=data)
        except Recipient.DoesNotExist:
            self.add_error('identifier', 'Invalid value.')

        return data

    def save(self):
        create_message(self)
