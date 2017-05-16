
# import ttk
from Tkinter import W, EW

# import sys
# sys.path.append(u'..')

from uiutil.frame.frame import BaseFrame
from uiutil.window.root import RootWindow
from uiutil.widget.entry import TextEntry
# from validation import valid_ipv4, valid_ipv6
from ..validation import valid_ipv4, valid_ipv6


class IPEntry(TextEntry):

    def __init__(self,
                 frame,
                 value=None,
                 trace=None,
                 link=None,
                 bind=None,
                 ipv6=False,
                 allow_invalid_values=True,
                 **kwargs):

        self.allow_invalid_values = allow_invalid_values
        self.ipv6 = ipv6

        if value is None:
            value = u'::' if self.ipv6 else u'0.0.0.0'

        super(TextEntry, self).__init__(frame=frame,
                                        value=value,
                                        trace=trace,
                                        link=link,
                                        bind=bind,
                                        **kwargs)

        registered_validate_ip = self.widget.register(self.validate_ip)

        self.widget[u'validate'] = u"key",
        self.widget[u'validatecommand'] = (registered_validate_ip, u"%P")

    def validate_ip(self,
                    ip):

        valid_ip = valid_ipv6(ip) if self.ipv6 else valid_ipv4(ip)

        self.config(foreground=u'black' if valid_ip else u'red')

        return True if self.allow_invalid_values else valid_ip


class IPTestFrame(BaseFrame):

    def __init__(self,
                 *args,
                 **kwargs):

        BaseFrame.__init__(self, *args, **kwargs)

        self.label(text=u'IPv4:',
                   row=self.row.next(),
                   column=self.column.start(),
                   sticky=W)

        self.__ipv4_field = IPEntry(self,
                                    width=len(u'255.255.255.255'),
                                    row=self.row.current,
                                    column=self.column.next(),
                                    sticky=W)

        self.label(text=u'IPv6:',
                   row=self.row.next(),
                   column=self.column.start(),
                   sticky=W)

        self.__ipv6_field = IPEntry(frame=self,
                                    ipv6=True,
                                    width=len(u'abcd:abcd:abcd:abcd:abcd:abcd:abcd:abcd'),
                                    row=self.row.current,
                                    column=self.column.next(),
                                    sticky=W)


class DeviceIPEntryTest(RootWindow):

    def __init__(self, *args, **kwargs):
        super(DeviceIPEntryTest, self).__init__(*args, **kwargs)

    def _setup(self):

        self.title(u"Test Device Frame")
        self.ip_frame = IPTestFrame(parent=self._main_frame)
        self.ip_frame.grid(sticky=EW)


if __name__ == u'__main__':
    DeviceIPEntryTest()
