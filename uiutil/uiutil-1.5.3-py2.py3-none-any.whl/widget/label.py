import ttk
from base_widget import BaseWidget


class Label(BaseWidget):
    WIDGET = ttk.Label
    VAR_TYPE = u'int_var'
    VAR_PARAM = u'textvariable'

    def __init__(self,
                 *args,
                 **kwargs):
        super(Label, self).__init__(*args,
                                    **kwargs)