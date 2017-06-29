#############################
#
#
#  Used to customize the user that is returned from cookie based authentication
#  as well as header based authentication
#
#
###############################


import json
from django.conf import settings
from django.contrib.auth.models import User, AnonymousUser
from rest_framework import exceptions, HTTP_HEADER_ENCODING, authentication


from helpers.security_helpers import decrypter

from django_framework.django_helpers.manager_helpers import get_manager
from django_framework.django_helpers.cache_helpers import NormalCache


IS_AUTHENTICATION_SERVER = settings.IS_AUTHENTICATION_SERVER

class TokenAuthentication(authentication.BaseAuthentication):
    """
    Simple token based authentication.

    Clients should authenticate by passing the token key in the "Authorization"
    HTTP header, prepended with the string "Token ".  For example:

        Authorization: Token 401f7ac837da42b97f613d789819ff93537bee6a
    """

    """
    A custom token model may be used, but must have the following properties.
    * key -- The string identifying the token
    * user -- The user to which the token belongs
    """

    def authenticate(self, request):
        print('do i get here', request.META.get('HTTP_AUTHORIZATION'))
        if request.META.get('HTTP_AUTHORIZATION', None):
            response = self.authenticate_via_headers(request = request)
        
        elif request.COOKIES.get('AUTHORIZATIONID', None):
            response = self.authenticate_via_cookies(request = request)
            
        else:
            response = None
            
        if response == None:
            response = self.create_anonymous_user()
            
        return response
    
    def authenticate_via_headers(self, request):
        auth = request.META.get('HTTP_AUTHORIZATION', b'')
        if isinstance(auth, str):
            auth = auth.encode(HTTP_HEADER_ENCODING)  # Work around django test client oddness
        auth = auth.split()  # split by spaces!

        if not auth or auth[0].lower() != b'token':
            response = None
        elif len(auth) != 2:
            raise exceptions.AuthenticationFailed('Invalid token header.')

        else:
            response = self.authenticate_credentials(token=auth[1])
        return response
    
    def authenticate_via_cookies(self, request):
        auth = request.COOKIES.get('AUTHORIZATIONID')
        if isinstance(auth, str):
            auth = auth.encode(HTTP_HEADER_ENCODING)  # Work around django test client oddness

        if not auth:
            response = None
        else:
            response = self.authenticate_credentials(token=auth)
        return response
    
    
    def create_anonymous_user(self):
        
        
        user = AnonymousUser()
        user.profile_id = -1
        user.profile_uuid = 'anonymous_user'
        
        return user, 'anonymous_user'
        
    
    def authenticate_credentials(self, token):
        try:
            user = self.convert_token_to_user(token = token)
            if IS_AUTHENTICATION_SERVER == True:
                self.verify_token(user_id = user.id, token = user.current_token)
                
        except Exception as e:
            raise exceptions.AuthenticationFailed(str(e))

        # otherwise it passses! as we need to go get the user!

        if user is None:
            raise exceptions.AuthenticationFailed('Unable to validate based on token!')
        return (user, token)
    
    def convert_token_to_user(self, token):
        
        print(token)
        cache = self.get_cache(token)
        print('ok')
        info_token=cache.get()
        print('token')
        if info_token == None:
            print('ahha')
            data = decrypter(astr = token, des_key = settings.PRIVATE_TRIPLE_DES_TOKEN_KEY)
            print('2')
            info_token = json.loads(data)
            print('3')
            cache.set(value = info_token, ttl = 300)
            print(4)
        else:
            print('noppie')
            print(info_token)
            
        token = info_token
        user = User()
        user.is_staff = token['user_is_staff']
        user.id = token['user_id']
        user.profile_id = token['profile_id']
        user.profile_uuid = token['profile_uuid']
        user.expire_at = token['expire_at']
        user.current_token = token['current_token']
        return user

    
    def verify_token(self, user_id, token):
        user = get_manager('AuthToken').authenticate(user_id=user_id, token = token)
        if user == None:
            raise exceptions.AuthenticationFailed('Please check token and try again.  Typically expired tokens!')
    
    
    def get_cache(self, key):
        return NormalCache(key = key)