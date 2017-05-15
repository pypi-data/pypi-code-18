# From https://www.redhat.com/archives/anaconda-devel-list/2012-June/msg00444.html

"""
Configuration file parser for shell-style config files.
"""

import shlex
from pipes import _safechars
from collections import OrderedDict

def unquote(s):
    return ' '.join(shlex.split(s))
def quote(s):
    for c in s:
        if c not in _safechars:
            break
    else:
        return s
    return '"'+s.replace('"', '\\"')+'"'

class ShellConfig(OrderedDict):
    def __init__(self, filename=None, read_unquote=True, write_quote=True):
        OrderedDict.__init__(self)
        self._lines = list()
        self.read_unquote = read_unquote
        self.write_quote = write_quote

    def set(self, key, val):
        self[str(key)] = str(val)

    # A copy of ConfigParser.read()
    def read(self, filenames):
        if isinstance(filenames, basestring):
            filenames = [filenames]
        read_ok = []
        for filename in filenames:
            try:
                fp = open(filename, 'r')
            except IOError:
                continue
            self._read(fp, filename)
            fp.close()
            read_ok.append(filename)
        return read_ok

    def _read(self, fp, fpname):
        for line in fp:
            self._lines.append(line)
            key, val = self._parseline(line)
            if key:
                self[key] = val

    def _parseline(self, line):
        s = line.strip()
        if '#' in s:
            s = s[:s.find('#')] # remove from comment to EOL
            s = s.strip()       # and any unnecessary whitespace
        key, eq, val = s.partition('=')
        if self.read_unquote:
            val = unquote(val)
        if key != '' and eq == '=':
            return (key, val)
        else:
            return (None, None)

    def __str__(self):
        s = ''
        for line in self._lines:
            key, val = self._parseline(line)
            if key is None:
                s += line
            else:
                val = self[key]
                if self.write_quote:
                    val = quote(val)
                s += key + '=' + val + "\n"
        return s
