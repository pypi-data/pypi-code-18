ERROR_CODE_EXCEPTION_MAPPING = {
    400: "Bad Request",
    401: "Unauthorized",
    402: "Payment Required",
    403: "Forbidden",
    404: "Not Found",
    405: "Method Not Allowed",
    406: "Not Acceptable",
    407: "Proxy Authentication Required",
    408: "Request Timeout",
    409: "Conflict",
    429: "Too Many Requests",
    500: "Internal Server Error"
}

def get_exception_for_error_code(error_code):
    error_msg = ERROR_CODE_EXCEPTION_MAPPING.get(error_code, "Unknown Error")
    return "Request returned: Error %s => %s" % (error_code, error_msg)
