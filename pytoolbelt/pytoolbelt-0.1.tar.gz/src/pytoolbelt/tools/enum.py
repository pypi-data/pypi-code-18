# -*- coding: utf-8 -*-

""" This module provides simple enum support. A little bit of meta class


usage:

class Foo(enumerated):
    FOO = enum()

class Bar(enumerated):
    BAR = enum(value=1)

    def __setup__(self, value):
        self.value = value


print Foo.FOO
print Bar.BAR.value
"""

__all__ = ['enumerated', 'enum']


class _TagProperty(object):
    counter = 0

    def __init__(self, args, keys):
        super(_TagProperty, self).__init__()
        self._ordinal = _TagProperty.counter
        _TagProperty.counter += 1
        self._init_args = args
        self._init_keys = keys


class EnumClass(type):
    def __new__(klass, name, bases, defines):

        all_props = dict()
        tag_props = list()

        for key, value in defines.iteritems():
            if isinstance(value, _TagProperty):
                tag_props.append((key, value))
            else:
                all_props[key] = value

        self = type.__new__(klass, name, bases, all_props)

        elements = list()

        for key, value in tag_props:
            constant = self.__new__(self, key, value._ordinal, value._init_args, value._init_keys)
            setattr(self, key, constant)
            elements.append(constant)

        elements.sort(lambda s, t: cmp(s.__ordinal__, t.__ordinal__))

        for index, value in enumerate(elements):
            value.__ordinal__ = index

        self.__elements__ = tuple(elements)
        return self

    def get(self, name, default=None):
        value = getattr(self, name, None)
        if isinstance(value, self): return value
        return default

    def __getitem__(self, name):
        value = getattr(self, name, None)
        if isinstance(value, self): return value
        raise KeyError(name)


def unpickler(type, name):
    return type[name]


class enumerated(object):
    """Base class for enumeration types
    
    This class is the base class for all enumeration types. You define a new
    enumeration by inheriting from this class. Note, that you should never inherit
    from any enum class except this one.
    
    Actual instances of this class are usually only created by assignments of
    `enum()` to class properties in the class suite of a subclass definition.
    
    This class provides a total ordering of its instances, which relies on the
    implicit `ordinal` value assigned to each instance upon construction. Note,
    that two instances of this class are comparable (with respect to `<`, `<=`,
    `>`, `>=`) if (and only if) they are instances of the very same subclass.
    
    Equality is defined in terms of identity for this class.
    
    Example:
    
        >>> class Scope(enumerated):
        ...
        ...    LOCAL = enum()
        ...    CLASS = enum()
        ...    GLOBAL = enum()
        
    The resulting class is an enum, which defines three constant members, each
    of which is an instance of class `Scope`:
    
        >>> Scope.LOCAL
        Scope.LOCAL
        
    Enum constants are usable as indices, for example into lists or tuples:
    
        >>> data = [1, 2, 3]
        >>> data[Scope.CLASS]
        2
        
    The first defined constant has the implicit ordinal value `0`, the second one
    has the value `1`, and so on.
    
    You can associate arbitrary information to with each enum constant; simply
    pass keyword arguments to the `enum` function:
    
        >>> class Instruction(enumerated):
        ...
        ...    __slots__ = ('stack_effect', 'ppname')
        ...
        ...    PUSH = enum(ppname = 'push', stack_effect = 1)
        ...    POP = enum(ppname = 'pop', stack_effect = -1)
        ...    DUP = enum(ppname = 'duplicate', stack_effect = 1)
        ...    SWAP = enum(ppname = 'swap', stack_effect = 0)
        ...
        ...    def __setup__(self, ppname = None, stack_effect = 0):
        ...        self.ppname = ppname
        ...        self.stack_effect = stack_effect
        
    which is made available to the `__setup__` method (which is called instead 
    Python's standard `__init__` when an instance of an enumerated class is
    created.)
    """

    __metaclass__ = EnumClass
    __slots__ = ('__weakref__', '__name__', '__ordinal__',)

    def __new__(klass, name, ordinal, args=(), keys={}):
        self = object.__new__(klass)
        self.__name__ = name
        self.__ordinal__ = ordinal
        self.__setup__(*args, **keys)
        return self

    def __setup__(self):

        """Initializer for enum constants
        
        This method is called instead of Python's standard `__init__`, when an
        enumeration constant value is constructed. It receives the arguments passed
        to the `enum` function when the defining class body was executed. 
        Subclasses may define additional set-up code here.
        """

        pass

    def ordinal(self):

        """Obtains this constant's ordinal value
        
        Every enumeration constant has an ordinal value, which can be obtained by
        calling this method. The ordinal is implicitly defined by the definition
        order in the `class` statement, which constructed the enum.
        """

        return self.__ordinal__

    def name(self):

        """Obtains this constant's name
        
        Every enumeration constant has a name, which is implicitly defined by the
        name, the constant has been assigned to in the body of the `class` statement.
        This method returns the name thus given to the constant.
        """

        return self.__name__

    def __str__(self):
        return "%s.%s" % (self.__class__.__name__, self.__name__)

    def __repr__(self):
        return self.__str__()

    def __le__(self, other):
        if not isinstance(other, type(self)): return NotImplemented
        return self.__ordinal__ <= other.__ordinal__

    def __lt__(self, other):
        if not isinstance(other, type(self)): return NotImplemented
        return self.__ordinal__ < other.__ordinal__

    def __ge__(self, other):
        if not isinstance(other, type(self)): return NotImplemented
        return self.__ordinal__ >= other.__ordinal__

    def __gt__(self, other):
        if not isinstance(other, type(self)): return NotImplemented
        return self.__ordinal__ > other.__ordinal__

    def __index__(self):
        return self.__ordinal__

    def __reduce__(self):
        return unpickler, (type(self), self.__name__)


def enum(*args, **keys):
    """Define an enumeration constant within a `enum` class body
    
    This function should only be used in the body of a `class` suite defining
    a new enumeration. The value returned is a temporary placeholder for the
    enumeration constant being defined.
    
    Any arguments supplied to this function will be passed down to the new
    constant's `__setup__` method when the constant value is actually created.
    """

    return _TagProperty(args, keys)
