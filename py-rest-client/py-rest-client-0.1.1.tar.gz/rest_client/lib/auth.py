from requests.auth import HTTPBasicAuth as _HTTPBasicAuth
from requests.auth import HTTPDigestAuth as _HTTPDigestAuth
from requests_oauthlib import OAuth1 as _OAuth1


class HTTPBasicAuth(_HTTPBasicAuth):
    """
    Patched HTTPBasicAuth class from requests.auth.
    
    How to use it:
        auth = HTTPBasicAuth('user', 'pass')) 
    """
    pass


class HTTPDigestAuth(_HTTPDigestAuth):
    """
    Patched HTTPDigestAuth class from requests.auth.
    
    How to use it:
        auth = HTTPDigestAuth('user', 'pass')) 
    """
    pass


class OAuth1(_OAuth1):
    """
    Patched OAuth1 class from requests.auth.
    
    How to use it:
        auth = OAuth1('YOUR_APP_KEY', 'YOUR_APP_SECRET', 'USER_OAUTH_TOKEN', 'USER_OAUTH_TOKEN_SECRET')
    """
    pass

