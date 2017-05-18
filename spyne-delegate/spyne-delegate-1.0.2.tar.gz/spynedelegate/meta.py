from functools import update_wrapper
from copy import copy

import inspect

import six

from spyne.decorator import rpc as original_rpc
from spyne.service import ServiceBase, ServiceBaseMeta

__all__ = ('rpc', 'DelegateBase', 'ExtensibleServiceBase')


_FORCE_EXCEPTION_NAMESPACE = '_FORCE_EXCEPTION_NAMESPACE'
_throws = '_throws'

class SpyneMethodWrapper(object):
    """
    This class wraps a spyne service method.
    It can be used to access the original undecorated method, as well as
    retrieve the spyne rpc decorated method, using ``get_spyne_rpc``
    """
    def __init__(self, func, args, kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

    def _apply_kwargs_override(self, service_class_attrs):
        "Hook for implementing patches and fixes for problems in spyne"

        rpc_kwargs = self.kwargs

        # 1. fix exception namespace problem
        #
        # This is needed because spyne does not support multiple namespaces
        # with Fault types. So the first WSDL which is loaded 'wins' and has
        # the Fault class in it's namespace. This will result in unexpected
        # results, especially when you have multiple workers with uwsgi. When
        # we customize this and set the type_name, we have each Fault type
        # living in it's own namespace See also:
        # https://github.com/arskom/spyne/blob/master/spyne/interface/_base.py#L193
        # (fault.__namespace__ = self.get_tns())

        if _FORCE_EXCEPTION_NAMESPACE in service_class_attrs \
          and _throws in self.kwargs:

            ns = service_class_attrs[_FORCE_EXCEPTION_NAMESPACE]
            ExceptionType = self.kwargs[_throws]

            # don't modify the original kwargs. No reason.
            fixed_kwargs = copy(self.kwargs)

            # it might seem that we are making the mistake here of creating a
            # new type each time an rpc decorator is used with the ``_throws``
            # argument. That is true, but it doesn't matter. The typename is
            # the same as the original. And the namespace will be set fixed by
            # spyne.The only thing we are solving is that we are consistent
            # with the name and namespace, therefor solving the problem that
            # the error namespace switches each time we reload the wsdl in
            # uwsgi.
            fixed_kwargs[_throws] = ExceptionType.customize(
                type_name=ExceptionType.__name__,  # same name
                __namespace__=ns  # all the same namespace
            )
            rpc_kwargs = fixed_kwargs
            
            # EULGH BAH. (this happens only once at compile/parse time)

        return rpc_kwargs

    def get_spyne_rpc(self, delegate_class, service_class_attrs):
        # determine the arguments of the original method, and cut off
        # ``self`` and ``ctx``.
        _args = inspect.getargspec(self.func)[0][1:]

        # create a local variable to be referenced in the wrapper closure
        func = self.func

        # define a wrapper function that will serve as the rpc endpoint.
        # this function will be called for each spyne request.
        # it will instantiate a delegate instance and call the corresponding
        # method on it.
        def wrapper(ctx, *args, **kwargs):
            delegate_instance = delegate_class(ctx)
            return func.__get__(
                delegate_instance, delegate_class)(*args, **kwargs)

        # build a bound function, whose function signature will be copied to
        # our wrapper function, so spyne will see it as the original method
        bound_func = func.__get__(delegate_class(), delegate_class)

        # update the wrapper function with the bound function signature.
        func_with_sig = update_wrapper(wrapper, bound_func)

        # decorate our new wrapper function with the spyne rpc decorator.
        # use the original aruments to our replacement decorator,
        # but apply some fixes to the original kwargs.
        return original_rpc(
            _args=_args,
            *self.args,
            **self._apply_kwargs_override(service_class_attrs)
        )(func_with_sig)


class rpc(object):  # noqa
    """
    This is our replacement for the spyne rpc decorator.
    It can be used on ``DelegateBase`` methods instead of ``spyne.Service``
    methods
    """
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def __call__(self, func):
        self.wrapped_func = func
        return SpyneMethodWrapper(self.wrapped_func, self.args, self.kwargs)


class DelegateMetaClass(type):
    """
    This metaclass removes the ``rpc`` decorator from the methods in
    our delegate, but stores the decorated methods in a class variable
    called ``_spyne_cls_dict``. We can use this class dict to pass to
    the original spyne ``ServiceBaseMeta`` class and obtain a spyne
    service class all created new!
    """
    def __new__(cls, name, bases, attrs):
        delegate_attrs = {}
        spyne_attrs = {}

        # collect spyne methods from base classes.
        if attrs.get('collect_base_methods', True):
            for base in reversed(bases):
                spyne_attrs.update(getattr(base, '_spyne_cls_dict', {}))

        # collect spyne methods in the delegate class.
        for k, v in attrs.items():
            if isinstance(v, SpyneMethodWrapper):
                spyne_attrs[k] = v  # collect spyne method
                delegate_attrs[k] = v.func  # remove decorator for normal use.
            else:
                delegate_attrs[k] = v  # this is a regular method

        # set spyne methods to class variable.
        delegate_attrs['_spyne_cls_dict'] = spyne_attrs

        # create new type using the original methods, with the decorator
        # removed.
        return type.__new__(cls, name, bases, delegate_attrs)


@six.add_metaclass(DelegateMetaClass)
class DelegateBase(object):
    """
    Use this as the base class for delegate objects.

    It get's the ctx as a parameter when it is initialized, so now
    you can leave that shit out of the service declaration and acces it as:

    ``self.ctx``

    """
    def __init__(self, ctx=None):
        self.ctx = ctx

    @classmethod
    def get__spyne_cls_dict(cls, service_class_attrs):
        # create a class dict of the same shape a you would get when typing
        # code in a file. The class dict will be used to create a spyne
        # service class.
        return {
            k: v.get_spyne_rpc(cls, service_class_attrs) for k, v in cls._spyne_cls_dict.items()}


class DelegateServiceMetaClass(ServiceBaseMeta):
    """
    This metaclass will initialize a spyne service class with the methods on
    the delegate object. if you are crazy you can also still
    define methods in this service class and they will override the delegate
    methods.
    """
    def __init__(cls, name, bases, attrs):  # noqa
        delegate = attrs.get('delegate')
        if delegate is not None:

            # I think we don't need the delegate in the spyne class definition
            del attrs['delegate']

            # build cls_dict with spyne service methods from the delegate
            delegate_service_methods = delegate.get__spyne_cls_dict(attrs)

            # add all attributes defined in the class definition.
            delegate_service_methods.update(attrs)

            # call original spyne metoclass to construct spyne service class,
            # with all our delegate methids included! HOW PWN!!!
            return super(
                DelegateServiceMetaClass, cls).__init__(
                    name, bases, delegate_service_methods)

        else:  # there is no delegate, act normal
            return super(
                DelegateServiceMetaClass, cls).__init__(name, bases, attrs)


@six.add_metaclass(DelegateServiceMetaClass)
class ExtensibleServiceBase(ServiceBase):
    """
    Use this class instead of ``spyne.ServiceBase``.
    """
    pass
