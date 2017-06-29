import requests


class Oauth2ClientOauth_2_0():
    def __init__(self, api_client, access_token_uri='https://sandbox.paycash.eu/authorization-server/oauth/token'):
        self.api_client = api_client
        self.access_token_uri = access_token_uri

    def get_access_token(self, client_id, client_secret, scopes=None, audiences=None, grant_type='client_credentials',
                         code=None, redirect_uri=None):
        if scopes is None:
            scopes = []
        if audiences is None:
            audiences = []
        params = {
            'grant_type': grant_type,
            'client_id': client_id,
            'client_secret': client_secret
        }
        if grant_type == 'authorization_code':
            params['code'] = code
        if len(scopes) > 0:
            params['scope'] = ",".join(scopes)
        if len(audiences) > 0:
            params['aud'] = ",".join(audiences)
        if redirect_uri:
            params['redirect_uri'] = redirect_uri
        data = requests.post(self.access_token_uri, params=params, verify=False)
        if data.status_code != 200:
            raise RuntimeError('Failed to login, %s %s' % (data.status_code, data.text))
        json_data = data.json()
        token = json_data['access_token']
        self.api_client.set_auth_header('Bearer %s' % token)
        return json_data
