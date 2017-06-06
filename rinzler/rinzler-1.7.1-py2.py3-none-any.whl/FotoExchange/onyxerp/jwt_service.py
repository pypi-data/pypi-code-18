from api.request import Request

class JwtService(Request):

    jwt = None

    def __int__(self):
        super(JwtService, self).__int__()

    def renew(self):
        response = self.get("/v1/renew/")

        status = response.get_status_code()
        data = response.get_decoded()

        if status == 200:
            return data['access_token']
        else:
            return {
                "status": status,
                "response": response.get_content()
            }
