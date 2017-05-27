"""
Python Instance Management
"""


class PyInstance(object):

    # Instance Tracker
    pyinstances = {}

    # Subkeys
    __INSTANCE = 'instance'
    __COUNTER = 'counter'

    def __new__(cls, session, *args, **kwargs):
        """
        Allocate a new instance or access an existing one using the session

        :param str session: name to reference the session by
        :retval: instance of cls
        """

        # Check if there is an existing instance
        if session not in cls.pyinstances:
            # there is not, so create one with refcount of zero
            cls.pyinstances[session] = {
                cls.__INSTANCE: super(PyInstance, cls).__new__(cls),
                cls.__COUNTER: 0
            }

        # increment the ref count
        cls.pyinstances[session][cls.__COUNTER] = (
            cls.pyinstances[session][cls.__COUNTER] + 1
        )

        # send the instance back to the caller
        return cls.pyinstances[session][cls.__INSTANCE]

    def __init__(self, session):
        """
        Initialize the instance

        :param str session: name of the session
        """
        # save the session name
        # it's primarily used to help clean up the pyinstances dict
        self.__session = session

    @property
    def session(self):
        """
        Return the active session the object instance is associated with

        :retval: str
        """
        return self.__session

    def __del__(self):
        """
        Clean up the instance

        .. note:: decrements the refernce counter and cleans out the session
            if the reference count hits zero (0).
        """

        if self.__session in PyInstance.pyinstances:
            # Decrement the reference counter
            PyInstance.pyinstances[self.__session][PyInstance.__COUNTER] = (
                PyInstance.pyinstances[
                    self.__session][PyInstance.__COUNTER] - 1
            )

            # If zero, clear out the session from the instances dict
            if not (
                PyInstance.pyinstances[self.__session][PyInstance.__COUNTER]
            ):
                del PyInstance.pyinstances[self.__session]
