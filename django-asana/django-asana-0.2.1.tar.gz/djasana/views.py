import json

from django.views.generic import FormView


class WebhookView(FormView):

    def post(self, request, *args, **kwargs):
        data = json.loads(request.data)

