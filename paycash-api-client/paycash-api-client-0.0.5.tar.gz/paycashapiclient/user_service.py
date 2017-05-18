class UserService:
    def __init__(self, client):
        self.client = client



    def DeactivateUser(self, data, headers=None, query_params=None, content_type="application/json"):
        """
        It is method for PUT /user/disable
        """
        uri = self.client.base_url + "/user/disable"
        return self.client.put(uri, data, headers, query_params, content_type)
