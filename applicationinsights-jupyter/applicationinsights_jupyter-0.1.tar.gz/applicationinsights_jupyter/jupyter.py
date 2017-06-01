import requests
import json

from datetime import datetime
from operator import itemgetter

class Jupyter:
    baseurl = 'https://api.applicationinsights.io/beta/apps/%s/query'
    headers = {'x-api-key': '%s', 'Content-Type': 'application/json'}
    data = '{ "query" : "%s" }'
    appId = ""
    apiKey = ""

    def __init__(self, appId, apiKey):
        self.appId = appId
        self.apiKey = apiKey

    def getAIData(self, userQuery):
        # hydrate the templates
        url = self.baseurl % self.appId;
        headers = self.headers
        data = self.data % userQuery
        headers['x-api-key'] = headers['x-api-key'] % self.apiKey

        # make the request and parse response
        response = requests.post(url, headers=headers, data=data)
        jsonObj = json.loads(response.text)
        if response != None and response.text != None and response.status_code == 200:
            rows = jsonObj["Tables"][0]["Rows"]
            cols = jsonObj["Tables"][0]["Columns"]
            if jsonObj["Tables"] != None and jsonObj["Tables"][0] != None and jsonObj["Tables"][0]["Rows"] != None and jsonObj["Tables"][0]["Columns"] != None:
                rows = jsonObj["Tables"][0]["Rows"]
                columns = jsonObj["Tables"][0]["Columns"]
                return {"Rows": rows, "Columns": columns }
        else:
            return None

    def sortAxes(self, rows, itemGetter):
        rows = sorted(rows, key=itemgetterKey)
        xaxis = []
        yaxis = []
        for r in rows:
            xaxis.append(r[0])
            yaxis.append(r[1])

        return {'xaxis': xaxis, 'yaxis': yaxis}





