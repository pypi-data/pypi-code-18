import typing


def check_iterable(iterable: typing.Iterable, name: str) -> None:
    """
    Helper method to check if an object is iterable. Throws TypeError if it is not
    :param iterable: The object to check
    :param name: The name of the iterable. Used for constructing the exception
    :return: None
    """
    try:
        # Iter will try to fetch the iterator, and raises a TypeError if something is not OK
        iter(iterable)
    except TypeError:
        raise TypeError("Parameter '{}' must be an 'iterable' object".format(name))


def check_callable(callable_object: typing.Callable, name: str, optional: bool=False) -> None:
    """
    Helper method to check if an object is callable. Throws TypeError if it is not
    :param callable_object: The object to check
    :param name: The name of the iterable. Used for constructing the exception
    :param optional: If true, callable_object can be None
    :return: 
    """
    if not callable(callable_object):
        # If the parameter is optional, it can be None, which is OK
        if optional and callable_object is None:
            return
        raise TypeError("Parameter '{}' must be a 'callable' object".format(name))
