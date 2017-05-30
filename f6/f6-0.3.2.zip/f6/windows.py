import os
import ctypes
import subprocess
import csv
import itertools

import win32api
import win32gui
import win32con
import win32process

def task_windows():

    def f(hwnd, _):
        if not win32gui.IsWindowVisible(hwnd):
            return
        if win32gui.GetParent(hwnd):
            return
        if win32gui.GetWindow(hwnd, win32con.GW_OWNER):
            return
        title = win32gui.GetWindowText(hwnd)
        if not title:
            return
        windows.append((hwnd, title))

    windows = []
    win32gui.EnumWindows(f, None)
    return windows[:-1]

def vk2name(vk, vks={}):
    if not vks:
        vks.update({
            getattr(win32con, t): t
            for t in dir(win32con) if t.startswith('VK')
        })
    try:
        return vks[vk]
    except KeyError:
        return chr(vk)

class Process(object):

    def __init__(self, **kwds):
        self.__dict__.update(kwds)
        self.name = self.Name
        self.pid = int(self.ProcessId)
        self.cmd = self.CommandLine
        self.path = self.ExecutablePath

    def kill(self, force=True, child=True):
        args = ''
        if force:
            args += ' /f'
        if child:
            args += ' /t'
        os.system('taskkill {} /pid {}'.format(args, self.pid))

    def __repr__(self):
        return 'Process(name="{}", pid={})'.format(self.name, self.pid)

def processes(pred):
    s = subprocess.check_output(
        'wmic /node:localhost process get /format:list')
    lines = s.replace('\r', '').split('\n')
    items = [list(g) for k, g in itertools.groupby(lines, bool) if k]
    ps = []
    for fields in items:
        d = {}
        for field in fields:
            i = field.index('=')
            key = field[:i]
            val = field[i+1:]
            d[key] = val
        ps.append(Process(**d))
    return filter(pred, ps)

ProcessInfoColumns = [
    'CSName',
    'CommandLine',
    'Description',
    'ExecutablePath',
    'ExecutionState',
    'Handle',
    'HandleCount',
    'InstallDate',
    'KernelModeTime',
    'MaximumWorkingSetSize',
    'MinimumWorkingSetSize',
    'Name',
    'OSName',
    'OtherOperationCount',
    'OtherTransferCount',
    'PageFaults',
    'PageFileUsage',
    'ParentProcessId',
    'PeakPageFileUsage',
    'PeakVirtualSize',
    'PeakWorkingSetSize',
    'Priority',
    'PrivatePageCount',
    'ProcessId',
    'QuotaNonPagedPoolUsage',
    'QuotaPagedPoolUsage',
    'QuotaPeakNonPagedPoolUsage',
    'QuotaPeakPagedPoolUsage',
    'ReadOperationCount',
    'ReadTransferCount',
    'SessionId',
    'Status',
    'TerminationDate',
    'ThreadCount',
    'UserModeTime',
    'VirtualSize',
    'WindowsVersion',
    'WorkingSetSize',
    'WriteOperationCount',
    'WriteTransferCount',
]

if __name__ == '__main__':
    ps = processes(lambda p: 'chrome' in p.name)
    from each import each
    each(ps).kill()
