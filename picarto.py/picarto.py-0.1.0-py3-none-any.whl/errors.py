class PicartoException(Exception):
    """Base exception class for picarto.py
    Ideally speaking, this could be caught to handle any exceptions thrown from this library.
    """
    pass


class HTTPException(PicartoException):
    """Exception that's thrown when an HTTP request operation fails.
    .. attribute:: response
        The response of the failed HTTP request. This is an
        instance of `aiohttp.ClientResponse`__.
        __ http://aiohttp.readthedocs.org/en/stable/client_reference.html#aiohttp.ClientResponse
    .. attribute:: text
        The text of the error. Could be an empty string.
    """

    def __init__(self, response, message):
        self.response = response
        if type(message) is dict:
            self.text = message.get('message', '')
            self.code = message.get('code', 0)
        else:
            self.text = message

        fmt = '{0.reason} (status code: {0.status})'
        if len(self.text):
            fmt = fmt + ': {1}'

        super().__init__(fmt.format(self.response, self.text))


class Forbidden(HTTPException):
    """Exception that's thrown for when status code 403 occurs.
    Subclass of :exc:`HTTPException`
    """
    pass


class NotFound(HTTPException):
    """Exception that's thrown for when status code 404 occurs.
    Subclass of :exc:`HTTPException`
    """
    pass
