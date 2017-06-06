from api.request import Request

class LoginService(Request):

    jwt = None

    def __int__(self):
        super(LoginService, self).__int__()

    def login(self):
        response = self.post("/v2/login/")

        status = response.get_status_code()
        data = response.get_decoded()

        if status == 200:
            return data['access_token']
        else:
            return {
                "status": status,
                "response": response.get_content()
            }
