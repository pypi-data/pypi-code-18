# -*- coding: utf-8 -*-
"""
Programatic interface to package structure.
"""
import ConfigParser
from cStringIO import StringIO

from dkfileutils.path import Path


class DefaultPackage(object):
    """Default package directory layout (consider this abstract)

       ::
       <parent>
         |
         |--<name>                  # self.wc
              |-- build             # self.build
              |   |-- coverage      # self.build_coverage
              |   |-- docs          # self.build_docs
              |   |-- lintscore     # self.build_lintscore
              |   |-- meta          # self.build_meta
              |   `-- pytest        # self.build_pytest
              |-- <name>            # importable name (self.name, self.source)
              |   |-- js            # self.source_js
              |   |-- less          # self.source_less
              |   |-- static        # self.django_static
              |   `-- templates     # self.django_templates
              |-- docs              # self.docs
              `-- tests             # self.tests
              +-- setup.py          #
              +-- requirements.txt  #

    """
    # pylint: disable=too-many-instance-attributes
    def __init__(self, wc):
        self.wc = Path(wc).abspath()
        self.location = self.wc.parent      # pylint: disable=no-member
        self.name = self.wc.basename().replace('-', '')
        self.docs = self.wc / 'docs'
        self.tests = self.wc / 'tests'
        self.build = self.wc / 'build'
        self.source = self.wc / self.name

        self.source_js = self.wc / self.name / 'js'
        self.source_less = self.wc / self.name / 'less'
        self.django_templates = self.wc / self.name / 'templates'
        self.django_static = self.wc / self.name / 'static'

        self.build_coverage = self.wc / 'build' / 'coverage'
        self.build_docs = self.wc / 'build' / 'docs'
        self.build_lintscore = self.wc / 'build' / 'lintscore'
        self.build_meta = self.wc / 'build' / 'meta'
        self.build_pytest = self.wc / 'build' / 'pytest'

    @property
    def source_dirs(self):
        """Directories containing source.
        """
        return [self.source, self.source_js, self.source_less]

    @property
    def django_dirs(self):
        """Directories containing/holding django specific files.
        """
        return [self.django_static, self.django_templates]

    @property
    def build_dirs(self):
        """Directories containing build artifacts.
        """
        return [self.build, self.build_coverage, self.build_docs,
                self.build_lintscore, self.build_meta, self.build_pytest]

    @property
    def all_dirs(self):
        """Return all package directories.
        """
        return ([self.docs, self.tests]
                + self.source_dirs
                + self.django_dirs
                + self.build_dirs)

    def missing_dirs(self):
        """Return all missing directories.
        """
        return [d for d in self.all_dirs if not d.exists()]

    def make_missing(self):
        """Create all missing directories.
        """
        for d in self.missing_dirs():
            d.makedirs()

    def __repr__(self):
        keylen = max(len(k) for k in self.__dict__.keys())
        # vallen = max(len(k) for k in self.__dict__.values())
        lines = []
        for k, v in sorted(self.__dict__.items()):
            lines.append("%*s %-s" % (keylen, k, v))
        return '\n'.join(lines)

    def write_ini(self, fname, section):
        """Write to ini file.
        """
        cp = ConfigParser.RawConfigParser()
        cp.add_section(section)
        vals = [
            'wc', 'location', 'name', 'docs', 'tests', 'source', 'source_js',
            'source_less', 'build', 'build_coverage', 'build_docs',
            'build_lintscore', 'build_meta', 'build_pytest',
            'django_templates', 'django_static',
        ]
        for val in vals:
            cp.set(section, val, getattr(self, val))
        print fname
        out = StringIO()
        cp.write(out)
        return out.getvalue()


class Package(DefaultPackage):
    """Package layout with possible overrides.
    """
    # pylint: disable=too-many-instance-attributes,too-many-locals,R0903
    def __init__(self, wc,
                 name=None,
                 docs=None,
                 tests=None,
                 build=None,
                 source=None,
                 source_js=None,
                 source_less=None,
                 build_coverage=None,
                 build_docs=None,
                 build_lintscore=None,
                 build_meta=None,
                 build_pytest=None,
                 django_templates=None,
                 django_static=None):
        # pylint: disable=multiple-statements,too-many-arguments,R0912
        super(Package, self).__init__(wc)
        if name: self.name = name
        if docs: self.docs = docs
        if tests: self.tests = tests
        if build:
            self.build = build
            self.build_coverage = self.build / 'coverage'
            self.build_docs = self.build / 'docs'
            self.build_lintscore = self.build / 'lintscore'
            self.build_meta = self.build / 'meta'
            self.build_pytest = self.build / 'pytest'
        if source:
            self.source = source
            self.source_js = self.source / 'js'
            self.source_less = self.source / 'less'
            self.django_templates = self.source / 'templates'
            self.django_static = self.source / 'static'
        if source_js: self.source_js = source_js
        if source_less: self.source_less = source_less
        if build_coverage: self.build_coverage = build_coverage
        if build_docs: self.build_docs = build_docs
        if build_lintscore: self.build_lintscore = build_lintscore
        if build_meta: self.build_meta = build_meta
        if build_pytest: self.build_pytest = build_pytest
        if django_templates: self.django_templates = django_templates
        if django_static: self.django_static = django_static
