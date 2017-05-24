import arcgis_sdk
import json
import responses

from rest_framework import status


def add_response(method, path, **kwargs):
    kwargs.setdefault('status', status.HTTP_200_OK)

    if 'body' in kwargs:
        kwargs['body'] = json.dumps(kwargs['body'])

    responses.add(
        getattr(responses, method),
        arcgis_sdk.ARCGIS_API_URL + path,
        content_type='application/json',
        **kwargs
    )
