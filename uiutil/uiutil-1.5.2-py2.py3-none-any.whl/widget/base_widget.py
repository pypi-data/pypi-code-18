from Tkinter import NORMAL, DISABLED

from ..mixin import WidgetMixIn, VarMixIn
from ..frame.introspection import locate_calling_base_frame


class BaseWidget(WidgetMixIn,
                 VarMixIn):

    # Define WIDGET when subclassing.
    # It should be a ttk widget, e.g ttk.Button
    #
    # Define VAR_TYPE when subclassing.
    # It should be a VarMixIn type, e.g self.string_var
    #
    # Define VAR_PARAM when subclassing.
    # It should be the parameter name into WIDGET that takes the variable, e.g. textvariable

    VAR_IS_OPTIONAL = True

    def __init__(self,
                 frame=None,
                 initial_value=None,
                 trace=None,
                 link=None,
                 bind=None,
                 *args,
                 **kwargs):
        """
        :param frame: Add the widget to this frame.
                      If not supplied, the nearest BaseFrame or BaseLabelFrame
                      in the stack will be used.
        :param initial_value: The initial value of the variable associated with the
                              widget.  If this is not supplied, then no variable is
                              created. Use the underlying widget's parameter to set
                              a static value (e.g. text for a Label)
        :param trace: function to trigger when the variable is modified
        :param link: a persistent object that the variable will link to
        :param bind: bindings for the widget
        :param kwargs: Parameters to pass to add_widget_and_position
        """

        # TODO: Add hooks for further customisation (e.g so that Switch can be based on this)
        try:
            self.WIDGET
        except AttributeError:
            raise NotImplementedError(u'WIDGET must be defined')

        try:
            self.VAR_TYPE
        except AttributeError:
            raise NotImplementedError(u'VAR_TYPE must be defined')

        try:
            self.VAR_PARAM
        except AttributeError:
            raise NotImplementedError(u'VAR_PARAM must be defined')

        super(BaseWidget, self).__init__(parent=frame, **kwargs)

        self.containing_frame = locate_calling_base_frame(frame)

        if not self.VAR_IS_OPTIONAL or initial_value is not None:
            # Declare the var
            var_type = getattr(self, self.VAR_TYPE)
            self.var = var_type(trace=trace,
                                link=link,
                                value=initial_value)

            kwargs[self.VAR_PARAM] = self.var

        if kwargs.get(u'tooltip'):
            self.widget, self.tooltip = self.containing_frame.add_widget_and_position(
                                            widget=self.WIDGET,
                                            frame=self.containing_frame,
                                            **kwargs)
        else:
            self.widget = self.containing_frame.add_widget_and_position(
                              widget=self.WIDGET,
                              **kwargs)

        # Copy methods of the underlying widget.
        widget_unbound_method_names = [method
                                       for method in dir(self.WIDGET)
                                       if not method.startswith(u'_') and method not in dir(self)]
        for method in widget_unbound_method_names:
             setattr(self, method, getattr(self.widget, method))

        if bind:
            try:
                self.bind(*bind)
            except AttributeError as e:
                raise RuntimeError(u'Underlying widget does not have a bind method')

    @property
    def value(self):
        try:
            return self.var.get()
        except AttributeError:
            raise RuntimeError(u'No variable was declared for this widget.')

    @value.setter
    def value(self,
              value):
        try:
            self.var.set(value)
        except AttributeError:
            raise RuntimeError(u'No variable was declared for this widget.')

    def enable(self):
        self.widget.config(state=NORMAL)

    def disable(self):
        self.widget.config(state=DISABLED)

