# Copyright (C) 2014-2015, Availab.io(R) Ltd. All rights reserved.

import re
import copy
import json
from StringIO import StringIO
from datetime import datetime
from jsonschema import Draft4Validator, ValidationError

import pycurl
from apilisk.utils import substitute_variables_recursively

class PycurlErrorCodesEnum(object):
    """
    Convert number to something human readable
    https://curl.haxx.se/libcurl/c/libcurl-errors.html
    """
    URL_MALFORMAT = 3
    COULDNT_RESOLVE_HOST = 6
    COULDNT_CONNECT = 7
    HTTP_RETURNED_ERROR = 22
    READ_ERROR = 26
    OPERATION_TIMEDOUT = 28
    SSL_CONNECT_ERROR = 35
    TOO_MANY_REDIRECTS = 47
    RANGE_ERROR = 33

class CurlCaller(object):
    """
    Handler which handles single call request step
    """
    def __init__(
        self, data, variables, authentication, debug=False
    ):
        """
        Initializes curl connection and sets all necessary options

        If curr_conn is passed, it will be used, otherwise new one will be
        created.
        """
        self.variables = copy.deepcopy(variables)
        self.debug_mode = debug
        self.debug_data = {}

        data_after_substitution = CurlCaller.assing_variables_to_request(
            data, variables
        )
        data_after_substitution["url"] = CurlCaller._construct_url(
            data_after_substitution["url"],
            data_after_substitution["query_parameters"]
        )
        auth_after_substitution = None
        if authentication:
            auth_after_substitution = CurlCaller.assing_variables_to_request(
                authentication, variables
            )

        self.validation = copy.deepcopy(data_after_substitution["validation"])
        self._response_headers = {}
        self._response_content_buffer = StringIO()

        self.conn = pycurl.Curl()

        # Defaults
        self.conn.setopt(pycurl.FOLLOWLOCATION, True)
        self.conn.setopt(pycurl.FAILONERROR, False)
        self.conn.setopt(pycurl.NOSIGNAL, True)
        self.conn.setopt(pycurl.NOPROGRESS, True)
        self.conn.setopt(pycurl.SSL_VERIFYHOST, False)
        self.conn.setopt(pycurl.SSL_VERIFYPEER, False)

        self.conn.setopt(pycurl.HEADERFUNCTION, self._store_headers)
        self.conn.setopt(pycurl.WRITEFUNCTION, self._response_content_buffer.write)
        self.conn.setopt(pycurl.TIMEOUT, 30)
        self.conn.setopt(pycurl.VERBOSE, False)



        if auth_after_substitution and \
            auth_after_substitution["type"] == "http_basic_auth":
            self.conn.setopt(pycurl.HTTPAUTH, pycurl.HTTPAUTH_ANY)
            self.conn.setopt(pycurl.USERNAME, authentication["data"]["user"])
            self.conn.setopt(
                pycurl.PASSWORD, authentication["data"]["password"]
            )

        self.conn.setopt(pycurl.URL, data_after_substitution["url"])
        if data_after_substitution["method"] == "get":
            self.conn.setopt(pycurl.HTTPGET, True)
        else:
            if data_after_substitution["body_data"] is not None:
                self.conn.setopt(
                    pycurl.POSTFIELDS,
                    data_after_substitution["body_data"]["data"]
                )

            self.conn.setopt(
                pycurl.CUSTOMREQUEST,
                data_after_substitution["method"].upper())

        # Set headers
        header_array = [
            u"{0}: {1}".format(key, value)
            for key, value in data_after_substitution["headers"].iteritems()
        ]
        self.conn.setopt(pycurl.HTTPHEADER, header_array)

        if self.debug_mode:
            self.debug_data["original_data"] = copy.deepcopy(data)
            self.debug_data["data_after_variable_substitution"] = \
                copy.deepcopy(data_after_substitution)
            self.debug_data["user_variables"] = copy.deepcopy(variables["var"])
            self.debug_data["req_variables"] = copy.deepcopy(variables["req"])

    @staticmethod
    def _construct_url(url, query_params):
        if len(query_params.keys()) == 0:
            return url

        query_list = []
        for (key, value) in query_params.iteritems():
            query_list.append(u"{0}={1}".format(key, value))

        question_mark_pos = url.find("?")
        if question_mark_pos == -1:
            return(u"{0}?{1}".format(url, "&".join(query_list)))
        elif question_mark_pos == len(url) - 1 or url[-1] == "&":
            return(u"{0}{1}".format(url, "&".join(query_list)))
        else:
            return(u"{0}&{1}".format(url, "&".join(query_list)))

    def _get_response_data_as_unicode(self):
        """
        Method to convert response data based on charset received in response
        header (content-type key).

        Taken from pyCurl sample

        Returns:
            Decoded response as unicode object
        """
        encoding = None
        if "content-type" in self._response_headers:
            content_type = self._response_headers["content-type"].lower()
            match = re.search("charset=(\S+)", content_type)
            if match:
                encoding = match.group(1)
        if encoding is None:
            # Default encoding for HTML is iso-8859-1.
            # Other content types may have different default encoding,
            # or in case of binary data, may have no encoding at all.
            encoding = "iso-8859-1"

        # Decode using the encoding we figured out.
        return self._response_content_buffer.getvalue().decode(encoding)

    def handle_and_get_report(self, include_data=False):
        """
        Calls the stuff and gets report for the call
        """
        try:
            self.conn.perform()
        except pycurl.error as pex:
            error_code = pex[0]
            message = pex[1]
            if error_code == PycurlErrorCodesEnum.HTTP_RETURNED_ERROR:
                return self._get_report_from_response(
                    self.conn, include_data
                )
            else:
                return self._get_report_from_error(message)
        else:
            return self._get_report_from_response(self.conn, include_data)


    def _get_report_from_response(self, response, include_data=False):
        response_content = self._get_response_data_as_unicode()
        errors = []
        if response.getinfo(response.RESPONSE_CODE) not in self.validation["return_codes"]:
            errors.append(
                {
                    "id": "wrong_status_code",
                    "message": u"Status code of response was {0}, but allowed status codes are {1}".format(
                        response.getinfo(response.RESPONSE_CODE),
                        ",".join([str(x) for x in self.validation["return_codes"]])
                    )
                }
            )

        body = None
        try:
            body = json.loads(response_content)
        except ValueError as e:
            body = response_content
            if self.validation["schema"]:
                errors.append(
                    {
                        "id": "not_json",
                        "message": (
                            "There is json schema set, but response "
                            "content is not a valid json document."
                        )
                    }
                )
        else:
            if self.validation["schema"] and \
                self.validation["schema"]["type"] == "json":

                validator = Draft4Validator(self.validation["schema"]["data"])
                validator.check_schema(self.validation["schema"]["data"])

                errs = []
                try:
                    validator.validate(body)
                except ValidationError:
                    errors.append(
                        {
                            "id": "not_valid",
                            "message": "Response is not valid against provided json schema",
                        }
                    )

        report = {
            "action": "call_request",
            "data": {
                "headers": self._response_headers,
                "body": body if include_data else None,
                "status_code": response.getinfo(
                    response.RESPONSE_CODE
                ),
                "name_lookup_duration_ms": CurlCaller._convert_duration(
                    response.getinfo(response.NAMELOOKUP_TIME)
                ),
                "connect_duration_ms": CurlCaller._convert_duration(
                    response.getinfo(response.CONNECT_TIME)
                ),
                "app_connect_duration_ms": CurlCaller._convert_duration(
                    response.getinfo(response.APPCONNECT_TIME)
                ),
                "pre_transfer_duration_ms": CurlCaller._convert_duration(
                    response.getinfo(response.PRETRANSFER_TIME)
                ),
                "start_transfer_duration_ms": CurlCaller._convert_duration(
                    response.getinfo(response.STARTTRANSFER_TIME)
                ),
                "total_duration_ms": CurlCaller._convert_duration(
                    response.getinfo(response.TOTAL_TIME)
                ),
                "redirect_duration_ms": CurlCaller._convert_duration(
                    response.getinfo(response.REDIRECT_TIME)
                )
            },
            "errors": errors,
            "status": "failed" if len(errors) > 0 else "success"
        }

        try:
            variables = json.loads(body)
        except Exception as e:
            variables = body

        if self.debug_mode:
            self.debug_data["new_variables"] = variables
            report["debug"] = copy.deepcopy(self.debug_data)

        return report, variables

    def _get_report_from_error(self, message):
        report = {
            "action": "call_request",
            "status": "failed",
            "data": None,
            "errors": [
                {
                    "id": "no_response",
                    "message": message,
                    "data": None
                }
            ]
        }
        if self.debug_mode:
            report["debug"] = copy.deepcopy(self.debug_data)

        return report, {}

    @staticmethod
    def _convert_duration(duration):
        """
        Converts pycurl duration from seconds to miliseconds
        Args:
            duration: Float duration in seconds

        Returns:
            Int number
        """
        return int(round(duration * 1000))

    def _store_headers(self, header_line):
        """
        Helper method to parse and store headers from curl

        Args:
            header_line: string with header
        """
        header_line = header_line.decode("utf-8")

        # Skip the first line
        if ":" not in header_line:
            return

        # Break the header line into header name and value.
        name, value = header_line.split(":", 1)
        name = name.strip()
        value = value.strip()

        # Names are case insensitive
        name = name.lower()

        self._response_headers[name] = value

    @staticmethod
    def assing_variables_to_request(config, variables):
        """
        Returns new configuration after variable substitution
        """
        cfg = copy.deepcopy(config)

        objects_with_allowed_vars = [
            "url", "headers", "body_data", "query_parameters"
        ]

        for key in objects_with_allowed_vars:
            if cfg.get(key):
                cfg[key] = substitute_variables_recursively(
                    config[key], variables
                )

        if config["validation"]["schema"]:
            cfg["validation"]["schema"]["data"] = \
                substitute_variables_recursively(
                    config["validation"]["schema"]["data"], variables
                )

        return cfg
