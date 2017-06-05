"""
This module makes it easy to connect to your application insights(https://azure.microsoft.com/en-us/services/application-insights/)
data, and makes it easier through helper functions, to convert it to jupyter charts format.
"""
import requests
import json
import copy

from datetime import datetime
from operator import itemgetter

class Jupyter:
    """ Jupyter class gets Application Insights data, and converts it making it easier for Jupyter charts to consume.

    Attributes:
        None
    """

    baseurl = 'https://api.applicationinsights.io/beta/apps/%s/query'
    headers = {'x-api-key': "%s", 'Content-Type': 'application/json'}
    data = '{ "query" : "%s" }'
    appId = ""
    apiKey = ""

    def __init__(self, appId, apiKey):
        """
        Creates a Application Insights Jupyter object. Takes in Application Insights appId and apiKey
        Args:
            appId (str): AppID (refer https://dev.applicationinsights.io/documentation/overview)
            apiKey (str): ApiKey refer https://dev.applicationinsights.io/documentation/overview)
        """
        self.appId = appId
        self.apiKey = apiKey

    def getAIData(self, userQuery):
        """Gets Application Insights data for a particular app. The function assumes that the output of the query will be simple metrics/timestamp etc

            Args:
                userQuery: The query to execute on the REST api (refer https://docs.microsoft.com/en-us/azure/application-insights/app-insights-analytics)

            Returns:
                If successful, returns a Dictionary with keys as "Rows" and "Columns". Returns None otherwise.
        """

        # hydrate the templates - make local copies first, because jupyter data persists
        baseurl = self.baseurl
        data = copy.copy(self.data)
        headers = copy.copy(self.headers)
        appId = self.appId
        apiKey = self.apiKey

        data = data % userQuery
        url = self.baseurl % self.appId;
        headers['x-api-key'] = headers['x-api-key'] % apiKey

        # make the request and parse response
        response = requests.post(url, headers=headers, data=data)
        jsonObj = json.loads(response.text)
        if response != None and response.text != None and response.status_code == 200:
            rows = jsonObj["Tables"][0]["Rows"]
            cols = jsonObj["Tables"][0]["Columns"]
            if (jsonObj["Tables"] != None and
                    jsonObj["Tables"][0] != None and
                    jsonObj["Tables"][0]["Rows"] != None and
                    jsonObj["Tables"][0]["Columns"] != None):
                rows = jsonObj["Tables"][0]["Rows"]
                columns = jsonObj["Tables"][0]["Columns"]
                return {"Rows": rows, "Columns": columns }
        else:
            return None

    def sortAxes(self, rows, itemGetter, x_index, y_index):
        """Sorts the result data, and returns the x axis and y axis data

            Args:
                rows: The "Rows" result of the query from getAIData()
                itemGetter: the itemgetter operator to specify which field to sort against
                x_index: specify which field of the array will be x axis
                y_index: specify which field of the array will be y axis

            Returns:
                If successful, returns a Dictionary with keys as "xaxis" and "yaxis". Returns None otherwise.
        """

        rows = sorted(rows, key=itemgetter)
        xaxis = []
        yaxis = []
        for r in rows:
            xaxis.append(r[x_index])
            yaxis.append(r[y_index])

        return {'xaxis': xaxis, 'yaxis': yaxis}



