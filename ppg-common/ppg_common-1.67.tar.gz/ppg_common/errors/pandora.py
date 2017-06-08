from tornado.web import HTTPError


class PandoraHTTPError(HTTPError):
    def __init__(self, code_type):
        # Call the base class constructor with the parameters it needs
        """
        :param code_type is from BlossomHTTPErrors
        """
        super(PandoraHTTPError, self).__init__(code_type[1], code_type[2])
        self.custom_code = code_type[0]


class PandoraHTTPErrors:
    NOT_FOUND = (404, 404, "Entry not found")
    UNAUTHORIZED = (401, 401, "Unauthorized access")
    FORBIDDEN = (403, 403, "Forbidden access")
    BAD_REQUEST = (400, 400, "Bad request")
    CONFLICT = (409, 409, "Conflict caused by duplicates")
    error_map = {
        404: NOT_FOUND,
        401: UNAUTHORIZED,
        403: FORBIDDEN,
        400: BAD_REQUEST,
        409: CONFLICT
    }
