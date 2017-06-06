from api.request import Request
from config.settings import URL_AUTH_API

class AuthService(Request):

    jwt = None

    def __int__(self, base_uri):
        super(AuthService, self).__int__()
        self.set_base_uri(URL_AUTH_API)

    def auth(self):
        response = self.post("/v1/auth/")

        status = response.get_status_code()
        data = response.get_decoded()

        if status == 200 or status == 401:
            return data['access_token']
        else:
            return {
                "status": status,
                "response": response.get_content()
            }
