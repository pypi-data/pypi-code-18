
class ApiliskException(Exception):
    """
    Vase class for all apilisk-related exceptions
    """

class ObjectNotFound(ApiliskException):
    """
    Requested object (project, testcase) has not been found
    """
