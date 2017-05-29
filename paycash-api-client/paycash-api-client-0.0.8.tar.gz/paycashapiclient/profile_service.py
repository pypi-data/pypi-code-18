class ProfileService:
    def __init__(self, client):
        self.client = client



    def DeleteAddress(self, addressId, headers=None, query_params=None, content_type="application/json"):
        """
        It is method for DELETE /profile/address/{addressId}
        """
        uri = self.client.base_url + "/profile/address/"+addressId
        return self.client.delete(uri, headers, query_params, content_type)


    def GetAddress(self, addressId, headers=None, query_params=None, content_type="application/json"):
        """
        It is method for GET /profile/address/{addressId}
        """
        uri = self.client.base_url + "/profile/address/"+addressId
        return self.client.get(uri, headers, query_params, content_type)


    def UpdateAddress(self, data, addressId, headers=None, query_params=None, content_type="application/json"):
        """
        It is method for PUT /profile/address/{addressId}
        """
        uri = self.client.base_url + "/profile/address/"+addressId
        return self.client.put(uri, data, headers, query_params, content_type)


    def ListAddresses(self, headers=None, query_params=None, content_type="application/json"):
        """
        It is method for GET /profile/address
        """
        uri = self.client.base_url + "/profile/address"
        return self.client.get(uri, headers, query_params, content_type)


    def AddAddress(self, data, headers=None, query_params=None, content_type="application/json"):
        """
        It is method for POST /profile/address
        """
        uri = self.client.base_url + "/profile/address"
        return self.client.post(uri, data, headers, query_params, content_type)


    def DeleteEmail(self, emailId, headers=None, query_params=None, content_type="application/json"):
        """
        It is method for DELETE /profile/emails/{emailId}
        """
        uri = self.client.base_url + "/profile/emails/"+emailId
        return self.client.delete(uri, headers, query_params, content_type)


    def GetEmail(self, emailId, headers=None, query_params=None, content_type="application/json"):
        """
        It is method for GET /profile/emails/{emailId}
        """
        uri = self.client.base_url + "/profile/emails/"+emailId
        return self.client.get(uri, headers, query_params, content_type)


    def UpdateEmail(self, data, emailId, headers=None, query_params=None, content_type="application/json"):
        """
        It is method for PUT /profile/emails/{emailId}
        """
        uri = self.client.base_url + "/profile/emails/"+emailId
        return self.client.put(uri, data, headers, query_params, content_type)


    def ListEmails(self, headers=None, query_params=None, content_type="application/json"):
        """
        It is method for GET /profile/emails
        """
        uri = self.client.base_url + "/profile/emails"
        return self.client.get(uri, headers, query_params, content_type)


    def AddEmail(self, data, headers=None, query_params=None, content_type="application/json"):
        """
        It is method for POST /profile/emails
        """
        uri = self.client.base_url + "/profile/emails"
        return self.client.post(uri, data, headers, query_params, content_type)


    def GetMe(self, headers=None, query_params=None, content_type="application/json"):
        """
        It is method for GET /profile/me
        """
        uri = self.client.base_url + "/profile/me"
        return self.client.get(uri, headers, query_params, content_type)


    def UpdateMe(self, data, headers=None, query_params=None, content_type="application/json"):
        """
        It is method for PUT /profile/me
        """
        uri = self.client.base_url + "/profile/me"
        return self.client.put(uri, data, headers, query_params, content_type)


    def DeletePhone(self, phoneId, headers=None, query_params=None, content_type="application/json"):
        """
        It is method for DELETE /profile/phones/{phoneId}
        """
        uri = self.client.base_url + "/profile/phones/"+phoneId
        return self.client.delete(uri, headers, query_params, content_type)


    def GetPhone(self, phoneId, headers=None, query_params=None, content_type="application/json"):
        """
        It is method for GET /profile/phones/{phoneId}
        """
        uri = self.client.base_url + "/profile/phones/"+phoneId
        return self.client.get(uri, headers, query_params, content_type)


    def UpdatePhone(self, data, phoneId, headers=None, query_params=None, content_type="application/json"):
        """
        It is method for PUT /profile/phones/{phoneId}
        """
        uri = self.client.base_url + "/profile/phones/"+phoneId
        return self.client.put(uri, data, headers, query_params, content_type)


    def ListPhones(self, headers=None, query_params=None, content_type="application/json"):
        """
        It is method for GET /profile/phones
        """
        uri = self.client.base_url + "/profile/phones"
        return self.client.get(uri, headers, query_params, content_type)


    def AddPhone(self, data, headers=None, query_params=None, content_type="application/json"):
        """
        It is method for POST /profile/phones
        """
        uri = self.client.base_url + "/profile/phones"
        return self.client.post(uri, data, headers, query_params, content_type)


    def VerifyProfile(self, data, headers=None, query_params=None, content_type="application/json"):
        """
        It is method for POST /profile/verification
        """
        uri = self.client.base_url + "/profile/verification"
        return self.client.post(uri, data, headers, query_params, content_type)


    def GetProfile(self, headers=None, query_params=None, content_type="application/json"):
        """
        It is method for GET /profile
        """
        uri = self.client.base_url + "/profile"
        return self.client.get(uri, headers, query_params, content_type)


    def CreateProfile(self, data, headers=None, query_params=None, content_type="application/json"):
        """
        It is method for PUT /profile
        """
        uri = self.client.base_url + "/profile"
        return self.client.put(uri, data, headers, query_params, content_type)
