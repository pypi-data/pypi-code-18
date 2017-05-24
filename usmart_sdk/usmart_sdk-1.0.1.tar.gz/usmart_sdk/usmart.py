"""
USMRT SDK
"""

import requests


class USMART:
    auth = None

    def __init__(self, auth=None):
        if auth is not None:
            if "keyId" not in auth:
                raise Exception("Auth requires keyId")
            if "keySecret" not in auth:
                raise Exception("Auth requires keySecret")

        self.auth = auth

    def request(self, organisation, resource, revision=None, query=None):
        url = self.buildURL(organisation, resource, revision)
        queryString = self.buildQuery(query)

        url += "?" + queryString
        
        headers = None
        if self.auth:
            headers = {
                "api-key-id": self.auth.keyId,
                "api-key-secret": self.auth.keySecret
            }
        return requests.get(
            url,
            headers=headers
        )

    def buildQuery(self, query=None):
        limit = 10
        offset = 0

        if query and "limit" in query:
            limit = query["limit"]
        if query and "offset" in query:
            offset = query["offset"]

        queries = []
        queries.append("limit(" + str(limit) + "," + str(offset) + ")")
        if query and "equals" in query:
            queries = queries + self.buildEqualQueries(query["equals"])

        return "&".join(queries)

    def buildEqualQueries(self, equals):
        results = []
        for equalQuery in equals:
            results.append(
                "" + equalQuery["key"] + "=" + equalQuery["value"]
            )
        return results

    def buildURL(self, organisation, resource, revision=None):
        revisionString = revision + "/" if revision else "latest/"
        return "https://api.usmart.io/org/" + organisation + "/" + resource + "/" +\
            revisionString + "urql";
