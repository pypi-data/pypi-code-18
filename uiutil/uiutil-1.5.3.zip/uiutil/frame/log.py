
import logging
import ttk
from Tkconstants import E, W, NSEW, NORMAL, DISABLED

from .frame import BaseFrame
from ..widget.scroll import TextScroll
from ..helper.text_handler import TextHandler
from ..widget.combobox import Combobox
from ..widget.label import Label
from ..widget.button import Button


class LogFrame(BaseFrame):

    BUTTON_WIDTH = 20

    def __init__(self,
                 *args,
                 **kwargs):

        self.__enable_poll = False

        BaseFrame.__init__(self, *args, **kwargs)

        self.log_level_label = Label(initial_value=u'Log Level:',
                                     row=self.row.start(),
                                     column=self.column.start(),
                                     sticky=W)

        self.level_list = [u'DEBUG',
                           u'INFO',
                           u'WARNING',
                           u'ERROR',
                           u'CRITICAL']

        self.log_level = Combobox(initial_value=u'INFO',
                                  values=self.level_list,
                                  trace=self.__level_change,
                                  column=self.column.next(),
                                  sticky=W)

        self.clear_button = Button(state=NORMAL,
                                   initial_value=u'Clear',
                                   width=self.BUTTON_WIDTH,
                                   command=self.__clear,
                                   column=self.column.next(),
                                   sticky=E,
                                   tooltip=u'Clear the log window')
        self.columnconfigure(self.column.current, weight=1)

        self.log_text = TextScroll(state=DISABLED,
                                   row=self.row.next(),
                                   column=self.column.start(),
                                   columnspan=3,
                                   sticky=NSEW)
        self.rowconfigure(self.row.current, weight=1)

        self.log_text.configure(font=u'TkFixedFont')

        # Create textLogger
        self.text_handler = TextHandler(self.log_text)
        self.text_handler.setLevel(self.log_level.value)

        # Add the handler to root logger
        logger = logging.getLogger()
        logger.addHandler(self.text_handler)

        self.__enable_poll = True

    def __level_change(self):
        self.text_handler.setLevel(self.log_level.value)

    def __clear(self):
        self.text_handler.clear()

    def poll(self):
        if self.__enable_poll:
            self.text_handler.poll()
