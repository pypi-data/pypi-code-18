class AssetsService:
    def __init__(self, client):
        self.client = client



    def GetAccountBalance(self, accountId, headers=None, query_params=None, content_type="application/json"):
        """
        It is method for GET /assets/accounts/{accountId}/balance
        """
        uri = self.client.base_url + "/assets/accounts/"+accountId+"/balance"
        return self.client.get(uri, headers, query_params, content_type)


    def GetAccount(self, accountId, headers=None, query_params=None, content_type="application/json"):
        """
        It is method for GET /assets/accounts/{accountId}
        """
        uri = self.client.base_url + "/assets/accounts/"+accountId
        return self.client.get(uri, headers, query_params, content_type)


    def ListAccounts(self, headers=None, query_params=None, content_type="application/json"):
        """
        It is method for GET /assets/accounts
        """
        uri = self.client.base_url + "/assets/accounts"
        return self.client.get(uri, headers, query_params, content_type)


    def CreateAccount(self, data, headers=None, query_params=None, content_type="application/json"):
        """
        It is method for POST /assets/accounts
        """
        uri = self.client.base_url + "/assets/accounts"
        return self.client.post(uri, data, headers, query_params, content_type)


    def CreateBank(self, data, headers=None, query_params=None, content_type="application/json"):
        """
        It is method for POST /assets/banks/sepa
        """
        uri = self.client.base_url + "/assets/banks/sepa"
        return self.client.post(uri, data, headers, query_params, content_type)


    def DisableBank(self, bankId, headers=None, query_params=None, content_type="application/json"):
        """
        It is method for DELETE /assets/banks/{bankId}
        """
        uri = self.client.base_url + "/assets/banks/"+bankId
        return self.client.delete(uri, headers, query_params, content_type)


    def GetBank(self, bankId, headers=None, query_params=None, content_type="application/json"):
        """
        It is method for GET /assets/banks/{bankId}
        """
        uri = self.client.base_url + "/assets/banks/"+bankId
        return self.client.get(uri, headers, query_params, content_type)


    def VerifyBank(self, data, bankId, headers=None, query_params=None, content_type="application/json"):
        """
        It is method for PUT /assets/banks/{bankId}
        """
        uri = self.client.base_url + "/assets/banks/"+bankId
        return self.client.put(uri, data, headers, query_params, content_type)


    def ListBanks(self, headers=None, query_params=None, content_type="application/json"):
        """
        It is method for GET /assets/banks
        """
        uri = self.client.base_url + "/assets/banks"
        return self.client.get(uri, headers, query_params, content_type)


    def CreateCreditCard(self, data, headers=None, query_params=None, content_type="application/json"):
        """
        It is method for POST /assets/creditcards/payone
        """
        uri = self.client.base_url + "/assets/creditcards/payone"
        return self.client.post(uri, data, headers, query_params, content_type, allow_redirects=False)


    def GetCreditCard(self, creditCardId, headers=None, query_params=None, content_type="application/json"):
        """
        It is method for GET /assets/creditcards/{creditCardId}
        """
        uri = self.client.base_url + "/assets/creditcards/"+creditCardId
        return self.client.get(uri, headers, query_params, content_type)


    def ListCreditCards(self, headers=None, query_params=None, content_type="application/json"):
        """
        It is method for GET /assets/creditcards
        """
        uri = self.client.base_url + "/assets/creditcards"
        return self.client.get(uri, headers, query_params, content_type)
