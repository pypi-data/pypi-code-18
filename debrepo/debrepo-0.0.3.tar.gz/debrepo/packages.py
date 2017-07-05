# Copyright (c) 2016 Andrew Hills
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Packages are represented by the metadata read from Debian RFC822 paragraphs in
a repository's distribution's component's architecture's :file:`Packages` file.
The :class:`Package` class avoids loading the actual package archives from the
filesystem until absolutely necessary (i.e., reading the change log).
"""


import os
import logging

from debian.arfile import ArError
from debian.debfile import DebFile, DebError
from debian.changelog import ChangeBlock

from debrepo.filters import ExcludeFilter, TransformFilter


class InvalidPackage(Exception):
    pass


class Package(object):
    """
    A single Debian package described by a repository's :file:`Packages` file
    """

    def __init__(self, deb822data, repo=None, filters=[]):
        """
        Given a Debian RFC822 paragraph parsed into a dictionary, and an
        optional set of *filters*, create a representation of a Debian package
        archive suitable for inspecting repository contents.

        Filters of type :class:`~debrepo.filters.TransformFilter` with *what*
        set to :class:`Package` are processed after the dictionary is
        interpreted. The :meth:`~debrepo.filters.TransformFilter.transform`
        method is given the instance of :class:`Package` as its only argument.

        Filters of type :class:`~debrepo.filters.TransformFilter` with *what*
        set to :class:`debian.changelog.ChangeBlock` are processed after each
        changelog block is loaded. The
        :meth:`~debrepo.filters.TransformFilter.transform` method is given the
        instance of :class:`debian.changelog.ChangeBlock` as its only argument.

        Filters of type :class:`~debrepo.filters.ExcludeFilter` with *what* set
        to :class:`debian.changelog.ChangeBlock` are processed while the
        changelog is loaded. If a :class:`~debian.changelog.ChangeBlock`
        matches the exclusion, it is not included in the changelog.

        If *repo* is a path to a :class:`repository <debrepo.repos.Repo>` root,
        the package changelog will be loadable when :meth:`changelog` is
        invoked. See: :meth:`changelog`.
        """

        self.deb822data = deb822data
        try:
            self.name = deb822data['Package']
            self.version = deb822data['Version']
            self.arch = deb822data['Architecture']
            self.filename = deb822data['Filename']
            self.parent = deb822data.get('Source')
        except KeyError as e:
            raise InvalidPackage('Paragraph missing %s key' % e.message)
        # self.repo must be set to an object with a path attribute in order to
        # extract the changelog from the deb archive
        self.repo = repo
        self._changelog = None

        self.change_filters = filter(lambda f: f.what == ChangeBlock, filters)
        package_filters = filter(lambda f: f.what == Package, filters)
        transform_filters = filter(
                lambda f: isinstance(f, TransformFilter), package_filters)
        logging.debug(
                'Processing %d transform filters on package %s',
                len(transform_filters), self.name)
        for f in transform_filters:
            f.transform(self)

    def changelog(self):
        """
        Returns the package's changelog

        If the packagea archive has not yet been loaded and :attr:`repo` is
        defined (see: :class:`Package`), this method will load it and store it
        in the :attr:`_changelog` attribute. To force a changelog reload from
        the package archive, set :attr:`_changelog` to :data:`None`.
        """

        if not self._changelog:
            if not self.repo:
                raise InvalidPackage(
                        'No changelog available without repository information'
                        'to load package file!')
            exclude_filters = filter(
                    lambda f: isinstance(f, ExcludeFilter),
                    self.change_filters)
            transform_filters = filter(
                    lambda f: isinstance(f, TransformFilter),
                    self.change_filters)

            try:
                self._changelog = []
                for block in DebFile(
                        filename=os.path.join(self.repo.path, self.filename)
                        ).changelog():
                    if any([f.exclude(block) for f in exclude_filters]):
                        logging.debug('Excluding changeblock: (filter)')
                        logging.debug(str(block))
                        continue
                    logging.debug(
                            'Processing %d transform filters on changeblock',
                            len(transform_filters))
                    for f in transform_filters:
                        f.transform(block)
                    self._changelog.append(block)
            except (DebError, ArError, IOError) as e:
                raise InvalidPackage(
                        'Invalid deb file %s: %s'
                        % (self.filename, e.message or e.strerror))

        return self._changelog

    def __eq__(self, other):
        return self.name == other.name \
                and self.version == other.version \
                and self.arch == other.arch

    def __str__(self):
        fmt = '%(name)s-%(version)s-%(arch)s'
        if self.parent:
            fmt += ' (%(parent)s)'
        return fmt % self.__dict__
