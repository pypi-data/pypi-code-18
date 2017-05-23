

from Tkinter import W, EW
from uiutil.frame.frame import BaseFrame
from uiutil.window.root import RootWindow
from uiutil.widget.entry import TextEntry

if __name__ == u"__main__":
    import sys
    sys.path.append(u'..')
    from validation import valid_ipv4, valid_ipv6
else:
    from ..validation import valid_ipv4, valid_ipv6


class IPEntryBase(TextEntry):

    # Need to define DEFAULT_VALUE
    # Need to define VALIDATE_IP_FUNCTION

    def __init__(self,
                 allow_invalid_values=True,
                 *args,
                 **kwargs):
        self.allow_invalid_values = allow_invalid_values

        kwargs[u'initial_value'] = kwargs.get(u'initial_value', self.DEFAULT_VALUE)

        super(TextEntry, self).__init__(*args,
                                        **kwargs)

        registered_validate_ip = self.widget.register(self.validate_ip)

        self.widget[u'validate'] = u"key",
        self.widget[u'validatecommand'] = (registered_validate_ip, u"%P")

    def validate_ip(self,
                    ip):
        valid_ip = self.VALIDATE_IP_FUNCTION(ip)

        self.config(foreground=u'black' if valid_ip else u'red')

        return True if self.allow_invalid_values else valid_ip


class IPv4Entry(IPEntryBase):
    DEFAULT_VALUE = u'0.0.0.0'
    VALIDATE_IP_FUNCTION = valid_ipv4

    def __init__(self,
                 *args,
                 **kwargs):
        super(IPv4Entry, self).__init__(*args,
                                        **kwargs)
class IPv6Entry(IPEntryBase):
    DEFAULT_VALUE = u'::'
    VALIDATE_IP_FUNCTION = valid_ipv6

    def __init__(self,
                 *args,
                 **kwargs):

        super(IPv6Entry, self).__init__(*args,
                                        **kwargs)



class IPTestFrame(BaseFrame):

    def __init__(self,
                 *args,
                 **kwargs):

        BaseFrame.__init__(self, *args, **kwargs)

        self.label(text=u'IPv4:',
                   row=self.row.next(),
                   column=self.column.start(),
                   sticky=W)

        self.__ipv4_field = IPv4Entry(self,
                                      width=len(u'255.255.255.255'),
                                      row=self.row.current,
                                      column=self.column.next(),
                                      sticky=W)

        self.label(text=u'IPv6:',
                   row=self.row.next(),
                   column=self.column.start(),
                   sticky=W)

        self.__ipv6_field = IPv6Entry(frame=self,
                                      width=len(u'abcd:abcd:abcd:abcd:abcd:abcd:abcd:abcd'),
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
