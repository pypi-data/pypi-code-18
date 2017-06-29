#!/usr/bin/python
# coding: utf8

__version__ = '0.1'


import datetime
import traceback
from pythonjsonlogger import jsonlogger


class GCEFormatter(jsonlogger.JsonFormatter):
    def __init__(self, service_name, service_version, *args, **kwargs):
        """Overwrite the init function of python-json-logger and
        and add the attributes service and version which are needed
        for google error reporting.
        """
        self.service_name = service_name
        self.service_version = service_version
        self.user_getter = None
        self.flask_request = None
        self.flask_request_user_attribute = "user_id"
        super(GCEFormatter, self).__init__(*args, **kwargs)

    def set_user_getter(self, func):
        """Provide a function which will be used to get the current user
        for the log record. This could for example be context variable.
        """
        self.user_getter = func

    def use_flask_request(self, flask_request):
        """Provide a flask request which will be used to determine the current
        request for the log entry.
        """
        self.flask_request = flask_request

    def get_response_code(self, record):
        # User provided
        if "reponse_code" in record.__dict__:
            return record.__dict__["reponse_code"]
        if "responseStatusCode" in record.__dict__:
            return record.__dict__["responseStatusCode"]
        return None

    def get_request(self, record):
        # User provided response code
        request_dict = {"responseStatusCode": self.get_response_code(record)}
        # Flask request context
        if self.flask_request is not None:
            if self.flask_request:
                request_dict["method"] = self.flask_request.method
                request_dict["url"] = self.flask_request.url
                request_dict["userAgent"] = self.flask_request.user_agent.string
                request_dict["referrer"] = self.flask_request.referrer
                request_dict["remoteIp"] = self.flask_request.remote_addr
                return request_dict
        # User provided
        if "method" in record.__dict__:
            request_dict["method"] = record.__dict__["method"]
        if "url" in record.__dict__:
            request_dict["url"] = record.__dict__["url"]
        if "userAgent" in record.__dict__:
            request_dict["userAgent"] = record.__dict__["userAgent"]
        if "referrer" in record.__dict__:
            request_dict["referrer"] = record.__dict__["referrer"]
        if "remoteIp" in record.__dict__:
            request_dict["remoteIp"] = record.__dict__["remoteIp"]
        return request_dict

    def get_user(self, record):
        # User provided
        if "user" in record.__dict__:
            return record.__dict__["user"]
        # User callback
        if self.user_getter is not None:
            return self.user_getter()
        # Flask request variable
        if self.flask_request is not None:
            if self.flask_request:
                return getattr(self.flask_request, self.flask_request_user_attribute, None)
        return None

    def get_location(self, record):
        # Error trace
        if record.exc_info:
            t = traceback.extract_tb(record.exc_info[2])
            if len(t) > 0:
                return {'filePath': t[0][0],
                        'lineNumber': t[0][1],
                        'functionName': t[0][2],
                        'text': t[0][3]}
        # Log trace
        return {'filePath': record.pathname,
                'lineNumber': record.lineno,
                'functionName': record.funcName}

    def get_message(self, record):
        return record.message

    def add_fields(self, log_record, record, message_dict):
        """Process the record and add all neccesary attributes for
        google cloud logging and error reporting.
        """
        #print record.__dict__
        log_record["timestamp"] = datetime.datetime.utcfromtimestamp(
            record.created).isoformat() + 'Z'
        log_record["severity"] = record.levelname.upper()
        log_record["serviceContext"] = {"service": self.service_name,
                                        "version": self.service_version}

        # Error context
        context = {}
        context["httpRequest"] = self.get_request(record)
        context["user"] = self.get_user(record)
        context["reportLocation"] = self.get_location(record)
        log_record["context"] = context

        # call to parent
        return super(GCEFormatter, self).add_fields(log_record, record, message_dict)

    def process_log_record(self, log_record):
        """Minor adjustments for the log output.
        """
        # Trace exceptions in message
        if "exc_info" in log_record and "message" in log_record:
            log_record["error_message"] = log_record.pop("message")
            log_record["message"] = log_record.pop("exc_info")
        return log_record
