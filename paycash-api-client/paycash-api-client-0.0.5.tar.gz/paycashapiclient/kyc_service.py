class KycService:
    def __init__(self, client):
        self.client = client



    def DownloadDocuments(self, documentId, headers=None, query_params=None, content_type="application/json"):
        """
        It is method for GET /kyc/document/get/{documentId}
        """
        uri = self.client.base_url + "/kyc/document/get/"+documentId
        return self.client.get(uri, headers, query_params, content_type)


    def ListDocuments(self, headers=None, query_params=None, content_type="application/json"):
        """
        It is method for GET /kyc/document/list
        """
        uri = self.client.base_url + "/kyc/document/list"
        return self.client.get(uri, headers, query_params, content_type)


    def AddDocument(self, data, headers=None, query_params=None, content_type="application/json"):
        """
        It is method for POST /kyc/verification
        """
        uri = self.client.base_url + "/kyc/verification"
        return self.client.post(uri, data, headers, query_params, content_type, allow_redirects=False)
