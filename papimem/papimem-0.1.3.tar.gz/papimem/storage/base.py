from abc import ABCMeta, abstractmethod


class ReqRes:
    """ Request-Response object """
    def __init__(self, request, response):
        self.request = request
        self.response = response


class StorageBase:
    """ Storage Abstract Base Class """
    __metaclass__ = ABCMeta

    def __init__(self, *args, **kwargs):
        pass

    def generate_key(self, request):
        """
        Generate key from incoming request.
        Your policy for storing requests may be different and take into
        account also some of the request headers. For sake of simplicty
        lets assume that only request method and url (with querystring)
        is enough to differentiate requests.
        """
        return "{} {}".format(request.method, request.url)

    @abstractmethod
    def get(self, key):
        """ Get ReqRes (request-response) object by key """
        pass

    @abstractmethod
    def save(self, key, reqres):
        """ Save ReqRes  (request-response) object in storage """
        pass

    @abstractmethod
    def get_all(self):
        """ Get all stored ReqRes (request-response) objects """
        pass
