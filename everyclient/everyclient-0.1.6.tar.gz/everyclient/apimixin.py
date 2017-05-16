# -*- coding: utf-8 -*-
from .http import HTTP
from .config import open_apis


class APIMixin(HTTP):

    def __getattr__(self, name):
        if not hasattr(super(APIMixin, self), name):
            self.set_attr(name)
        return self.__getattribute__(name)

    def set_attr(self, name):
        if name in open_apis:
            super(APIMixin, self).__setattr__(name, self._create_func(name))
        else:
            raise AttributeError(
                "\n-----------------------------------------------------\n"
                "The API method \'%s\' is not supported by Everysense."
                "\n-----------------------------------------------------\n"
                "Surpported API methods are: "
                "%s" 
                "\n-----------------------------------------------------\n"
                % (str(name), str(open_apis))
                )

    def _create_func(self, name):
        def func(args):
            return self.request(name, args)
        func.__name__ = name
        return func
        