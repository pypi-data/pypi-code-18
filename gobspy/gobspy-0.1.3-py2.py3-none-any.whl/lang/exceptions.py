from .utils import indent

class BoardFormatException(Exception):
    pass

class SourceException(Exception):

    def __init__(self, message, area=None):
        self.message = message
        self.area = area

    def __repr__(self):
        s = ''
        if self.area:
            s += '\n%s\n' % (self.area,)
        s += '%s\n' % (indent(self.message),)
        return s

    def error_type(self):
        return 'Error'


class StaticException(SourceException):
    pass


class DynamicException(SourceException):
    pass
