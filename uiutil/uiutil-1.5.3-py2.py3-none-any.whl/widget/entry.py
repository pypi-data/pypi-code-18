import ttk
from base_widget import BaseWidget


class TextEntry(BaseWidget):
    WIDGET = ttk.Entry
    VAR_TYPE = u'string_var'
    VAR_PARAM = u'textvariable'
    VAR_IS_OPTIONAL = False

    def __init__(self,
                 *args,
                 **kwargs):
        super(TextEntry, self).__init__(*args, **kwargs)


class IntEntry(BaseWidget):
    WIDGET = ttk.Entry
    VAR_TYPE = u'int_var'
    VAR_PARAM = u'textvariable'
    VAR_IS_OPTIONAL = False

    def __init__(self,
                 *args,
                 **kwargs):
        super(IntEntry, self).__init__(*args,
                                       **kwargs)
