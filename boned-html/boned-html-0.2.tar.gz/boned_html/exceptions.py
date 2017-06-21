"""Some exceptions for boner
"""


class MismatchingText(Exception):
    """An exception raised when you provide text association to class but some text is missing
    """


class UnasignableChunk(Exception):
    """Trying to assigne a class to an unasignable chunk
    """
