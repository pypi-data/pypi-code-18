#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2013-2014, NewAE Technology Inc
# All rights reserved.
#
# Author: Colin O'Flynn
#
# Find this and more at newae.com - this file is part of the chipwhisperer
# project, http://www.assembla.com/spaces/chipwhisperer
#
#    This file is part of chipwhisperer.
#
#    chipwhisperer is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    chipwhisperer is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with chipwhisperer.  If not, see <http://www.gnu.org/licenses/>.
#=================================================
import logging

from chipwhisperer.common.api.autoscript import AutoScript
from chipwhisperer.common.utils.pluginmanager import Plugin
from chipwhisperer.common.utils.tracesource import TraceSource, ActiveTraceObserver
from chipwhisperer.common.utils.parameter import setupSetParam


class PreprocessingBase(TraceSource, ActiveTraceObserver, AutoScript, Plugin):
    """
    Base Class for all preprocessing modules
    Derivable Classes work like this:
        - updateScript is called to update the scripts based on the current status of the object
        - the other methods are used by the API to apply the preprocessing filtering
    """
    _name = "None"

    def __init__(self, traceSource=None):
        self.enabled = False
        ActiveTraceObserver.__init__(self)
        TraceSource.__init__(self, self.getName())
        AutoScript.__init__(self)
        self.setTraceSource(traceSource, blockSignal=True)
        if traceSource:
            traceSource.sigTracesChanged.connect(self.sigTracesChanged.emit)  # Forwards the traceChanged signal to the next observer in the chain
        self.getParams().addChildren([
                 {'name':'Enabled', 'key':'enabled', 'type':'bool', 'default':self.getEnabled(), 'get':self.getEnabled, 'set':self.setEnabled}
        ])
        self.findParam('input').hide()

        self.register()
        if __debug__: logging.debug('Created: ' + str(self))

        #Old attribute dict
        self._attrdict = None

    def updateScript(self, _=None):
        self.addFunction("init", "setEnabled", "%s" % self.findParam('enabled').getValue())

    def getEnabled(self):
        """Return if it is enable or not"""
        return self.enabled

    @setupSetParam("Enabled")
    def setEnabled(self, enabled):
        """Turn on/off this preprocessing module"""
        self.enabled = enabled
        self.updateScript()

    def getTrace(self, n):
        """Get trace number n"""
        if self.enabled:
            trace = self._traceSource.getTrace(n)
            # Do your preprocessing here
            return trace
        else:
            return self._traceSource.getTrace(n)

    def getTextin(self, n):
        """Get text-in number n"""
        return self._traceSource.getTextin(n)

    def getTextout(self, n):
        """Get text-out number n"""
        return self._traceSource.getTextout(n)

    def getKnownKey(self, n=None):
        """Get known-key number n"""
        return self._traceSource.getKnownKey(n)

    def getSampleRate(self):
        """Get the Sample Rate"""
        return self._traceSource.getSampleRate()

    def init(self):
        """Do any initialization required once all traces are loaded"""
        pass

    def getSegmentList(self):
        return self._traceSource.getSegmentList()

    def getAuxData(self, n, auxDic):
        return self._traceSource.getAuxData(n, auxDic)

    def getSegment(self, n):
        return self._traceSource.getSegment(n)

    def numTraces(self):
        return self._traceSource.numTraces()

    def numPoints(self):
        return self._traceSource.numPoints()

    def attrSettings(self):
        """Return user-added attributes, used in determining cache settings"""

        if self.__dict__ == self._attrdict:
            return self._attrdict_trimmed

        self._attrdict = self.__dict__.copy()
        attrdict = self.__dict__.copy()

        del attrdict["_attrdict"]
        if hasattr(attrdict, "_attrdict_trimmed"): del attrdict["_attrdict_trimmed"]
        del attrdict["runScriptFunction"]
        del attrdict["sigTracesChanged"]
        del attrdict["_smartstatements"]
        del attrdict["_traceSource"]
        attrdict["params"] = str(attrdict["params"])
        del attrdict["scriptsUpdated"]
        del attrdict["updateDelayTimer"]

        self._attrdict_trimmed = attrdict
        return self._attrdict_trimmed

    def __del__(self):
        if __debug__: logging.debug('Deleted: ' + str(self))