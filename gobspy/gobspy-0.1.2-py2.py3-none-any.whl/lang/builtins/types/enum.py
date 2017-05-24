from ...i18n import translate as t

class Enum(object):
    """Represents an enumerated type."""

    def __init__(self, i):
        self._ord = int(i)

    def enum_type(self):
        """Subclasses should implement the method to return the name
        of the enumerated type."""
        raise Exception("Subclass responsibility")

    def enum_size(self):
        """Subclasses should implement the method to return the number
        of elements in the enumerated type."""
        raise Exception("Subclass responsibility")

    def next(self):
        """Returns the next element in the enumerated type. (Wrap around
        if the maximum is reached)."""
        return self.__class__((self._ord + 1) % self.enum_size())

    def prev(self):
        """Returns the previous element in the enumerated type. (Wrap around
        if the minimum is reached)."""
        return self.__class__((self._ord - 1) % self.enum_size())

    def opposite(self):
        """Returns the opposite element in the enumerated type.
        Currently only works for enums of an even number of elements,
        returning the opposite element if they were in a circle."""
        new_i = (self._ord + self.enum_size() / 2) % self.enum_size()
        return self.__class__(new_i)

    def ord(self):
        """Returns the ord of the instance in the enumerated type."""
        return self._ord

    def __eq__(self, other):
        return isinstance(other, Enum) and \
               self.enum_type() == other.enum_type() and \
               self._ord == other.ord()


class NamedEnum(Enum):

    def name(self):
        pass

    def initial(self):
        return self.name()[0]

    def i18n_name(self):
        return t(self.name())

    def i18n_initial(self):
        return self.i18n_name()[0]
