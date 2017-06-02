class SatmetrixAPIError(Exception):
    """Satmetrix Returned Error"""

class SatmetrixAPIErrorNotFound(SatmetrixAPIError):
    """Satmetrix Returned 4xx Error"""

class SatmetrixAPIErrorInternalError(SatmetrixAPIError):
    """Satmetrix Returned 5xx Error"""

