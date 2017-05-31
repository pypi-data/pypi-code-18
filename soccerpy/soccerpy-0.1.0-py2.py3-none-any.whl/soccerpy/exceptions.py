class GeneralException(Exception):
    pass


class BadRequestException(Exception):
    pass


class RestrictedResourceException(Exception):
    pass


class NotFoundException(Exception):
    pass


class TooManyRequestsException(Exception):
    pass
