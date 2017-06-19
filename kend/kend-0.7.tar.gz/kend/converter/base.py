import exceptions


class ConversionError(exceptions.ValueError):
    pass

class NotImplementedError(ConversionError):
    """Raised when attempting to call an unimplemented converter method"""
    pass

class ParseError(ConversionError):
    """Raised when attempting to parse a format"""
    pass

class FormatError(ConversionError):
    """Raised when attempting to parse a format of the wrong schema"""
    pass

class VersionError(ConversionError):
    """Raised when attempting to parse a format of the wrong version"""
    pass

class SerialisationError(ConversionError):
    """Raised when attempting to serialise an incomplete object"""
    pass


class BaseConverter:

    @staticmethod
    def parse(*args, **kwargs):
        raise NotImplementedError()

    @staticmethod
    def serialise(*args, **kwargs):
        raise NotImplementedError()

class InvalidConverter:

    @staticmethod
    def parse(*args, **kwargs):
        raise ParseError('Unable to find parser for requested class (%s).' % str(args[0]))

    @staticmethod
    def serialise(*args, **kwargs):
        raise SerialisationError('Unable to find serialiser for requested class (%s).' % str(args[0]))

    
MIME_TYPE_BASE = 'application/x-kend'
