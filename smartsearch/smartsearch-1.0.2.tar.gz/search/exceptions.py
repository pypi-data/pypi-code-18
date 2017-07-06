class APIKeyRequiredError(BaseException):
    pass


class ClientStringUnacceptableError(BaseException):
    pass


class ClientListUnacceptableError(BaseException):
    pass


class ConfItemNotFound(BaseException):
    pass


class AllClientsFailedError(BaseException):
    pass


class InvalidKeyTypeError(BaseException):
    pass