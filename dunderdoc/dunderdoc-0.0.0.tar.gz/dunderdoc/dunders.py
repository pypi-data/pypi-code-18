from enum import Enum

dunder_dict = {}  # dict is populated by creating an instance of `Dunder`


class DunderSections(Enum):
    binary = 'Binary Operators'
    unary = 'Unary Operations'
    inplace = 'Inplace Binary Operator (=)'
    reverse = 'Reverse Binary Operations'
    comparison = 'Comparison operators'
    async = 'Async methods'
    advanced = 'Advanced methods you probably wont need'
    read = 'Designed for reading'
    other = 'Possibly interesting methods for modifying how a class behaves'
    special = 'Special python methods for internal things'
    ignore = 'Dont show this'


class Dunder:
    """
    Compat class for namespacing reasons. Also allows to add a metaclas
    in the future if we need it?
    """
    method = 'ignore'
    section = DunderSections.ignore

    def __init__(self, method=None):
        if method:
            dunder_dict[self.method] = self
        super().__init__()


class BinaryDunder(Dunder):
    reason_string = 'Used for the {operator} operator.'
    usage_string = 'myobject {operator} 5'
    method = None
    section = DunderSections.binary
    example_string = """
    def {method}(self, other):
        if isinstance(other, MyClass):
            return self.data {operator} other.data
        else:
            raise TypeError
    """

    @property
    def example(self):
        return self.example_string.format(
            method=self.method, operator=self.operator)

    @property
    def reason(self):
        return self.reason_string.format(operator=self.operator)

    @property
    def usage(self):
        return self.usage_string.format(operator=self.operator)

    def __init__(self, method=None, operator=None):
        self.method = method
        self.operator = operator
        super().__init__(method=method)


class ReversedBinaryDunder(BinaryDunder):
    reason_string = 'Used for reversed {operator} operator.'
    usage = '5 {operator} myobject'
    section = DunderSections.reverse
    example_string = """
    def {method}(self, other):
        if isinstance(other, MyClass):
            return other.data {operator} self.data
        else:
            raise TypeError
    """


class InPlaceBinaryDunder(BinaryDunder):
    reason_string = 'Used for the {operator} operator. Modifies the object.'
    section = DunderSections.inplace
    example_string = """
    def {method}(self, other):
        if isinstance(other, MyClass):
            self.data {operator} other.data
        else:
            raise TypeError
    """


class ComparisonDunder(BinaryDunder):
    reason_string = 'Used for the {operator} comparison operator.'
    section = DunderSections.comparison


class ReverseComparisonDunder(ReversedBinaryDunder):
    reason_string = 'Used for the reversed {operator} comparison operator.'
    section = DunderSections.comparison


class UnaryDunder(Dunder):
    method = None
    section = DunderSections.unary
    operator = None

    def is_op(self):
        return not ('(' in self.operator and ')' in self.operator)

    @property
    def reason(self):
        return 'Used for the {} unary operator.'.format(self.operator)

    @property
    def usage(self):
        return self.get_operator_string('myobject')

    def get_operator_string(self, data):
        if self.is_op():
            return '{}{}'.format(self.operator, data)
        else:
            return '{}({})'.format(self.operator.rstrip('()'), data)

    @property
    def example(self):
        return '''
    def {}(self):
        return {}
        '''.format(self.method, self.get_operator_string('self.data'))

    def __init__(self, method=None, operator=None):
        self.method = method
        self.operator = operator
        super().__init__(method=method)


BinaryDunder(method='__add__', operator='+')
BinaryDunder(method='__sub__', operator='-')
BinaryDunder(method='__mul__', operator='*')
BinaryDunder(method='__floordiv__', operator='//')
BinaryDunder(method='__truediv__', operator='/')
BinaryDunder(method='__mod__', operator='%')
BinaryDunder(method='__pow__', operator='**')
BinaryDunder(method='__lshift__', operator='<<')
BinaryDunder(method='__rshift__', operator='>>')
BinaryDunder(method='__and__', operator='&')
BinaryDunder(method='__or__', operator='|')
BinaryDunder(method='__xor__', operator='^')
BinaryDunder(method='__matmul__', operator='@')


# get all binary dunders
binary_dunders = []
for c, v in dunder_dict.items():
    if isinstance(v, BinaryDunder):
        binary_dunders.append(v)


# create i-dunders (in place binary operations) and r-dunders (reversed binary)
for c in binary_dunders:
    operator = c.operator + '='
    method = '__' + 'i' + c.method.strip('_') + '__'
    InPlaceBinaryDunder(method=method, operator=operator)

for c in binary_dunders:
    operator = c.operator
    method = '__' + 'r' + c.method.strip('_') + '__'
    ReversedBinaryDunder(method=method, operator=operator)


ComparisonDunder(method='__lt__', operator='<')
ComparisonDunder(method='__le__', operator='<=')
ComparisonDunder(method='__eq__', operator='==')
ComparisonDunder(method='__ne__', operator='!=')
ComparisonDunder(method='__ge__', operator='>=')
ComparisonDunder(method='__gt__', operator='>')

comp_dunders = [v for c, v in dunder_dict.items()
                if isinstance(v, ComparisonDunder)]

# add reversed comparison
for c in comp_dunders:
    operator = c.operator
    method = '__' + 'r' + c.method.strip('_') + '__'
    ReversedBinaryDunder(method=method, operator=operator)


UnaryDunder(method='__neg__', operator='-')
UnaryDunder(method='__pos__', operator='+')
UnaryDunder(method='__invert__', operator='~')
UnaryDunder(method='__abs__', operator='abs()')
UnaryDunder(method='__complex__', operator='complex()')
UnaryDunder(method='__int__', operator='int()')
UnaryDunder(method='__long__', operator='long()')
UnaryDunder(method='__float__', operator='float()')
UnaryDunder(method='__oct__', operator='oct()')
UnaryDunder(method='__hex__', operator='hex()')
UnaryDunder(method='__bool__', operator='bool()')
UnaryDunder(method='__bytes__', operator='bytes()')
UnaryDunder(method='__round__', operator='round()')


class GenericDunder(Dunder):
    def __init__(self, method, reason, section, usage, example):
        self.method = method
        self.reason = reason
        self.section = section
        self.usage = usage
        self.example = example
        super().__init__(method=method)

GenericDunder('__future__',
              'Special dunder, can not be implemented. '
                'This is used when importing python3 compatability libraries in python2',
              DunderSections.special,
              'from __future__ import',
              example='n/a')
GenericDunder('__aenter__',
              'Used for async context manager.',
              DunderSections.async,
              'async with myobject as something:',
              example='see __enter__')
GenericDunder('__aexit__',
              'Used for async context manager.',
              DunderSections.async,
              'called when by python when `async with` finishes',
              example='see __exit__')
GenericDunder('__aiter__',
              'Used for async iterators.',
              DunderSections.async,
              'async for i in myobject:',
              example=None)
GenericDunder('__anext__',
              'Async iterator equivalent of __next__',
              DunderSections.async,
              'Used by python during async iteration',
              example='see __next__')
GenericDunder('__await__',
              'Await an object (instead of a function)',
              DunderSections.async,
              'await myobject',
              example=None)

# Advanced
# todo: Stuff most wont need, put examples and things for these things
GenericDunder('__new__',
              'Probably wont need',
              DunderSections.advanced,
              'todo',
              example=None)
GenericDunder('__mro__',
              'Probably wont need',
              DunderSections.advanced,
              'todo',
              example=None)
GenericDunder('__bases__',
              'Probably wont need',
              DunderSections.advanced,
              'todo',
              example=None)
GenericDunder('__weakref__',
              'Probably wont need',
              DunderSections.advanced,
              'todo',
              example=None)
GenericDunder('__self__',
              'Probably wont need',
              DunderSections.advanced,
              'todo',
              example=None)
GenericDunder('__prepare__',
              'Probably wont need',
              DunderSections.advanced,
              'todo',
              example=None)
GenericDunder('__classcell__',
              'Probably wont need',
              DunderSections.advanced,
              'todo',
              example=None)
GenericDunder('__objclass__',
              'Probably wont need',
              DunderSections.advanced,
              'todo',
              example=None)
GenericDunder('__get__',
              'Probably wont need',
              DunderSections.advanced,
              'todo',
              example=None)
GenericDunder('__set__',
              'Probably wont need',
              DunderSections.advanced,
              'todo',
              example=None)
GenericDunder('__delete__',
              'Probably wont need',
              DunderSections.advanced,
              'todo',
              example=None)
GenericDunder('__func__',
              'Probably wont need',
              DunderSections.advanced,
              'todo',
              example=None)
GenericDunder('__code__',
              'Probably wont need',
              DunderSections.advanced,
              'todo',
              example=None)
GenericDunder('__import__',
              'Probably wont need',
              DunderSections.special,
              'n/a',
              example=None)
GenericDunder('__init_subclass__',
              'Probably wont need',
              DunderSections.advanced,
              'n/a',
              example=None)
GenericDunder('__instancecheck__',
              'Probably wont need',
              DunderSections.advanced,
              'n/a',
              example=None)
GenericDunder('__length_hint__',
              'Probably wont need',
              DunderSections.advanced,
              'n/a',
              example=None)
GenericDunder('__missing__',
              'Probably wont need',
              DunderSections.advanced,
              'n/a',
              example=None)
GenericDunder('__subclasscheck__',
              'Probably wont need',
              DunderSections.advanced,
              'n/a',
              example=None)
GenericDunder('__set_name__',
              'Probably wont need',
              DunderSections.advanced,
              'n/a',
              example=None)



# read attributes
GenericDunder('__annotations__',
              'Designed for reading',
              DunderSections.read,
              'todo',
              example='n/a')
GenericDunder('__class__',
              'Designed for reading. Returns the class of the object.',
              DunderSections.read,
              'myobject.__class__',
              example='n/a')
GenericDunder('__closure__',
              'Designed for reading',
              DunderSections.read,
              'todo',
              example='n/a')
GenericDunder('__defaults__',
              'Designed for reading',
              DunderSections.read,
              'todo',
              example='n/a')
GenericDunder('__dict__',
              'Designed for reading. Gives the objects data as a dictionary.\n'
              '(Will not work if __slots__ is being used exclusively)',
              DunderSections.read,
              'myobject.__dict__',
              example='n/a')
GenericDunder('__doc__',
              'Designed for reading',
              DunderSections.read,
              'todo',
              example='n/a')
GenericDunder('__file__',
              'Designed for reading. Get the file of the module.',
              DunderSections.read,
              'mymodule.__file__',
              example='n/a')
GenericDunder('__globals__',
              'Designed for reading',
              DunderSections.read,
              'todo',
              example='n/a')
GenericDunder('__kwdefaults__',
              'Designed for reading',
              DunderSections.read,
              'todo',
              example='n/a')
GenericDunder('__module__',
              'Designed for reading',
              DunderSections.read,
              'todo',
              example='n/a')
GenericDunder('__name__',
              'Designed for reading. Get the name of the class.',
              DunderSections.read,
              'self.__class__.__name__',
              example='n/a')
GenericDunder('__qualname__',
              'Designed for reading. Get the fully qualified class name',
              DunderSections.read,
              'self.__class__.__qualname__',
              example='n/a')


# possibly interesting ones that people actually use
GenericDunder('__dir__',
              'Override the behavior of dir()',
              DunderSections.other,
              'dir(myobject)',
              example='''\
    def __dir__(self):
        return [k for k in self.__dict__ if not k.startswith('__')]
    ''')
GenericDunder('__contains__',
              'Used for the `in` operator',
              DunderSections.other,
              '5 in myobject',
              example='''
    def __contains__(self, object):
        return object in self.data
    ''')
GenericDunder(
    '__call__',
    'Call the object like a function',
    DunderSections.other,
    'myobject()',
    example='''
    def __call__(self, *args, **kwargs):
        return self._run(*args, **kwargs)
    ''')
GenericDunder(
    '__del__',
    'Called by the GC when the object gets deleted',
    DunderSections.other,
    'Called by the GC when the object gets deleted. '
    'It will NOT be called during `del myobject` '
    'if there is more than one reference to the object',
    example='''
    def __del__(self):
        self.connection.close()
        self.connection.wait_till_closed()
        del self.connection
        ''')
GenericDunder(
    '__delattr__',
    'Delete an attribute',
    DunderSections.other,
    'del myobject.someattr',
    example='''
    def __delattr__(self, attr):
        if attr == 'myconn':
            self.myconn.close()
    ''')
GenericDunder('__delitem__',
              'Delete an item (square bracket notation)',
              DunderSections.other,
              'del myobject[someitem]',
              example=None)
GenericDunder('__enter__',
              'Context manager enter',
              DunderSections.other,
              'with myobject:',
              example=None)
GenericDunder('__exit__',
              'Context manager exit',
              DunderSections.other,
              'called by python when the `with myobject:` block ends',
              example=None)
GenericDunder('__getattr__',
              'Get an attribute not found. Only called if attr is not found on object.',
              DunderSections.other,
              'getattr(myobject)',
              example='''
    def __getattr__(self, attr):
        if attr in self._color_dict:
            return self._color_dict[attr]
        return getattr(self.data)
    ''')
GenericDunder('__getattribute__',
              'Get an attribute. ALWAYS called during `getattr()`',
              DunderSections.other,
              'getattr(myobject)',
              example=None)
GenericDunder('__getitem__',
              'Get an item (Square bracket notation)',
              DunderSections.other,
              'myobject[someitem]',
              example=None)
GenericDunder('__setitem__',
              'Set an item (Square bracket notation)',
              DunderSections.other,
              'myobject[someitem] = 5',
              example='n/a')
GenericDunder('__hash__',
              'Calculate the hash of the object. Useful when storing in a set'
              'or as the key to a dictionary',
              DunderSections.other,
              'Used by python when an object is hashed',
              example=None)
GenericDunder('__init__',
              'Initialize the existing object.',
              DunderSections.other,
              'myobject = MyClass(*args)',
              example=None)
GenericDunder('__len__',
              'Get the length of the object',
              DunderSections.other,
              'len(myobject)',
              example=None)
GenericDunder('__str__',
              'Get the pretty string representation of the object (usually for printing)',
              DunderSections.other,
              'str(myobject); print(myobject)',
              example=None)
GenericDunder('__slots__',
              'Set an items slots instead of using __dict__',
              DunderSections.other,
              'class MyClass: __slots__ = (some, vals)',
              example=None)
GenericDunder('__setattr__',
              'Set an attribute. Always called anytime an attribute is set',
              DunderSections.other,
              'myobject.someattr = 5',
              example=None)
GenericDunder('__next__',
              'Used by python for iteration. Return the next item.',
              DunderSections.other,
              'next(myobject)',
              example=None)
GenericDunder('__repr__',
              'Get the string representation for the object for debugging purposes.',
              DunderSections.other,
              '>>> myobject   (in REPL)',
              example=None)
GenericDunder('__format__',
              'The string representation of the object when used in a format block',
              DunderSections.other,
              '"somestring {}".format(myobject)',
              example=None)
GenericDunder('__index__',
              'Get the integer representation of the object for index slicing reasons',
              DunderSections.other,
              'somelist[myobject:otherobject]',
              example=None)
GenericDunder('__iter__',
              'Return a iterator object that contains __next__. (could be self)',
              DunderSections.other,
              'for i in myobject',
              example=None)
GenericDunder('__reversed__',
              'Just like __iter__ except it returns the items in reversed order (starting at index -1)',
              DunderSections.other,
              'for i in reversed(myobject)',
              example=None)

GenericDunder('__main__',
              'The name of the entrypoint file to python.\n'
              'Also can create a __main__.py, which will be run during'
              '\n the -m flag on python',
              DunderSections.special,
              'python -m mypackage',
              example=None)





