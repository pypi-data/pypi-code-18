from flask import jsonify
from app import app


class AppError(Exception):
    """
    AppError is very generic so please
    update your Error naming convention
    to match your service
    """

    def __init__(self, error):
        Exception.__init__(self, error)

    def get_message(self):
        return self.message


class ConflictError(AppError):
    def __init__(self, error):
        AppError.__init__(self, error)

    def get_message(self):
        return self.message


class NotFoundError(AppError):
    def __init__(self, error, **kwargs):
        AppError.__init__(self, error)

    def get_message(self):
        return self.message


class BadRequest(AppError):

    def __init__(self, error="Bad Request"):
        AppError.__init__(self, error)

    def get_message(self):
        return self.message


@app.errorhandler(ConflictError)
def handle_conflict_error(error):
    response = {'error': error.get_message()}
    response = jsonify(response)
    response.status_code = 409
    return response


@app.errorhandler(BadRequest)
def handle_bad_request_exists(error):
    response = {'error': error.get_message()}
    response = jsonify(response)
    response.status_code = 400
    return response


@app.errorhandler(NotFoundError)
def handle_not_found(error):
    response = {'error': error.get_message()}
    response = jsonify(response)
    response.status_code = 404
    return response
