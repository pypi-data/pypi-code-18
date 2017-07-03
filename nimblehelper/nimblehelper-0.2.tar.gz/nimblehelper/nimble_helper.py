from .exceptions import BadInputException, InvalidAuthentication


# This class was created in order to extract functionality from nimble microservices
class NimbleHelper:
    # Checks Request For HTTP_X_CONSUMER_ID header (indicates kong has authorized the request)
    @staticmethod
    def __check_authorization(request):
        x_consumer_id = request.META.get('HTTP_X_CONSUMER_ID', None)
        if not x_consumer_id:
            raise InvalidAuthentication
        return x_consumer_id

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
            'x_consumer_id': cls.__check_authorization(request),
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
            'x_consumer_id': cls.__check_authorization(request),
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
