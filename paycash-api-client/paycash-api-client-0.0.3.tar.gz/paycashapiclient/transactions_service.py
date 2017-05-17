class TransactionsService:
    def __init__(self, client):
        self.client = client



    def GetTransaction(self, transactionId, headers=None, query_params=None, content_type="application/json"):
        """
        It is method for GET /transactions/{transactionId}
        """
        uri = self.client.base_url + "/transactions/"+transactionId
        return self.client.get(uri, headers, query_params, content_type)


    def ListTransactions(self, headers=None, query_params=None, content_type="application/json"):
        """
        It is method for GET /transactions
        """
        uri = self.client.base_url + "/transactions"
        return self.client.get(uri, headers, query_params, content_type)


    def CreateTransaction(self, data, headers=None, query_params=None, content_type="application/json"):
        """
        It is method for POST /transactions
        """
        uri = self.client.base_url + "/transactions"
        return self.client.post(uri, data, headers, query_params, content_type)
