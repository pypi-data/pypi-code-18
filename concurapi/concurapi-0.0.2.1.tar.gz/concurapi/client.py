import logging
from requests import post, get, put, delete
from requests.exceptions import RequestException
from .exceptions import ServiceNotAvailable, ServerException, HTTPException

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

try:
    import http.client as http_client
except ImportError:
    # Python 2
    import httplib as http_client
http_client.HTTPConnection.debuglevel = 1


class WithDomainError(object):
    def __init__(self, f):
        self.f = f

    def __call__(self, *args, **kwargs):
        logger.debug("making an http request")
        try:
            response = self.f(*args, **kwargs)
        except RequestException as e:
            raise ServiceNotAvailable(e)
        try:
            response.raise_for_status()
        except Exception as e:
            if response.status_code > 500:
                logger.error("A server error occurred", e)
                raise ServerException(e)
            elif 400 < response.status_code < 500:
                raise HTTPException(e)
            else:
                raise e
        logger.debug("http request done")
        return response

    def __get__(self, instance, owner):
        from functools import partial
        return partial(self.__call__, instance)


class ConcurAPI(object):
    def __init__(self, options=None, **kwargs):
        self.end_point = kwargs.get("endpoint", "https://www.concursolutions.com/")
        self.client_key = kwargs["client_key"]
        self.client_secret = kwargs["client_secret"]
        self.username = kwargs["username"]
        self.password = kwargs["password"]
        self.refresh_token = kwargs.get("refresh_token", None)
        self.token_hash = None
        self.token_hash_requested_at = None
        self.token_expires_at = None
        self.get_token_hash()

    def get_token_hash(self):
        path = "{0}/net2/oauth2/accesstoken.ashx".format(self.end_point)

        @WithDomainError
        def token_http_call():
            result = post(path, headers={"X-ConsumerKey": self.client_key, "Accept": "application/json"},
                            auth=(self.username, self.password))
            return result
        response = token_http_call()
        data = response.json()

        self.token_hash = data.get("Access_Token", {}).get("Token", None)
        self.token_expires_at = data.get("Access_Token", {}).get("Expiration_date", None)
        self.refresh_token = data.get("Access_Token", {}).get("Refresh_Token", None)

    def get_headers(self):
        return {
            "Authorization": ("%s %s" % ("OAuth", self.token_hash)),
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "Concur-platform-sdk-python"
        }

    @WithDomainError
    def get_request(self, action_url):
        response = get("{0}/{1}".format(self.end_point, action_url), headers=self.get_headers())
        return response

    @WithDomainError
    def post_request(self, action_url, data):
        response = post("{0}/{1}".format(self.end_point, action_url), json=data, headers=self.get_headers())
        return response

    @WithDomainError
    def put_request(self, action_url, data):
        response = put("{0}/{1}".format(self.end_point, action_url), json=data, headers=self.get_headers())
        return response

    @WithDomainError
    def delete_request(self, action_url):
        response = delete("{0}/{1}".format(self.end_point, action_url), headers=self.get_headers())
        return response




