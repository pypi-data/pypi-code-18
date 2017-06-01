#!/usr/bin/env python
#
#
# 8-Bit Breadboard Emulator
#
# https://eartoearoak.com/ebbbe
#
# Copyright 2017 Al Brown
#
# An emulation of of Ben Eater's 8-bit breadboard computer (https://eater.net/8bit/)
#
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as published by
# the Free Software Foundation
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from PySide.QtCore import Slot, Signal
from PySide.QtGui import QWidget
from ebbbe.view.constants import Colour
from ebbbe.view.ui import load_ui
from ebbbe.view.widget_led import WidgetLed
from ebbbe.view.widget_led_bank import WidgetLedBank

from ebbbe.view.widget_dip import WidgetDip


class WidgetMar(QWidget):
    signalSet = Signal(bool, int)

    def __init__(self, parent):
        QWidget.__init__(self, parent)

        self.customWidgets = {'WidgetLedBank': WidgetLedBank,
                              'WidgetDip': WidgetDip,
                              'WidgetLed': WidgetLed}

        load_ui(self, 'widget_mar.ui')

        self._ledRun.set_colour(Colour.GREEN)
        self._ledRun.light(True)
        self._ledSet.set_colour(Colour.RED)
        self._widgetLeds.set_led_count(4, Colour.YELLOW)
        self._widgetDip.set_dip_count(4)
        self._widgetDip.enable(False)
        self._widgetDip.signalChanged.connect(self.__on_changed)

    def __on_changed(self, value):
        checked = self._buttonSet.isChecked()
        self.signalSet.emit(checked, value)

    @Slot(bool)
    def on__buttonSet_clicked(self, checked):
        self._ledRun.light(not checked)
        self._ledSet.light(checked)
        self._widgetDip.enable(checked)

        value = self._widgetDip.get()
        self.signalSet.emit(checked, value)

    def set(self, value):
        self._widgetLeds.set(value)

    def reset(self):
        self._buttonSet.setChecked(False)
        self.on__buttonSet_clicked(False)
