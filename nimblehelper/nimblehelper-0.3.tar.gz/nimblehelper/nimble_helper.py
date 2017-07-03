from .exceptions import BadInputException, InvalidAuthentication, InternalServerError
import hashlib
import requests
import json

SIEBEL_GATEWAY_URL = "http://authenticationservice:8000/siebel/siebelrequest/"
SUCCESSFUL = "Operation successful"
INTERNAL_SERVER_ERROR = "An error has occured, please try again later"


# This class was created in order to extract functionality from nimble microservices
class NimbleHelper:
    # Checks Request For HTTP_X_CONSUMER_ID header (indicates kong has authorized the request)
    @staticmethod
    def _check_authorization(request):
        x_consumer_id = request.META.get('HTTP_X_CONSUMER_ID', None)
        if not x_consumer_id:
            raise InvalidAuthentication
        return x_consumer_id

    @classmethod
    def _run_siebel_request(cls, x_consumer_id, data):
        headers = {"X_Consumer_ID": x_consumer_id, "Content-Type": "application/json"}
        try:
            results = requests.post(SIEBEL_GATEWAY_URL, data=data, headers=headers)
        except ConnectionError as exception:
            raise InternalServerError(str(exception))
        return json.loads(results.content.decode("utf-8"))

    # Checks the required fields in a tuple [('name',), ('id',)] will be checked in a "AND" format,
    # if multiple values in a tuple e.g. [('name', 'id',)] these will be treated as 'OR' conditionals
    @staticmethod
    def check_required_input(required_fields, call_values):
        try:
            for fields in required_fields:
                check = False
                for field in fields:
                    if call_values['data'][field]:
                        check = True
                if not check:
                    raise BadInputException
        except KeyError:
            raise BadInputException
        return True

    # These functions get data from a request passed through
    # ==============================================================================================
    # START OF FUNCTIONS
    # ==============================================================================================
    # Takes in a fields argument (list of tuples) in order to map request variables to a dict, pass
    # through required_fields in order to have required fields add the names as tuples to the required_fields list

    # USED FOR GET REQUESTS
    @classmethod
    def check_get_parameters(cls, request, fields, required_fields=None, pk=None):
        call_values = {
            'x_consumer_id': cls._check_authorization(request),
            'data': {}
        }
        for field in fields:
            parameter, value = field
            if pk and value == "pk":
                call_values['data'][parameter] = pk
            else:
                call_values['data'][parameter] = request.GET.get(value, None)
        cls.check_required_input(required_fields, call_values)
        return call_values

    # USED FOR POST REQUESTS
    @classmethod
    def check_post_parameters(cls, request, fields, required_fields):
        call_values = {
            'x_consumer_id': cls._check_authorization(request),
            'data': {}
        }
        for field in fields:
            parameter, value = field
            call_values['data'][parameter] = request.POST.get(value, None)
        cls.check_required_input(required_fields, call_values)
        return call_values
        # ==============================================================================================
        # END OF FUNCTIONS
        # ==============================================================================================


class NimbleErrors:
    @staticmethod
    def _200_success(data=None, message=SUCCESSFUL):  # pragma: no cover
        data = [] if data is None else data
        return {"status": 200, "message": message, "data": data}

    @staticmethod
    def __201_success(data=None, message=SUCCESSFUL):  # pragma: no cover
        data = [] if data is None else data
        return {"status": 201, "message": message, "data": data}

    @staticmethod
    def __400_error_message(message):  # pragma: no cover
        return {"status": 400, "message": message, "data": []}

    @staticmethod
    def __401_error_message(message):  # pragma: no cover
        return {"status": 401, "message": message, "data": []}

    @staticmethod
    def __403_error_message(message):  # pragma: no cover
        return {"status": 403, "message": message, "data": []}

    @staticmethod
    def __404_error_message(message):  # pragma: no cover
        return {"status": 404, "message": message, "data": []}

    @staticmethod
    def __500_error_message(message=INTERNAL_SERVER_ERROR, data=None):  # pragma: no cover
        data = [] if data is None else data
        return {"status": 500, "message": message, "data": data}

    @staticmethod
    def _sha224(data):
        return hashlib.sha224(data.encode("utf-8")).hexdigest()

    @classmethod
    def _show_error(cls, error_code, error_message):  # pragma: no
        if error_code != 400 and error_code != 401 and error_code != 403:
            error_code = 500
        response_code_list = {
            400: cls.__400_error_message(error_message),
            401: cls.__401_error_message(error_message),
            403: cls.__403_error_message(error_message),
            500: cls.__500_error_message(error_message)
        }
        return response_code_list[error_code]
