from api.request import Request
class DriveService(Request):

    jwt = None

    def __int__(self, url_base_api):
        super(DriveService, self).__int__(url_base_api=url_base_api)

    def upload_files(self, ref_cod, app_mod_cod):
        response = self.post("/v1/{0}/modulo/{1}/".format(ref_cod, app_mod_cod))

        status = response.get_status_code()

        if status == 200:
            return True
        else:
            return {
                "status": status,
                "response": response.get_content()
            }
