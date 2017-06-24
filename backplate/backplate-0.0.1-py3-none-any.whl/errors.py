
import logging

from flask import jsonify

log = logging.getLogger(__name__)

class APIError(Exception):
    def __init__(self, code, status=None, description=None, data=None):
        self.code = code
        self.status = status
        self.description = description
        self.data = data

    def format(self):
        code = self.code
        status = self.status
        description = self.description
        data = self.data

        error_object = {
            'code': code,
            'status': status,
            'description': description,
        }

        if data:
            error_object['data'] = data

        return error_object

generics = {
    400: 'Bad Request',
    401: 'Unauthorized',
    403: 'Forbidden',
    404: 'Not Found',
    405: 'Method Not Allowed',
    410: 'Gone',
    500: 'Internal Server Error',
    503: 'Service Unavailable'
}

def errordef(code, status, description):
    return {
        'code': code,
        'status': status,
        'description': description
    }

def create_error_handler(errors={}, json_formatter=None):
    def handle_error(e):
        # get exception status code, default 500 for unknown/generic
        status = getattr(e, 'code', 500)

        # if the exception isn't ours
        if type(e) is not APIError:
            code = None
            status = status
            message = None

            # format error content from generics
            generic = generics[status]
            if generic:
                code = generic.replace(' ', '_').upper()
                message = str(e)
            else:
                code = 'GENERAL_ERROR'
                message = str(e)

            # update the error object
            e = APIError(code, status, message)

        error = errors.get(e.code)
        if error:
            e.status = e.status or error['status']
            e.description = e.description or error['description']

        # log exception if 500 server error
        # remove description for consumer facing data
        status = e.status
        if status >= 500:
            log.exception(e)
            e.description = None

        # json formatter for data envelopes
        data = e.format()
        if callable(json_formatter):
            data = json_formatter(data, status)

        resp = jsonify(data)
        return resp, status
    return handle_error
