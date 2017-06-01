import json
import urllib

import requests

from spotinst import aws_elastigroup


class SpotinstClient:
    __account_id_key = "accountId"
    __base_elastigroup_url = "https://api.spotinst.io/aws/ec2/group"

    def __init__(self, authToken, accountId=None, printOutput=True):
        self.auth_token = authToken
        self.account_id = accountId
        self.should_print_output = printOutput

    def print_output(self, output):
        if self.should_print_output is True:
            print output

    def create_elastigroup(self, group):

        group = aws_elastigroup.ElastigroupCreationRequest(group)
        excluded_group = self.exclude_missing(json.loads(group.toJSON()))
        body = json.dumps(excluded_group)

        self.print_output(body)
        groupResponse = self.sendPost(body, self.__base_elastigroup_url)

        retVal = groupResponse["response"]["items"][0]

        return retVal

    def update_elastigroup(self, group_update, group_id):

        group = aws_elastigroup.ElastigroupUpdateRequest(group_update)
        excluded_group_update = self.exclude_missing(json.loads(group.toJSON()))
        body = json.dumps(excluded_group_update)

        self.print_output(body)
        groupResponse = self.sendPut(body, self.__base_elastigroup_url + "/" + group_id)

        retVal = groupResponse["response"]["items"][0]

        return retVal

    def delete_elastigroup(self, group_id):
        delurl = self.__base_elastigroup_url + "/" + group_id
        response = self.sendDelete(url=delurl)
        return response

    def get_elastigroup(self, group_id):
        geturl = self.__base_elastigroup_url + "/" + group_id
        result = self.send_get(url=geturl)
        return result["response"]["items"][0]

    def get_elastigroups(self):
        content = self.send_get(url=self.__base_elastigroup_url)
        return content["response"]["items"]

    def send_get(self, url):
        queryParams = None
        if self.account_id is not None:
            queryParams = urllib.urlencode(dict({self.__account_id_key: self.account_id}))

        headers = dict({'Content-Type': 'application/json', 'Authorization': 'Bearer ' + self.auth_token})

        self.print_output("{\"message\" : \"Sending get request to spotinst API.\"}")

        result = requests.get(url, params=queryParams, headers=headers)

        if result.status_code == self.HTTP_STATUS_CODES.SUCCESS:
            self.print_output("{\"statusCode\" : \"" + str(result.status_code) + "\"}")
            data = json.loads(result.content)
            return data
        else:
            self.print_output("{\"statusCode\" : \"" + str(result.status_code) + "\"}")
            data = json.loads(result.content)
            self.print_output(json.dumps(data["response"]))
            raise SpotinstClientException("Error encountered while getting elastigroup", data["response"]["errors"])

    def sendDelete(self, url):
        err = None
        queryParams = None
        if self.account_id is not None:
            queryParams = urllib.urlencode(dict({self.__account_id_key: self.account_id}))

        headers = dict({'Content-Type': 'application/json', 'Authorization': 'Bearer ' + self.auth_token})

        self.print_output("Sending deletion request to spotinst API.")

        result = requests.delete(url, params=queryParams, headers=headers)

        if result.status_code == self.HTTP_STATUS_CODES.SUCCESS:
            return True
        else:
            self.print_output(result.status_code)
            data = json.loads(result.content)
            self.print_output(json.dumps(data["response"]))
            raise SpotinstClientException("Error encountered while getting elastigroup", data["response"]["errors"])

    def sendPost(self, body, url):
        err = None
        queryParams = None
        if self.account_id is not None:
            queryParams = urllib.urlencode(dict({self.__account_id_key: self.account_id}))

        headers = dict({'Content-Type': 'application/json', 'Authorization': 'Bearer ' + self.auth_token})

        self.print_output("Sending post request to spotinst API.")

        result = requests.post(url, params=queryParams, data=body, headers=headers)

        if result.status_code == self.HTTP_STATUS_CODES.SUCCESS:
            self.print_output("Success")
            data = json.loads(result.content)
        else:
            self.print_output(result.status_code)
            data = json.loads(result.content)
            self.print_output(json.dumps(data["response"]))
            raise SpotinstClientException("Error encountered while getting elastigroup", data["response"]["errors"])

        return data

    def sendPut(self, body, url):
        err = None
        query_params = None
        if self.account_id is not None:
            query_params = urllib.urlencode(dict({self.__account_id_key: self.account_id}))

        headers = dict({'Content-Type': 'application/json', 'Authorization': 'Bearer ' + self.auth_token})

        self.print_output("Sending put request to spotinst API.")

        result = requests.put(url, params=query_params, data=body, headers=headers)

        if result.status_code == self.HTTP_STATUS_CODES.SUCCESS:
            self.print_output("Success")
            data = json.loads(result.content)
        else:
            self.print_output(result.status_code)
            data = json.loads(result.content)
            self.print_output(json.dumps(data["response"]))
            raise SpotinstClientException("Error encountered while getting elastigroup", data["response"]["errors"])

        return data

    class HTTP_STATUS_CODES:
        SUCCESS = 200
        BAD_REQUEST = 400
        UNAUTHORIZED = 401
        INTERNAL_SERVER_ERROR = 500

    def exclude_missing(self, obj):
        # Delete keys with the value 'none' in a dictionary, recursively.

        # if obj.items() is not None:
        if obj.items() is not None:
            for key, value in obj.items():

                # Remove none values
                if value == aws_elastigroup.none:
                    del obj[key]

                # Handle Objects
                elif isinstance(value, dict):
                    self.exclude_missing(obj=value)

                # Handle lists
                elif self.is_sequence(arg=value):
                    for listitem in value:
                        # Handle Lists of objects
                        try:
                            self.exclude_missing(obj=listitem)
                        except AttributeError:
                            pass
        return obj  # For convenience

    def is_sequence(self, arg):
        return (not hasattr(arg, "strip") and
                hasattr(arg, "__getitem__") or
                hasattr(arg, "__iter__"))


class SpotinstClientException(Exception):
    def __init__(self, message, errors):
        message = self.generate_error_message_string(errors, message)
        # Call the base class constructor with the parameters it needs
        super(SpotinstClientException, self).__init__(message)

        # custom errors
        self.errors = errors

    def generate_error_message_string(self, errors, message):
        for error in errors:
            error_message = error["message"]
            error_code = error["code"]
            error_string = error_code + " : " + error_message
            message += " | " + error_string
        return message
