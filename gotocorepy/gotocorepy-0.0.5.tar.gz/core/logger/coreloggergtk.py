from core.logger.base.corebaselogger import CoreBaseLogger
from gi.repository import Gtk



class CoreLoggerGtk(CoreBaseLogger):
    def __init__(self):
        super(CoreLoggerGtk, self).__init__()
        self.window = Gtk.Window(Gtk.WindowType.TOPLEVEL)
        self.view = Gtk.TextView()
        self.view.set_wrap_mode(Gtk.WrapMode.WORD)
        self.view.set_editable(False)

        self.buffer = self.view.get_buffer()
        self.scrolledwindow = Gtk.ScrolledWindow()
        self.scrolledwindow.set_hexpand(True)
        self.scrolledwindow.set_vexpand(True)
        self.window.add(self.scrolledwindow)
        self.window.set_size_request(640, 480)

        self.scrolledwindow.add(self.view)
        self.window.show_all()

    def addLogEntry(self, message):
        end_iter = self.buffer.get_end_iter()
        self.buffer.insert(end_iter, self.createEntryFrom(message) + self.br)
