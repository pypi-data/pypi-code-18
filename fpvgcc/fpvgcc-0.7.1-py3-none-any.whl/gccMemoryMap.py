
# Copyright (C) 2015 Quazar Technologies Pvt. Ltd.
#               2015 Chintalagiri Shashank
#
# This file is part of fpv-gcc.
#
# fpv-gcc is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# fpv-gcc is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with fpv-gcc.  If not, see <http://www.gnu.org/licenses/>.


import logging
from .ntreeSize import SizeNTree, SizeNTreeNode


class LinkAliases(object):
    def __init__(self):
        self._aliases = {}

    def register_alias(self, target, alias):
        if alias in self._aliases.keys():
            if target != self._aliases[alias]:
                logging.warning("Alias Collision : {0} :: {1} ; {2}"
                                "".format(alias, target, self._aliases[alias]))
        else:
            self._aliases[alias] = target

    def encode(self, name):
        for key in self._aliases.keys():
            if name.startswith(key):
                # if alias.startswith(linkermap_section.gident):
                # alias = alias[len(linkermap_section.gident):]
                return self._aliases[key] + name
        return name

    def __repr__(self):
        return '\n'.join(["{0:>38} -> {1:<38}".format(a, t)
                          for (a, t) in sorted(self._aliases.items(),
                                               key=lambda x: x[1])])


class GCCMemoryMapNode(SizeNTreeNode):
    def __init__(self, parent=None, node_t=None,
                 name=None, address=None, size=None, fillsize=None,
                 arfile=None, objfile=None, arfolder=None):
        super(GCCMemoryMapNode, self).__init__(parent, node_t)
        self._leaf_property = '_size'
        self._ident_property = 'name'
        self._size = None
        if name is None:
            if objfile is not None:
                name = objfile
            else:
                name = ""
        self.name = name
        if address is not None:
            self._address = int(address, 16)
        else:
            self._address = None
        if size is not None:
            self._defsize = int(size, 16)
        else:
            self._defsize = None
        self.arfolder = arfolder
        self.arfile = arfile
        self.objfile = objfile
        self._fillsize = None
        self.fillsize = fillsize

    @property
    def address(self):
        if self._address is not None:
            return format(self._address, '#010x')
        else:
            return ""

    @address.setter
    def address(self, value):
        self._address = int(value, 16)

    def contains_address(self, addr):
        if not self.address or self.region in ['DISCARDED', 'UNDEF']:
            return False
        if int(self.address, 0) <= int(addr, 0) < \
                (int(self.address, 0) + self.size):
            return True
        return False

    @property
    def defsize(self):
        return self._defsize

    @defsize.setter
    def defsize(self, value):
        self._defsize = int(value, 16)

    @property
    def osize(self):
        return self._size

    @osize.setter
    def osize(self, value):
        if len(self.children):
            logging.warning("Setting leaf property at a node which "
                            "has children : {0}".format(self.gident))
        newsize = int(value, 16)
        if self._size is not None:
            if newsize != self._size:
                logging.warning(
                    "Overwriting leaf property at node : {0} :: {1} -> {2}"
                    "".format(self.gident, self._size, newsize)
                )
            else:
                logging.warning("Possibly missing leaf node "
                                "with same name : {0}".format(self.gident))
        self._size = newsize

    @property
    def fillsize(self):
        return self._fillsize

    @fillsize.setter
    def fillsize(self, value):
        if value:
            try:
                self._fillsize = int(value, 0)
            except TypeError:
                self._fillsize = int(value)
        else:
            self._fillsize = 0

    def add_child(self, newchild=None, name=None,
                  address=None, size=None, fillsize=0,
                  arfile=None, objfile=None, arfolder=None):
        if newchild is None:
            nchild = GCCMemoryMapNode(name=name, address=None, size=None,
                                      fillsize=0, arfile=None, objfile=None,
                                      arfolder=None)
            newchild = super(GCCMemoryMapNode, self).add_child(nchild)
        else:
            newchild = super(GCCMemoryMapNode, self).add_child(newchild)
        return newchild

    def push_to_leaf(self):
        if not self.objfile:
            logging.warning("No objfile defined. Can't push to leaf : "
                            "{0}".format(self.gident))
            return
        for child in self.children:
            if child.name == self.objfile.replace('.', '_'):
                return
        newleaf = self.add_child(name=self.objfile.replace('.', '_'))
        if self._defsize is not None:
            newleaf.defsize = hex(self._defsize)
        if self._address is not None:
            newleaf.address = hex(self._address)
        if self.fillsize is not None:
            newleaf.fillsize = self.fillsize
        if self.objfile is not None:
            newleaf.objfile = self.objfile
        if self.arfile is not None:
            newleaf.arfile = self.arfile
        if self.arfolder is not None:
            newleaf.arfolder = self.arfolder
        newleaf.osize = hex(self._size)
        return newleaf

    @property
    def leafsize(self):
        # if 'DISCARDED' in self.region:
        # return 0
        # if len(self.children) > 0:
        #     raise AttributeError
        if self.fillsize is not None:
            if self._size is not None:
                return self._size + self.fillsize
            else:
                return self.fillsize
        return self._size

    @leafsize.setter
    def leafsize(self, value):
        raise AttributeError

    @property
    def region(self):
        if not isinstance(self.parent, GCCMemoryMap) and \
                self.parent.region == 'DISCARDED':
            return 'DISCARDED'
        if self._address is None:
            return 'UNDEF'
        # tla = self.get_top_level_ancestor
        # if tla is not None and tla is not self:
        # if tla.region == 'DISCARDED':
        # return 'DISCARDED TLA'
        if self._address == 0:
            return "DISCARDED"
        for region in self.tree.memory_regions:
            if self._address in region:
                return region.name
        raise ValueError(self._address)

    @property
    def is_leaf_property_set(self):
        return self._is_leaf_property_set

    def __repr__(self):
        r = '{0:.<60}{1:<15}{2:>10}{6:>10}{3:>10}    {5:<15}{4}' \
            ''.format(self.gident, self.address or '', self.defsize or '',
                      self.size or '', self.objfile or '', self.region,
                      self._size or '')
        return r


class GCCMemoryMap(SizeNTree):
    node_t = GCCMemoryMapNode

    def __init__(self):
        self.memory_regions = []
        self.aliases = LinkAliases()
        super(GCCMemoryMap, self).__init__()

    @property
    def used_regions(self):
        ur = ['UNDEF']
        for node in self.root.all_nodes():
            if node.region not in ur:
                ur.append(node.region)
        ur.remove('UNDEF')
        ur.remove('DISCARDED')
        return ur

    @property
    def used_objfiles(self):
        of = []
        for node in self.root.all_nodes():
            if node.objfile is None and node.leafsize \
                    and node.region not in ['DISCARDED', 'UNDEF']:
                logging.warning(
                    "Object unaccounted for : {0:<40} {1:<15} {2:>5}"
                    "".format(node.gident, node.region, str(node.leafsize))
                )
                continue
            if node.objfile not in of:
                of.append(node.objfile)
        return of

    def arfile_objfiles(self, arfile):
        of = []
        for node in self.root.all_nodes():
            if node.leafsize and node.region not in ['DISCARDED', 'UNDEF']:
                continue
            if node.arfile == arfile and node.objfile not in of:
                of.append(node.objfile)
        return of

    @property
    def used_arfiles(self):
        af = []
        for node in self.root.all_nodes():
            if node.arfile is None and node.leafsize \
                    and node.region not in ['DISCARDED', 'UNDEF']:
                logging.warning(
                    "Object unaccounted for : {0:<40} {1:<15} {2:>5}"
                    "".format(node.gident, node.region, str(node.leafsize))
                )
                continue
            if node.arfile not in af:
                af.append(node.arfile)
        return af

    @property
    def used_files(self):
        af = []
        of = []
        for node in self.root.all_nodes():
            if node.arfile is None and node.leafsize \
                    and node.region not in ['DISCARDED', 'UNDEF']:
                if node.objfile is None and node.leafsize \
                        and node.region not in ['DISCARDED', 'UNDEF']:
                    logging.warning(
                        "Object unaccounted for : {0:<40} {1:<15} {2:>5}"
                        "".format(node.gident, node.region, str(node.leafsize))
                    )
                    continue
                else:
                    if node.objfile not in of:
                        of.append(node.objfile)
            if node.arfile not in af:
                af.append(node.arfile)
        if None in af:
            af.remove(None)
        if None in of:
            of.remove(None)
        return of, af

    @property
    def used_sections(self):
        sections = [node.gident for node in self.top_level_nodes
                    if node.size > 0 and
                    node.region not in ['DISCARDED', 'UNDEF']]
        sections += [node.gident for node in
                     sum([n.children for n in self.top_level_nodes
                          if n.region == 'UNDEF'], [])
                     if node.region != 'DISCARDED' and node.size > 0]
        return sections

    @property
    def all_symbols(self):
        asym = []
        for node in self.root.all_nodes():
            if node.name not in asym:
                asym.append(node.name)
        return asym

    def symbols_from_file(self, lfile):
        fsym = []
        for node in self.root.all_nodes():
            if node.name not in fsym and lfile in [node.objfile, node.arfile]:
                fsym.append(node.name)
        return fsym

    def get_symbol_fp(self, symbol):
        r = []
        for rgn in self.used_regions:
            r.append(self.get_symbol_fp_rgn(symbol, rgn))
        return r

    def get_symbol_fp_rgn(self, symbol, region):
        rv = 0
        for node in self.root.all_nodes():
            if node.name == symbol:
                if node.region == region:
                    if node.leafsize is not None:
                        rv += node.leafsize
        return rv

    def get_objfile_fp(self, objfile):
        r = []
        for rgn in self.used_regions:
            r.append(self.get_objfile_fp_rgn(objfile, rgn))
        return r

    def get_objfile_fp_rgn(self, objfile, region):
        rv = 0
        for node in self.root.all_nodes():
            if node.objfile == objfile:
                if node.region == region:
                    if node.leafsize is not None:
                        rv += node.leafsize
        return rv

    def get_objfile_fp_secs(self, objfile):
        r = []
        for section in self.used_sections:
            r.append(self.get_objfile_fp_sec(objfile, section))
        return r

    def get_arfile_fp_secs(self, arfile):
        r = []
        for section in self.used_sections:
            r.append(self.get_arfile_fp_sec(arfile, section))
        return r

    def get_objfile_fp_sec(self, objfile, section):
        rv = 0
        for node in self.get_node(section).all_nodes():
            if node.objfile == objfile:
                if node.leafsize is not None:
                    rv += node.leafsize
        return rv

    def get_arfile_fp_sec(self, arfile, section):
        rv = 0
        for node in self.get_node(section).all_nodes():
            if node.arfile == arfile:
                if node.leafsize is not None:
                    rv += node.leafsize
        return rv

    def get_arfile_fp(self, arfile):
        r = []
        for rgn in self.used_regions:
            r.append(self.get_arfile_fp_rgn(arfile, rgn))
        return r

    def get_arfile_fp_rgn(self, arfile, region):
        rv = 0
        for node in self.root.all_nodes():
            if node.arfile == arfile:
                if node.region == region:
                    if node.leafsize is not None:
                        rv += node.leafsize
        return rv


class MemoryRegion(object):
    def __init__(self, name, origin, size, attribs):
        self.name = name
        self.origin = int(origin, 16)
        self.size = int(size, 16)
        self.attribs = attribs

    def __repr__(self):
        r = '{0:.<20}{1:>20}{2:>20}   {3:<20}' \
            ''.format(self.name, format(self.origin, '#010x'),
                      self.size or '', self.attribs)
        return r

    def __contains__(self, value):
        if not isinstance(value, int):
            value = int(value, 16)
        if self.origin <= value < (self.origin + self.size):
            return True
        else:
            return False
