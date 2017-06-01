from django import forms


class WebhookForm(forms.Form):
    json = forms.Textarea()
