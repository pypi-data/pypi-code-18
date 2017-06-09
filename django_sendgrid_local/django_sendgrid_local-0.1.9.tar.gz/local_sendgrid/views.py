import json
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from .models import Event
from django.http import HttpResponse
import logging
# Create your views here.


@csrf_exempt
def events(request):
    """
    Recives a bash of sendgrid events.

    Args:
        request (Request): an http request of django

    Returns:
        HttpResponse: Usign the corresponding code.
    """
    if request.method == 'POST':
        events = json.loads(request.body.decode('utf-8'))
        logging.debug(events)
        for event_data in events:
            # This is a abstract model that return the corresponding event created.
            try:
                Event.factory(event_data)
            except ObjectDoesNotExist:
                logging.warning("{} does not exist in contacts".format(
                    event_data['email']
                ))

        return HttpResponse(status=201)
    return HttpResponse(status=400)
