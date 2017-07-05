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
Debian repositories contain a nested hierarchy. Repositories have
distributions, which have components, which have architectures, which have
:mod:`~debrepo.packages`. The classes below represent this hierarchy. In
general, creating an instance at one level of the hierarchy automatically
causes instances to be created for all the lower levels by reading from the
filesystem.
"""


import os
import logging

from debian.deb822 import Deb822

from debrepo.packages import Package, InvalidPackage
from debrepo.utils import FMT
from debrepo.filters import ExcludeFilter, TransformFilter


class InvalidRepo(Exception):
    pass


class InvalidDist(Exception):
    pass


class InvalidComponent(Exception):
    pass


class InvalidArch(Exception):
    pass


class Repo(object):
    """A subdivision of a :class:`compose <debrepo.composes.Compose>`
    containing :class:`distributions <Dist>`"""

    def __init__(self, path, strict=False, filters=[]):
        """
        Given a *path* to a repository directory, and an optional set of
        *filters*, load a repository and all its subcomponents from the
        filesystem. If *strict* is :data:`True`, any unexpected content will
        cause the loading of the hierarchy to halt and fail with an exception.

        Filters of type :class:`~debrepo.filters.TransformFilter` with *what*
        set to :class:`Repo` are processed after the entire hierarchy, from the
        repository down, is loaded (so, after all other filters have been
        processed). The :meth:`~debrepo.filters.TransformFilter.transform`
        method is given the instance of :class:`Repo` as its only argument.

        Filters of type :class:`~debrepo.filters.ExcludeFilter` with *what* set
        to :class:`Dist` are applied while scanning distribution directories.
        If a directory matches the exclusion, it is not scanned, and a
        :class:`Dist` object for the directory is not created. The omission of
        the distribution does not cause a failure in strict mode.
        """

        self.path = path.rstrip('/')
        if not os.path.isdir(self.path):
            raise InvalidRepo('Not a directory: %s' % self.path)
        self.name = os.path.basename(self.path)

        dist_filters = filter(lambda f: f.what == Dist, filters)
        repo_filters = filter(lambda f: f.what == Repo, filters)
        exclude_filters = filter(
                lambda f: isinstance(f, ExcludeFilter), dist_filters)
        transform_filters = filter(
                lambda f: isinstance(f, TransformFilter), repo_filters)

        self.dists = []
        dists_dir = os.path.join(self.path, 'dists')
        if not os.path.isdir(dists_dir):
            raise InvalidRepo('No dists in %s' % self.path)
        for dist_dir in os.listdir(dists_dir):
            if any([f.exclude(dist_dir) for f in exclude_filters]):
                logging.info('Excluding dist %s (filter)', dist_dir)
                continue
            dist_path = os.path.join(dists_dir, dist_dir)
            if os.path.isdir(dist_path):
                try:
                    self.dists.append(Dist(
                        dist_path, strict=strict, filters=filters))
                except InvalidDist as e:
                    if strict:
                        raise InvalidRepo(
                                'Invalid dist %s: %s' % (dist_dir, e.message))
                    else:
                        logging.info('%s is not a dist, skipping', dist_dir)
                        logging.info('reason: %s', e.message)
                else:
                    logging.debug('Found dist: %s', self.dists[-1])
        self.packages = [pkg for dist in self.dists for pkg in dist.packages]
        for pkg in self.packages:
            pkg.repo = self
        logging.debug(
                'Processing %d transform filters on repo %s',
                len(transform_filters), self.name)
        for f in transform_filters:
            f.transform(self)

    def get_dist(self, dist_name):
        """Select dist object by name"""

        matching_dists = [
                dist for dist in self.dists if dist.name == dist_name]
        if len(matching_dists) > 1:
            raise InvalidDist('Multiple dists matched %s! Help!' % dist_name)
        if not matching_dists:
            return None
        return matching_dists[0]

    def __eq__(self, other):
        return self.name == other.name

    def __str__(self):
        return FMT.format(
                'Repo {name} at {path} ({distct|dist(s)}, {pkgct|package(s)})',
                name=self.name,
                path=self.path,
                distct=len(self.dists),
                pkgct=len(self.packages),
                )


class Dist(object):
    """A subdivision of a :class:`repository <Repo>` containing
    :class:`components <Component>`"""

    def __init__(self, path, strict=False, filters=[]):
        """
        Given a *path* to a distribution directory, and an optional set of
        *filters*, load a distribution and all its subcomponents from the
        filesystem. If *strict* is :data:`True`, any unexpected content will
        cause the loading of the hierarchy to halt and fail with an exception.

        Filters of type :class:`~debrepo.filters.TransformFilter` with *what*
        set to :class:`Dist` are processed after the entire hierarchy, from the
        distribution down, is loaded (so, after all other filters have been
        processed). The :meth:`~debrepo.filters.TransformFilter.transform`
        method is given the instance of :class:`Dist` as its only argument.

        Filters of type :class:`~debrepo.filters.ExcludeFilter` with *what* set
        to :class:`Component` are applied while scanning component directories.
        If a directory matches the exclusion, it is not scanned, and a
        :class:`Component` object for the directory is not created. The
        omission of the component does not cause a failure in strict mode.
        """

        self.path = path.rstrip('/')
        self.path = path.rstrip('/')
        if not os.path.isdir(self.path):
            raise InvalidDist('Not a directory: %s', self.path)
        self.name = os.path.basename(self.path)
        self.release_file = None
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            # Prefer InRelease to Release
            if os.path.isfile(item_path):
                if item == 'InRelease':
                    self.release_file = item_path
                    self.signature_exists = True
                    break
                if item == 'Release':
                    self.release_file = item_path
                    self.signature_exists = os.path.isfile(
                            os.path.join(path, 'Release.gpg'))
        if not self.release_file:
            raise InvalidDist('No release file in %s' % path)
        try:
            self.release = Deb822(open(self.release_file))
        except Exception as e:
            raise InvalidDist(
                    'Failed to parse release file: %s: %s'
                    % (self.release_file, e.message))
        self.arches = self.release['Architectures'].split()

        component_filters = filter(lambda f: f.what == Component, filters)
        dist_filters = filter(lambda f: f.what == Dist, filters)
        exclude_filters = filter(
                lambda f: isinstance(f, ExcludeFilter), component_filters)
        transform_filters = filter(
                lambda f: isinstance(f, TransformFilter), dist_filters)

        self.components = []
        for component in self.release['Components'].split():
            if any([f.exclude(component) for f in exclude_filters]):
                logging.info('Excluding component %s (filter)', component)
                continue
            component_path = os.path.join(self.path, component)
            try:
                self.components.append(Component(
                    component_path, self.arches, strict=strict,
                    filters=filters))
            except InvalidComponent as e:
                raise InvalidDist(
                        'Invalid component %s: %s' % (component, e.message))
            else:
                logging.debug('Registered component: %s', self.components[-1])
        self.packages = [
                pkg for component in self.components
                for pkg in component.packages]
        logging.debug(
                'Processing %d transform filters on dist %s',
                len(transform_filters), self.name)
        for f in transform_filters:
            f.transform(self)

    def get_component(self, component_name):
        """Select component object by name"""

        matching_components = [
                component for component in self.components
                if component.name == component_name]
        if len(matching_components) > 1:
            raise InvalidComponent(
                    'Multiple components matched %s! Help!' % component_name)
        if not matching_components:
            return None
        return matching_components[0]

    def __eq__(self, other):
        return self.name == other.name

    def __str__(self):
        return FMT.format(
                'Dist {name} at {path} ({componentct|component(s)}, ' +
                '{pkgct|package(s)})',
                name=self.name,
                path=self.path,
                componentct=len(self.components),
                pkgct=len(self.packages),
                )


class Component(object):
    """A subdivision of a :class:`distribution <Dist>` containing
    :class:`architectures <Arch>`"""

    def __init__(self, path, arches, strict=False, filters=[]):
        """
        Given a *path* to a component directory, a list of valid *arches*, and
        an optional set of *filters*, load a component and all its
        subcomponents from the filesystem. If *strict* is :data:`True`, any
        unexpected content will cause the loading of the hierarchy to halt and
        fail with an exception.

        Filters of type :class:`~debrepo.filters.TransformFilter` with *what*
        set to :class:`Component` are processed after the entire hierarchy,
        from the component down, is loaded (so, after all other filters have
        been processed). The :meth:`debrepo.filters.TransformFilter.transform`
        method is given the instance of :class:`Component` as its only
        argument.

        Filters of type :class:`~debrepo.filters.ExcludeFilter` with *what* set
        to :class:`Arch` are applied while scanning architecture directories.
        If a directory matches the exclusion, it is not scanned, and an
        :class:`Arch` object for the directory is not created. The omission of
        the architecture does not cause a failure in strict mode.
        """

        self.path = path.rstrip('/')
        self.path = path
        if not os.path.isdir(self.path):
            raise InvalidComponent('Not a directory: %s' % self.path)
        self.name = os.path.basename(self.path)
        if not arches:
            raise InvalidComponent('No arches')

        arch_filters = filter(lambda f: f.what == Arch, filters)
        component_filters = filter(lambda f: f.what == Component, filters)
        exclude_filters = filter(
                lambda f: isinstance(f, ExcludeFilter), arch_filters)
        transform_filters = filter(
                lambda f: isinstance(f, TransformFilter), component_filters)

        self.arches = []
        for arch in arches:
            if any([f.exclude(arch) for f in exclude_filters]):
                logging.info('Excluding arch %s (filter)', arch)
                continue
            arch_path = os.path.join(self.path, 'binary-%s' % arch)
            try:
                self.arches.append(Arch(
                    arch_path, strict=strict, filters=filters))
            except InvalidArch as e:
                raise InvalidComponent(
                        'Invalid arch %s: %s' % (arch, e.message))
            else:
                logging.debug('Registered arch: %s', self.arches[-1])
        self.packages = [pkg for arch in self.arches for pkg in arch.packages]
        logging.debug(
                'Processing %d transform filters on component %s',
                len(transform_filters), self.name)
        for f in transform_filters:
            f.transform(self)

    def get_arch(self, arch_name):
        """Select arch object by name"""

        matching_arches = [
                arch for arch in self.arches if arch.name == arch_name]
        if len(matching_arches) > 1:
            raise InvalidArch('Multiple arches matched %s! Help!' % arch_name)
        if not matching_arches:
            return None
        return matching_arches[0]

    def __eq__(self, other):
        return self.name == other.name

    def __str__(self):
        return FMT.format(
                'Component {name} at {path} ({archct|arch(es)}, ' +
                '{pkgct|package(s)})',
                name=self.name,
                path=self.path,
                archct=len(self.arches),
                pkgct=len(self.packages),
                )


class Arch(object):
    """A subdivision of :class:`component <Component>` containing
    :class:`packages <debrepo.packages.Package>`."""

    def __init__(self, path, strict=False, filters=[]):
        """
        Given a *path* to an architecture directory, and an optional set of
        *filters*, load an architecture and all its subcomponents from the
        filesystem. If *strict* is :data:`True`, any unexpected content will
        cause the loading of the hierarchy to halt and fail with an exception.

        Filters of type :class:`~debrepo.filters.TransformFilter` with *what*
        set to :class:`Arch` are processed after the entire hierarchy, from the
        architecture down, is loaded (so, after all other filters have been
        processed). The :meth:`~debrepo.filters.TransformFilter.transform`
        method is given the instance of :class:`Arch` as its only argument.

        Filters of type :class:`~debrepo.filters.ExcludeFilter` with *what* set
        to :class:`~debrepo.packages.Package` are applied while reading the
        :file:`Packages` file. If an entry matches the exclusion, it is not
        scanned, and a :class:`~debrepo.packages.Package` instance for the
        entry is not created.
        """

        self.path = path.rstrip('/')
        self.path = path.rstrip('/')
        if not os.path.isdir(self.path):
            raise InvalidArch('Not a directory: %s' % self.path)
        self.name = os.path.basename(self.path)
        if self.name.startswith('binary-'):
            self.name = self.name[7:]
        elif strict:
            raise InvalidArch('Arch directory name must begin with "binary-"')
        self.release_file = os.path.join(self.path, 'Release')
        try:
            self.release = Deb822(open(self.release_file))
        except Exception as e:
            release_message = 'Failed to parse release file: %s: %s' \
                    % (self.release_file, e.message)
            if strict:
                raise InvalidArch(release_message)
            else:
                self.release = None
                logging.warning(release_message)
        if self.release and self.release['Architecture'] != self.name:
            arch_mismatch_message = \
                    'Release arch "%s" does not match expected arch "%s"' \
                    % (self.release['Architecture'], self.name)
            if strict:
                raise InvalidArch(arch_mismatch_message)
            else:
                logging.warning(arch_mismatch_message)
        self.packages_file = os.path.join(self.path, 'Packages')

        package_filters = filter(lambda f: f.what == Package, filters)
        arch_filters = filter(lambda f: f.what == Arch, filters)
        exclude_filters = filter(
                lambda f: isinstance(f, ExcludeFilter), package_filters)
        transform_filters = filter(
                lambda f: isinstance(f, TransformFilter), arch_filters)

        self.packages = []
        try:
            for paragraph in Deb822.iter_paragraphs(open(self.packages_file)):
                if any([
                        f.exclude(paragraph['Package'])
                        for f in exclude_filters]):
                    logging.info(
                            'Excluding package %s (filter)',
                            paragraph['Package'])
                    continue
                new_package = Package(
                        paragraph,
                        filters=filter(lambda f: f.what != Package, filters))
                logging.debug('Parsed package: %s', new_package)
                if new_package.arch != self.name \
                        and new_package.arch != 'all':
                    raise InvalidPackage(
                            'Package arch "%s" does not match expected arch '
                            '"%s"' % (new_package.arch, self.name))
                self.packages.append(new_package)
        except Exception as e:
            if type(e) == InvalidPackage:
                raise InvalidArch(
                        'Arch contains package from another arch: %s'
                        % e.message)
            raise InvalidArch(
                    'Failed to parse packages file: %s: %s'
                    % (self.packages_file, e.message))
        logging.debug(
                'Processing %d transform filters on arch %s',
                len(transform_filters), self.name)
        for f in transform_filters:
            f.transform(self)

    def get_package(self, package_name):
        """Select package object by name"""

        matching_packages = [
                pkg for pkg in self.packages if pkg.name == package_name]
        if len(matching_packages) > 1:
            raise InvalidPackage(
                    'Multiple packages matched %s! Help!' % package_name)
        if not matching_packages:
            return None
        return matching_packages[0]

    def __eq__(self, other):
        return self.name == other.name

    def __str__(self):
        return FMT.format(
                'Arch {name} at {path} ({pkgct|package(s)})',
                name=self.name,
                path=self.path,
                pkgct=len(self.packages),
                )
