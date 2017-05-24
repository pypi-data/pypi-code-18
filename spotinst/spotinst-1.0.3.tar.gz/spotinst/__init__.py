import json
import urllib

import requests

from spotinst import elastigroup


class SpotinstClient:
    __accountIdKey = "accountId"
    __base_elastigroup_url = "https://api.spotinst.io/aws/ec2/group"

    def __init__(self, authToken, accountId=None):
        self.authToken = authToken
        self.accountId = accountId

    def create_elastigroup(self, group):
        group = elastigroup.ElastigroupCreationRequest(group)
        excludedgroup = self.exclude_none(json.loads(group.toJSON()))
        body = json.dumps(excludedgroup)
        groupResponse = self.sendPost(body, self.__base_elastigroup_url)
        group = groupResponse["response"]["items"][0]
        return group

    def delete_elastigroup(self, groupId):
        delurl = self.__base_elastigroup_url + "/" + groupId
        response = self.sendDelete(url=delurl)
        return response

    def get_elastigroup(self, groupId):
        geturl = self.__base_elastigroup_url + "/" + groupId
        result = self.sendGet(url=geturl)
        return result["response"]["items"][0]

    def get_elastigroups(self):
        content = self.sendGet(url=self.__base_elastigroup_url)
        return content["response"]["items"]

    def sendGet(self, url):
        queryParams = None
        if self.accountId is not None:
            queryParams = urllib.urlencode(dict({self.__accountIdKey: self.accountId}))

        headers = dict({'Content-Type': 'application/json', 'Authorization': 'Bearer ' + self.authToken})

        print "Sending get request to spotinst API."

        result = requests.get(url, params=queryParams, headers=headers)

        if result.status_code == self.HTTP_STATUS_CODES.SUCCESS:
            data = json.loads(result.content)
            return data
        else:
            print result.status_code
            data = json.loads(result.content)
            return data

    def sendDelete(self, url):
        queryParams = None
        if self.accountId is not None:
            queryParams = urllib.urlencode(dict({self.__accountIdKey: self.accountId}))

        headers = dict({'Content-Type': 'application/json', 'Authorization': 'Bearer ' + self.authToken})

        print "Sending deletion request to spotinst API."

        result = requests.delete(url, params=queryParams, headers=headers)

        if result.status_code == self.HTTP_STATUS_CODES.SUCCESS:
            return True
        else:
            print result.status_code
            data = json.loads(result.content)
            print json.dumps(data["response"])
            return False

    def sendPost(self, body, url):
        queryParams = None
        if self.accountId is not None:
            queryParams = urllib.urlencode(dict({self.__accountIdKey: self.accountId}))

        headers = dict({'Content-Type': 'application/json', 'Authorization': 'Bearer ' + self.authToken})

        print "Sending post request to spotinst API."

        result = requests.post(url, params=queryParams, data=body, headers=headers)

        if result.status_code == self.HTTP_STATUS_CODES.SUCCESS:
            print "Success"
            data = json.loads(result.content)
        else:
            print result.status_code
            data = json.loads(result.content)
            print json.dumps(data["response"])

        return data

    class HTTP_STATUS_CODES:
        SUCCESS = 200
        BAD_REQUEST = 400
        UNAUTHORIZED = 401
        INTERNAL_SERVER_ERROR = 500

    def exclude_none(self, obj):
        # Delete keys with the value ``None`` in a dictionary, recursively.

        if obj.items() is not None:

            for key, value in obj.items():
                if value is None:
                    del obj[key]

                # Handle Objects
                elif isinstance(value, dict):
                    self.exclude_none(obj=value)

                # Handle lists
                elif self.is_sequence(arg=value):
                    for listitem in value:
                        # Handle Lists of objects
                        try:
                            self.exclude_none(obj=listitem)
                        except AttributeError:
                            pass
        return obj  # For convenience

    def is_sequence(self, arg):
        return (not hasattr(arg, "strip") and
                hasattr(arg, "__getitem__") or
                hasattr(arg, "__iter__"))
