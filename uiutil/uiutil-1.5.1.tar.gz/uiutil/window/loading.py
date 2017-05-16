
import os
from Tkconstants import EW

from .child import ChildWindow
from ..frame.loading import LoadingFrame


class LoadingWindow(ChildWindow):

    def __init__(self,
                 wait_func,
                 message=u'Loading...',
                 *args,
                 **kwargs):

        self.window_title = message
        self.wait_func = wait_func

        super(LoadingWindow, self).__init__(width=300,
                                            height=40 if os.name == u'nt' else 35,
                                            fixed=True,
                                            padding=u'0 0 0 0',
                                            *args,
                                            **kwargs)

    def _setup(self):
        self.overrideredirect(1)  # Setting this to 1 makes window borderless (plus no OS close button)

        self.config = LoadingFrame(parent=self._main_frame,
                                   wait_func=self.wait_func)
        self.config.grid(sticky=EW)
