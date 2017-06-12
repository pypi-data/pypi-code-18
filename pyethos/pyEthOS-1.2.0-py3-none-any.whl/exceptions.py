class EthOSError(Exception):
    pass


class EthOSBadRequestError(EthOSError):
    pass


class EthOSUnauthorizedError(EthOSError):
    pass


class EthOSPaymentRequiredError(EthOSError):
    pass


class EthOSNotFoundError(EthOSError):
    pass


class EthOSConflictError(EthOSError):
    pass


class EthOSForbiddenError(EthOSError):
    pass


class EthOSInternalServiceError(EthOSError):
    pass


ERROR_CODE_EXCEPTION_MAPPING = {
    400: EthOSBadRequestError,
    401: EthOSUnauthorizedError,
    402: EthOSPaymentRequiredError,
    403: EthOSForbiddenError,
    404: EthOSNotFoundError,
    409: EthOSForbiddenError,
    500: EthOSInternalServiceError
}

def get_exception_for_error_code(error_code):
    return ERROR_CODE_EXCEPTION_MAPPING.get(error_code, EthOSError)
