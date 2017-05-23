import ttk
from base_widget import BaseWidget


class Button(BaseWidget):
    WIDGET = ttk.Button
    VAR_TYPE = u'string_var'
    VAR_PARAM = u'textvariable'

    def __init__(self,
                 *args,
                 **kwargs):
        super(Button, self).__init__(*args, **kwargs)
