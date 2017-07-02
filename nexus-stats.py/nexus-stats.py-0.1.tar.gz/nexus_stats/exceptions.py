class NexusException(Exception):
    """Base exception."""
    pass

class ServerException(NexusException):
    """Raised when the server is unavailable."""
    pass

class UserNotFound(NexusException):
    """Raised when using the profile endpoint on a user that doesn't exist."""
    pass

class ProfileFieldNotFound(NexusException):
    """Raised when a field of a user's profile is not detected."""
    def __init__(self, field):
        self.field = field

class MissingInput(NexusException):
    """Raised when a function is called without a required argument."""
    def __init__(self, functionUsed, argMissing):
        self.function = functionUsed
        self.argMissing = argMissing