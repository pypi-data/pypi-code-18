#! /usr/bin/env python3

import mvi, setuptools

description = 'Move files by text edit'

long_description = '''\
Organising large amounts of files via the command line is cumbersome. The
standard UNIX `mv` command can rename a file or directory, or move items in
bulk, but the two operations cannot be combined. Furthermore, editing
capabilities on the command line offered by most shells are too limited to
comfortably alter long file or directory names, or add characters from foreign
character sets. Names containing spaces or other special characters should be
quoted or escaped, adding yet another layer of annoyance.

Larry Wall's `rename` complements `mv` with the ability to rename in bulk, but
being based on regular expressions it is suited mostly for file sets that share
a common naming structure. It also requires fluidity in Perl's regular
expression syntax to be useful, which sets a very high bar for entry.

Mvi (which can be seen to be either a contraction of "mv vi" or a more general
abbreviation of "move interactively") aims to simplify bulk renames of files
and directories by opening the directory listing in a text editor, thus
providing a powerful interface for editing destination paths. Names can be
changed by editing the lines in place while preserving order. Upon save and
exit mvi will show a list of scheduled rename operations and ask for
confirmation before performing the changes on disk.'''

setuptools.setup(
  name='mvi',
  version=mvi.__version__,
  description=description,
  long_description=long_description,
  url='https://github.com/gertjanvanzwieten/mvi',
  author='Gertjan van Zwieten',
  author_email = 'git@gjvz.nl',
  license='MIT',
  install_requires=[],
  python_requires='>=3',
  py_modules=['mvi'],
  scripts=['mvi'],
)
