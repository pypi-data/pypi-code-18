
from Tkinter import StringVar, IntVar, BooleanVar


class VarMixIn(object):

    def __init__(self,
                 *args,
                 **kwargs):

        super(VarMixIn, self).__init__()

    def _var(self,
             var,
             name=u'',
             value=None,
             trace=None,
             link=None):

        """
        Call with either value, value + trace or link. If these are mixed,
        link is used.
        :param var: This is the Var type, e.g. StringVar
        :param value: value to set the Var object to
        :param trace: Add a trace to the Var for triggering on change.
                      this is just the function to call
        :param link: link an object that has a get and set method
        :return:
        """

        if link and (value or trace):
            raise ValueError(u"If 'var' is called with 'link' set, "
                             u"don't also set value or trace")

        if link:
            # Initial value taken from the linked object
            value = link.get()

        if name.startswith(u'__'):
            raise ValueError(u"Private names (beginning with '__') aren't"
                             u"allowed. Mangling can't be done at runtime.")

        var = var() if value is None else var(value=value)

        if name:
            setattr(self,
                    name,
                    var)
            setattr(var,
                    u'name',
                    name)

        if link:
            # set the linked object value to the Var's value
            var.trace(u"w",
                      lambda name, index, mode: link.set(var.get()))

        elif trace is not None:
            var.trace(u"w",
                      lambda name, index, mode: trace())

        return var

    def string_var(self,
                   *args,
                   **kwargs):

        """See GUIHelpers.var for *args/**kwargs"""

        return self._var(var=StringVar,
                         *args,
                         **kwargs)

    def int_var(self,
                *args,
                **kwargs):

        """See GUIHelpers.var for *args/**kwargs"""

        return self._var(var=IntVar,
                         *args,
                         **kwargs)

    def boolean_var(self,
                    *args,
                    **kwargs):

        """See GUIHelpers.var for *args/**kwargs"""

        return self._var(var=BooleanVar,
                         *args,
                         **kwargs)
