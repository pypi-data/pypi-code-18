"""
Packer specific errors
"""

class PackerError(Exception):
    """
    Generic Packer exception
    """

class PackerUnknownFormatType(PackerError):
    """
    Packer error raised when an unknown format type is specified
    """

class PackerMalformedDataError(PackerError):
    """
    Packer error raised for malformed data
    """
