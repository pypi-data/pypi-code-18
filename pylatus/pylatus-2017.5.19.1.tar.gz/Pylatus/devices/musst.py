#!/usr/bin/python
# -*- coding: utf-8 -*-

import collections
from PyQt5 import QtCore
import aspic
from auxygen.devices import logger
from ..controller.config import Config


class Musst(QtCore.QObject):
    sigIdle = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.queue = collections.deque()
        self.cmd = None
        self.con = None
        self.timeout1 = 0
        self.timeout2 = 0
        self.callback = None
        self.oldCon = ()
        self.logger = logger.Logger('MUSST')
        self.timerIdle = QtCore.QTimer()
        self.timerCmd = QtCore.QTimer()
        self.connectSignals()

    # noinspection PyUnresolvedReferences
    def connectSignals(self):
        self.timerIdle.setInterval(50)
        self.timerIdle.timeout.connect(lambda: self.runCommand('musst_comm("?STATE")', self.checkIdle))
        self.timerCmd.timeout.connect(self.checkQueue)

    def checkIdle(self, value):
        if value == 'IDLE':
            self.timerIdle.stop()
            self.sigIdle.emit()

    def setConfig(self):
        self.timeout1 = float(Config.MusstTimeout1) * 1e6 if Config.MusstTimeout1 else 0
        self.timeout2 = float(Config.MusstTimeout2) * 1e6 if Config.MusstTimeout2 else 0
        if self.oldCon and self.oldCon != (Config.MusstSpec, Config.MusstFirmware):
            self.connectToSpec()

    def connectToSpec(self):
        if Config.MusstSpec and Config.MusstFirmware:
            try:
                host, port = Config.MusstSpec.split(':')
            except (IndexError, ValueError):
                self.logger.error('MUSST address is incorrect')
                return
            self.oldCon = Config.MusstSpec, Config.MusstFirmware
            address = host, port
            self.init_musst_commands = (
                # stop current program
                'musst_comm("ABORT")',
                'musst_comm("BTRIG 0")',
                'musst_comm("CLEAR")',
                'musst_comm("HSIZE 0")',
                # set buffer size
                'musst_comm("ESIZE 500000 1")',
                # upload the program
                f'musst_upload_program("musst", "{Config.MusstFirmware}", 1)',
            )
            self.queue.clear()
            self.con = aspic.manager.qonnect(address)
            self.con.sigConnectedToSpec.connect(self.reset)
            self.con.sigError.connect(self.logger.error)
            if self.con.isConnected():
                QtCore.QMetaObject.invokeMethod(self, 'reset', QtCore.Qt.QueuedConnection)
            self.cmd = aspic.Qommand(self.con)
            self.cmd.sigFinished.connect(self.commandFinished)
            self.cmd.sigError.connect(self.logger.error)
            self.timerCmd.start(20)
        else:
            self.timerCmd.stop()
            self.callback = None
            self.cmd = None
            self.con = None

    def commandFinished(self, text):
        if self.callback:
            callback = self.callback
            self.callback = None
            callback(text)

    @QtCore.pyqtSlot(name='reset')
    def reset(self):
        self.logger.info('Musst is connected')
        for musst_command in self.init_musst_commands:
            self.runCommand(musst_command)

    def checkQueue(self):
        if self.callback:
            return
        if self.queue:
            cmd, self.callback = self.queue.popleft()
            self.cmd.run(cmd)

    def setVar(self, var, value):
        self.runCommand(f'musst_comm("VAR {var} {int(value):d}")')

    def runScan(self, nframes, exptime, mod1, mod2):
        params = {
            'STARTDELAY': self.timeout2,
            'NPOINTS': nframes,
            'CTIME': exptime * 1e6,
            'INITDELAY': self.timeout2,
            'NPOINTS2': mod1,
            'NPOINTS2A': mod2,
        }
        for var in params:
            self.setVar(var, params[var])
        self.runCommand('musst_comm("RUN SCAN")')
        self.timerIdle.start()

    def abort(self):
        self.runCommand('musst_comm("ABORT")', lambda _: self.logger.warn(f'Musst has been stopped! Message: {_}'))
        self.closeShutter()

    def openShutter(self):
        self.runCommand('musst_comm("RUN SHUTTER_OPEN")', lambda _: self.logger.info(f'Shutter is open: {_}'))

    def closeShutter(self):
        self.runCommand('musst_comm("RUN SHUTTER_CLOSE")', lambda _: self.logger.info(f'Shutter is closed: {_}'))

    def trigChannel(self, chan, trtime=0.1):
        self.runCommand(f'trigch {chan:d} {trtime:.2f}',
                        lambda _: self.logger.info(f'Musst triggers channel {chan:d} for {trtime:.2f} seconds: {_}'))

    def runCommand(self, command, callback=None):
        if self.isConnected():
            self.queue.append((command, callback))

    def isConnected(self):
        return self.cmd and self.con and self.con.isConnected()
