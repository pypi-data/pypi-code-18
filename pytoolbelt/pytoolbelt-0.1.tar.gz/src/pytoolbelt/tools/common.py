# -*- coding: utf-8 -*-

def forward_property(name, data_member="_data"):
    """ a simple property-forwarder
    this forwarder is used for accessing property-values which are contained in a separate container


    class Foo(object):
        def __init__(self, data):
            self._data = data

        id = forward_property("id")

    class Foo(object):
        def __init__(self, data):
            self._bar = data

        id = forward_property("id", data_member="bar")

    data = dict(id=1)

    foo1 = Foo(data)
    foo2 = Foo(data)

    print foo1.id
    >> 1
    print foo2.id
    >> 1
    """
    def _obj_from_chain(chain_key, current_dom):
        for attr_name in chain_key.split("."):
            current_dom = getattr(current_dom, attr_name)
        return current_dom

    def getter(self): return getattr(_obj_from_chain(data_member, self),name)
    def setter(self, value): setattr(_obj_from_chain(data_member, self), name, value)
    return property(getter, setter)

