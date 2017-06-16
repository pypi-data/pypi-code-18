"""Plugin for setuptools providing compilation of i18n files."""
import os
from distutils.errors import DistutilsSetupError

from setuptools import Command

__version__ = '0.1.1'


def mkmo(in_file):
    """Compile messages."""
    out_file = '%s.mo' % os.path.splitext(in_file)[0]
    os.system("msgfmt %s -o %s" % (in_file, out_file))


def validate_i18n(dist, attr, value):
    """Validate i18n files."""
    for i18n_file in value:
        if not os.path.isfile(i18n_file):
            raise DistutilsSetupError('Filename {} does not exist.'.format(i18n_file))


class build_i18n(Command):
    """Custom command that compiles messages."""

    user_options = [
        ('build-lib=', 'd', "directory to \"build\" (copy) to"),
        ]

    def initialize_options(self):
        self.build_lib = None

    def finalize_options(self):
        self.set_undefined_options('build', ('build_lib', 'build_lib'))

    def run(self):
        if self.distribution.i18n_files:
            for in_file in self.distribution.i18n_files:
                target = os.path.join(self.build_lib, in_file)
                self.mkpath(os.path.dirname(target))
                self.copy_file(in_file, target)
                mkmo(target)
