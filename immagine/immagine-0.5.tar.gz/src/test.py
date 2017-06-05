#!/usr/bin/env python

''' A framed toolbar that disappears when the pointer isn't moving
    or hovering in the toolbar.

    A response to the question at
    http://stackoverflow.com/questions/26272684/how-can-i-show-hide-toolbar-depending-on-mouse-movements-and-mouse-position-insi

    Written by PM 2Ring 2014.10.09
'''

#import pygtk
#pygtk.require('2.0')
import gtk
#import gobject

#if gtk.pygtk_version < (2, 4, 0):
#    print 'pygtk 2.4 or better required, aborting.'
#    exit(1)


from toolbar_window import AutoHideWindow


class ToolbarDemo(object):
    def button_cb(self, widget, data=None):
        print("Button '%s' clicked" % data)
        return True

    def move_toolbar(self, widget, event):
        self.toolbar_win.begin_move_drag(event.button, int(event.x_root),
                                         int(event.y_root), event.time)

    def motion_notify_cb(self, widget, event):
        self.toolbar_win.show_with_auto_hide()
        return True

    def eventbox_cb(self, widget, event):
        self.toolbar_win.show_with_auto_hide()
        return True

    def quit(self, widget):
        gtk.main_quit()

    def __init__(self):
        self.toolbar_win = tb = AutoHideWindow()

        self.window = win = gtk.Window(gtk.WINDOW_TOPLEVEL)
        width = gtk.gdk.screen_width() // 2
        height = gtk.gdk.screen_height() // 5
        win.set_size_request(width, height)
        win.set_title("Magic Toolbar demo")
        win.set_border_width(10)

        win.connect("destroy", self.quit)
        #self.motion_handler = win.connect("motion_notify_event", self.motion_notify_cb)
        win.connect("motion_notify_event", self.motion_notify_cb)
        win.add_events(gtk.gdk.POINTER_MOTION_MASK |
            gtk.gdk.POINTER_MOTION_HINT_MASK)

        box = gtk.VBox()
        box.show()
        win.add(box)

        #An EventBox to capture events inside Frame,
        # i.e., for the Toolbar and its child widgets.
        ebox = gtk.EventBox()
        ebox.show()
        ebox.set_above_child(True)
        ebox.connect("enter_notify_event", self.eventbox_cb)
        ebox.connect("leave_notify_event", self.eventbox_cb)
        box.pack_start(ebox, expand=False)

        self.frame = frame = gtk.Frame()
        frame.show()
        ebox.add(frame)

        toolbar = gtk.Toolbar()
        toolbar.set_style(gtk.TOOLBAR_TEXT)
        toolbar.set_show_arrow(False)

        movebut = gtk.Button('Move')
        movebut.connect('button-press-event', self.move_toolbar)

        toolbar_hbox = gtk.HBox(homogeneous=False, spacing=0)
        toolbar_hbox.pack_start(toolbar, expand=False, fill=False)
        toolbar_hbox.pack_end(movebut, expand=False, fill=False)

        #toolbar.set_border_width(5)
        self.toolbar_win.add(toolbar_hbox)

        def make_toolbutton(text, data):
            button = gtk.ToolButton(None, label=text)
            button.set_expand(True)
            button.connect('clicked', self.button_cb)
            button.show_all()
            return button

        def make_toolsep():
            sep = gtk.SeparatorToolItem()
            sep.set_expand(True)
            #sep.set_draw(False)
            sep.show()
            return sep

        for i in xrange(5):
            button = make_toolbutton('ToolButton{}'.format(i), i)
            toolbar.insert(button, -1)
            #toolbar.insert(make_toolsep(), -1)

        for i in xrange(1, 9, 2):
            toolbar.insert(make_toolsep(), i)

        button = gtk.Button('_Quit')
        button.show()
        box.pack_end(button, False)
        button.connect("clicked", self.quit)

        win.show_all()
        frame.unmap()


def main():
    ToolbarDemo()
    gtk.main()


if __name__ == "__main__":
    main()
