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
A *compose* is a collection of :mod:`repositories <debrepo.repos>`, generally
created as the output of product content generation. Because Debian
repositories exist as a nested hierarchy on a filesystem, and because composes
exist as directories containing repository directories, a compose may be
thought of as an element in the same hierarchy, at the top. Creating a
:class:`Compose` instance, in the same way as each of the levels of object in a
repository, will cause the entire hierarchy to be recursively read from the
filesystem.
"""

import os
import os.path
import logging

from debrepo.repos import Repo, InvalidRepo
from debrepo.utils import FMT
from debrepo.filters import ExcludeFilter, TransformFilter


class InvalidCompose(Exception):
    pass


class Compose(object):
    """A collection of repositories"""

    def __init__(self, path, strict=False, filters=[]):
        """
        Given a *path* to a compose directory, and an optional set of
        *filters*, load a compose and all its subcomponents from the
        filesystem. If *strict* is :data:`True`, any unexpected content will
        cause the loading of the hierarchy to halt and fail with an exception.

        Filters of type :py:class:`~debrepo.filters.TransformFilter` with
        *what* set to :py:class:`Compose` are processed after the entire
        hierarchy is loaded (so, after all other filters have been processed).
        The :py:meth:`~debrepo.filters.TransformFilter.transform` method is
        given the instance of :py:class:`Compose` as its only argument.

        Filters of type :py:class:`~debrepo.filters.ExcludeFilter` with *what*
        set to :py:class:`~debrepo.repos.Repo` are applied while scanning
        repository directories. If a directory matches the exclusion, it is not
        scanned, and a :py:class:`~debrepo.repos.Repo` object for the directory
        is not created. The omission of the repository does not cause a failure
        in strict mode.
        """

        self.path = path.rstrip('/')
        if not os.path.isdir(self.path):
            raise InvalidCompose('Not a directory: %s' % self.path)
        self.name = os.path.basename(self.path)

        repo_filters = filter(lambda f: f.what == Repo, filters)
        compose_filters = filter(lambda f: f.what == Compose, filters)
        exclude_repos = filter(
                lambda f: isinstance(f, ExcludeFilter), repo_filters)
        transform_filters = filter(
                lambda f: isinstance(f, TransformFilter), compose_filters)

        self.repos = []
        for repo_dir in sorted(os.listdir(self.path)):
            repo_path = os.path.join(self.path, repo_dir)
            if os.path.isdir(repo_path):
                if any([f.exclude(repo_dir) for f in exclude_repos]):
                    logging.info('Excluding repo %s (filter)', repo_dir)
                    continue
                try:
                    self.repos.append(Repo(
                        repo_path, strict=strict, filters=filters))
                except InvalidRepo as e:
                    if strict:
                        raise
                    logging.info('%s is not a repository, skipping', repo_dir)
                    logging.info('reason: %s' % e.message)
                else:
                    logging.debug('Found repository: %s' % self.repos[-1])
        if not self.repos:
            raise InvalidCompose('No repositories in %s' % self.path)
        self.packages = [pkg for repo in self.repos for pkg in repo.packages]
        logging.debug(
                'Processing %d transform filters on compose %s',
                len(transform_filters), self.name)
        for f in transform_filters:
            f.transform(self)

    def get_repo(self, repo_name):
        """Select :py:class:`repository <debrepo.repos.Repo>` object by name"""

        matching_repos = [
                repo for repo in self.repos if repo.name == repo_name]
        if len(matching_repos) > 1:
            raise InvalidRepo('Multiple repos matched %s! Help!' % repo_name)
        if not matching_repos:
            return None
        return matching_repos[0]

    def __eq__(self, other):
        return self.name == other.name

    def __str__(self):
        return FMT.format(
                'Compose at {path} ({repoct|repo(s)}, {pkgct|package(s)})',
                path=self.path,
                repoct=len(self.repos),
                pkgct=len(self.packages),
                )
