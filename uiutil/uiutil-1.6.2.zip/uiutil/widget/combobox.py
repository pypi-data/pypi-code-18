import ttk
from base_widget import BaseWidget


class Combobox(BaseWidget):
    WIDGET = ttk.Combobox
    VAR_TYPE = u'string_var'
    VAR_PARAM = u'textvariable'
    VAR_IS_OPTIONAL = False

    def __init__(self,
                 *args,
                 **kwargs):
        super(Combobox, self).__init__(*args, **kwargs)

    @property
    def values(self):
        return self.widget[u'values']

    @values.setter
    def values(self,
               values):
        self.config(values=values)
