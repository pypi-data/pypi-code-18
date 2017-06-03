import requests

from rest_client.lib.exceptions import EndpointError


class response_validation(object):
    """
    This is decorator with response response_validation.
    Checks if current response's status_code is ok. Raises exception if not.
    """
    error_msg = "{status_code} {reason}."

    def __init__(self, func):
        self.func = func

    def __call__(self, request):
        if request.status_code != requests.codes.ok:
            error_msg = self.error_msg.format(status_code=request.status_code, reason=request.reason)
            raise EndpointError(error_msg)
        return self.func(request)
