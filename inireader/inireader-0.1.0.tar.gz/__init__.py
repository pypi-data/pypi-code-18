# coding: utf-8
# config.py - configuration parsing for Mercurial
#
#  Copyright 2017 Aurélien Campéas <aurelien.campeas@pythonian.fr>
#  Copyright 2009 Matt Mackall <mpm@selenic.com> and others
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.

# NOTE: this is an extraction of mercurial.config and a few
#       supporting bits from mercurial.error and mercurial.util
#       all adapted to work with Python 3 and path objects
from __future__ import absolute_import

import errno
import os
import re
from pathlib import Path

# allow path.read_bytes

def patchpathlib():
    """Pathlib for python 2 does not support .read/write_bytes
    this monkeypatch is pertinent up to python 3.4
    """
    import sys
    v = sys.version_info
    if v.major == 3 and v.minor >= 5:
        return

    import pathlib
    def read_bytes(self):
        with self.open('rb') as f:
            return f.read()

    def write_bytes(self, bytes):
        with self.open('wb') as f:
            f.write(bytes)

    pathlib.Path.read_bytes = read_bytes
    pathlib.Path.write_bytes = write_bytes

patchpathlib()


def expandpath(path):
    return os.path.expanduser(os.path.expandvars(path))


class sortdict(dict):
    '''a simple sorted dictionary'''

    def __init__(self, data=None):
        self._list = []
        if data:
            self.update(data)

    def copy(self):
        return sortdict(self)

    def __setitem__(self, key, val):
        if key in self:
            self._list.remove(key)
        self._list.append(key)
        dict.__setitem__(self, key, val)

    def __iter__(self):
        return self._list.__iter__()

    def update(self, src):
        if isinstance(src, dict):
            src = src.items()
        for k, v in src:
            self[k] = v

    def clear(self):
        dict.clear(self)
        self._list = []

    def items(self):
        return [(k, self[k]) for k in self._list]

    def __delitem__(self, key):
        dict.__delitem__(self, key)
        self._list.remove(key)

    def pop(self, key, *args, **kwargs):
        dict.pop(self, key, *args, **kwargs)
        try:
            self._list.remove(key)
        except ValueError:
            pass

    def keys(self):
        return self._list

    def iterkeys(self):
        return self._list.__iter__()

    def iteritems(self):
        for k in self._list:
            yield k, self[k]

    def insert(self, index, key, val):
        self._list.insert(index, key)
        dict.__setitem__(self, key, val)


class ParseError(Exception):
    """Raised when parsing config files and {rev,file}sets (msg[, pos])"""

    def __init__(self, *args, **kw):
        Exception.__init__(self, *args)
        self.hint = kw.get('hint')


class reader(object):

    def __init__(self, path=None, includepaths=[]):
        self._data = {}
        self._source = {}
        self._unset = []
        self._includepaths = [Path(ip) for ip in includepaths]
        if path:
            self.read(path)

    def copy(self):
        newreader = reader()
        for k in self._data:
            newreader._data[k] = self[k].copy()
        newreader._source = self._source.copy()
        return newreader

    def __contains__(self, section):
        return section in self._data

    def __getitem__(self, section):
        return self._data.get(section, {})

    def __iter__(self):
        for d in self.sections():
            yield d

    def update(self, src):
        for s, n in src._unset:
            if s in self and n in self._data[s]:
                del self._data[s][n]
                del self._source[(s, n)]
        for s in src:
            if s not in self:
                self._data[s] = sortdict()
            self._data[s].update(src._data[s])
        self._source.update(src._source)

    def get(self, section, item, default=None):
        return self._data.get(section, {}).get(item, default)

    def source(self, section, item):
        return self._source.get((section, item), "")

    def sections(self):
        return sorted(self._data.keys())

    def items(self, section):
        return self._data.get(section, {}).items()

    def set(self, section, item, value, source=""):
        if section not in self:
            self._data[section] = sortdict()
        self._data[section][item] = value
        if source:
            self._source[(section, item)] = source

    def parse(self, src, data, sections=None, remap=None, include=None):
        sectionre = re.compile(r'\[([^\[]+)\]')
        itemre = re.compile(r'([^=\s][^=]*?)\s*=\s*(.*\S|)')
        contre = re.compile(r'\s+(\S|\S.*\S)\s*$')
        emptyre = re.compile(r'(;|#|\s*$)')
        commentre = re.compile(r'(;|#)')
        unsetre = re.compile(r'%unset\s+(\S+)')
        includere = re.compile(r'%include\s+(\S|\S.*\S)\s*$')
        section = ""
        item = None
        line = 0
        cont = False

        for l in data.splitlines(True):
            line += 1
            if line == 1 and l.startswith(u'\xef\xbb\xbf'):
                # Someone set us up the BOM
                l = l[3:]
            if cont:
                if commentre.match(l):
                    continue
                m = contre.match(l)
                if m:
                    if sections and section not in sections:
                        continue
                    v = self.get(section, item) + "\n" + m.group(1)
                    self.set(section, item, v, "%s:%d" % (src, line))
                    continue
                item = None
                cont = False
            m = includere.match(l)

            if m and include:
                expanded = expandpath(m.group(1))
                includepaths = [src.parent] + self._includepaths

                for base in includepaths:
                    inc = base.joinpath(expanded).resolve()

                    try:
                        include(inc, remap=remap, sections=sections)
                        break
                    except IOError as inst:
                        if inst.errno != errno.ENOENT:
                            raise ParseError("cannot include %s (%s)"
                                             % (inc, inst.strerror),
                                             "%s:%s" % (src, line))
                continue
            if emptyre.match(l):
                continue
            m = sectionre.match(l)
            if m:
                section = m.group(1)
                if remap:
                    section = remap.get(section, section)
                if section not in self:
                    self._data[section] = sortdict()
                continue
            m = itemre.match(l)
            if m:
                item = m.group(1)
                cont = True
                if sections and section not in sections:
                    continue
                self.set(section, item, m.group(2), "%s:%d" % (src, line))
                continue
            m = unsetre.match(l)
            if m:
                name = m.group(1)
                if sections and section not in sections:
                    continue
                if self.get(section, name) is not None:
                    del self._data[section][name]
                self._unset.append((section, name))
                continue

            raise ParseError(l.rstrip(), ("%s:%s" % (src, line)))

    def read(self, path, sections=None, remap=None):
        self.parse(path, Path(path).read_bytes().decode('utf-8'),
                   sections, remap, self.read)
