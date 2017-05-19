from unittest.mock import MagicMock
from django.conf import settings


def force_prevented_calls(func):
    """
    Function decorator to enforce prevented calls during testing.
    Finally, it overrides the behaviour of the prevent_call_in_testing decorator
    :param func: 
    :return: None
    """

    def func_wrapper(*args, **kwargs):
        old_value = None
        if hasattr(settings, 'IS_TESTING_ENVIRONMENT'):
            old_value = settings.IS_TESTING_ENVIRONMENT
            settings.IS_TESTING_ENVIRONMENT = False
        try:
            result = func(*args, **kwargs)
        finally:
            if old_value is not None:
                settings.IS_TESTING_ENVIRONMENT = old_value

        return result

    return func_wrapper


def prevent_call_in_testing(return_value=None):
    """
    Function decorator to prevent kontakt api calls if it's run in testing environment
    :param return_value: Mock value
    :return: Returns return_value if in testing environment
    """
    def real_decorator(func):
        def func_wrapper(*args, **kwargs):
            if isinstance(func, MagicMock):
                # Method is a mock. Execute anyway
                return func(*args, **kwargs)

            if hasattr(settings, 'IS_TESTING_ENVIRONMENT'):
                if settings.IS_TESTING_ENVIRONMENT:
                    return return_value  # Prevent API calls under testing conditions
            return func(*args, **kwargs)

        return func_wrapper
    return real_decorator
