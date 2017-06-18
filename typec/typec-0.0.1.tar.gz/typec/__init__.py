# -*- coding: utf-8 -*-
#
# This file is part of the typec library
#
# Copyright (c) 2017 Tiago Coutinho
# Distributed under the MIT license. See LICENSE for more info.

"""
typec is a python library which provides facilities to
type check function arguments and class members
"""


from functools import wraps
from inspect import signature, isclass, ismodule

__version__ = '0.0.1'

__all__ = ['Int', 'Float', 'Str', 'Bool', 'Number', 'Positive', 'PositiveInt',
           'PositiveNumber', 'Iterable', 'Module', 'Class', 'Callable',
           'checked', 'Check', 'BaseFunctionCheck', 'BaseTypeCheck']

def __checked_function(f):
    sig, ann = signature(f), f.__annotations__
    @wraps(f)
    def wrapper(*args, **kwargs):
        bound = sig.bind(*args, **kwargs)
        for name, value in bound.arguments.items():
            if name in ann:
                ann[name].check(value, name=name)
        return f(*args, **kwargs)
    return wrapper


def __checked_class(cls):
    # apply checked decorator to methods
    for name, value in cls.__dict__.items():
        if callable(value):
            setattr(cls, name, checked(value))

    # Instantiate the Check class members
    for name, value in cls.__annotations__.items():
        if issubclass(value, Check):
            check = value()
        else:
            if isclass(value):
                check = Type(value)()
            elif callable(value):
                check = Func(value)()
        check.__set_name__(cls, name)
        setattr(cls, name, check)
    return cls


def checked(f_or_class):
    if isclass(f_or_class):
        check = __checked_class
    else:
        check = __checked_function
    return check(f_or_class)


class CheckMeta(type):

    def __and__(this_cls, other_cls):
        class And(Check):
            @classmethod
            def check(cls, value, *, name=''):
                this_cls.check(value, name=name)
                other_cls.check(value, name=name)
        return And

    def __or__(this_cls, other_cls):
        class Or(Check):
            @classmethod
            def check(cls, value, *, name=''):
                try:
                    this_cls.check(value, name=name)
                except:
                    other_cls.check(value, name=name)
        return Or


class Check(metaclass=CheckMeta):

    @classmethod
    def check(cls, value, *, name=''):
        return value

    def __set__(self, obj, value):
        if obj is None:
            pass
        self.check(value, name=self.name)
        obj.__dict__[self.name] = value

    def __set_name__(self, cls, name):
        self.name = name


class BaseFunctionCheck(Check):
    function = None
    exception = TypeError

    @classmethod
    def check(cls, value, *, name=''):
        if not cls.function(value):
            try:
                fname = cls.function.__name__
            except AttributeError:
                fname = cls.__name__
            if name:
                name = f' for {name!r}'
            raise cls.exception(f'Condition {fname!r} failed{name}')
        return value


_FUNCTION_MAP = {}
def Function(func, exc=TypeError):
    FunctionCheck = _FUNCTION_MAP.get(func)
    if FunctionCheck is None:
        class FunctionCheck(BaseFunctionCheck):
            function = func
            exception = exc
        FunctionCheck.__name__ = f'{func.__name__.capitalize()}Function'
    return FunctionCheck


class BaseTypeCheck(Check):
    type = None
    @classmethod
    def check(cls, value, *, name=''):
        if not isinstance(value, cls.type):
            if name:
                name = f' for {name!r}'
            raise TypeError(f'Expected type {cls.type.__name__!r}{name} (got ' \
                            f'type {type(value).__name__!r} instead)')
        return value


_TYPE_MAP = {}
def Type(typed):
    TypeCheck = _TYPE_MAP.get(typed)
    if TypeCheck is None:
        class TypeCheck(BaseTypeCheck):
            type = typed
        TypeCheck.__name__ = f'{typed.__name__.capitalize()}Type'
    return TypeCheck


class Positive(Check):
    @classmethod
    def check(cls, value, *, name=''):
        if value <= 0:
            raise ValueError(f'Expected >0 (got {value} instead)')
        return value


Int = Type(int)
Float = Type(float)
Str = Type(str)
Bool = Type(bool)
Number = Int | Float
PositiveInt = Int & Positive
PositiveNumber = Number & Positive
isiterable = lambda x : hasattr(x, '__iter__')
isiterable.__name__ = 'isiterable'
Iterable = Function(isiterable)
Module = Function(ismodule)
Class = Function(isclass)
Callable = Function(callable)

# -----------------------------------------------------------------------------
# main
# -----------------------------------------------------------------------------

def main():
    import time
    @checked
    def iplus(a, b, c: Module):
        Int.check(a, name='a')
        Int.check(b, name='b')
        return a + b
    try:
        iplus('hello', 1, time)
    except TypeError as te:
        print(f"iplus('hello', 1) threw {te}")

    try:
        iplus(1, 2, 'ups')
    except TypeError as te:
        print(f"iplus('hello', 1, 'ups') threw {te}")


if __name__ == '__main__':
    main()
