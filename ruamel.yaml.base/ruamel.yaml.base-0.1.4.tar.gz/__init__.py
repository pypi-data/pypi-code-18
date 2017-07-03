# coding: utf-8

from __future__ import print_function, absolute_import, division, unicode_literals

_package_data = dict(
    full_package_name='ruamel.yaml.base',
    version_info=(0, 1, 4),
    __version__='0.1.4',
    author='Anthon van der Neut',
    author_email='a.van.der.neut@ruamel.eu',
    description='YAMLBase class with saving loading and version support',
    # keywords="",
    entry_points='base=ruamel.yaml.base.__main__:main',
    # entry_points=None,
    license='Copyright Ruamel bvba 2007-2016',
    since=2016,
    # status="α|β|stable",  # the package status on PyPI
    # data_files="",
    universal=True,
    nested=True,
    install_requires=[
        'ruamel.std.pathlib',
        'ruamel.yaml',
    ],
    tox=dict(
        env='23',
        deps=['python-dateutil', 'beautifulsoup4'],
    ),
)

version_info = _package_data['version_info']
__version__ = _package_data['__version__']

#################################

from ruamel.std.pathlib import Path   # NOQA
import ruamel.yaml                    # NOQA


class YAMLBase:
    """
    top level should be a mapping (for version, creating)
    """
    def __init__(self, path=None, verbose=0):
        if not isinstance(path, Path):
            path = Path(path)
        self._path = path
        if not self._create_ok:
            assert self._path.exists()
        self._verbose = verbose
        self._data = None
        self._last_read = None
        self._changed = False

    @property
    def data(self):
        if self._changed:  # if changed don't re-read
            return self._data
        if not self._last_read or self._last_read < self._path.stat().st_mtime:
            if self._verbose > 0:
                print('metadata {}reading {}'.format('re' if self._data else '', self._path))
            self._data = None
        if self._data is None:
            try:
                with self._path.open() as fp:
                    self._data = ruamel.yaml.main.round_trip_load(fp, preserve_quotes=True)
            except FileNotFoundError:  # NOQA
                if not self._create_ok:
                    raise
                self._data = ruamel.yaml.comments.CommentedMap()
                self._changed = True
            self.check_version()
            self._last_read = -1 if not self._path.exists() else self._path.stat().st_mtime
        return self._data

    @property
    def fast_data(self):
        import ruamel.yaml.cyaml              # NOQA
        if self._data is not None:
            return self._data
        with self._path.open() as fp:
            return ruamel.yaml.load(fp, Loader=ruamel.yaml.cyaml.CSafeLoader)

    def save(self, force=False, out=None):
        assert self._data is not None
        # should check if file changed on disc and warn
        if not force and not self._changed:
            return
        if out is None:
            with self._path.open('w') as out:
                ruamel.yaml.main.round_trip_dump(self._data, out)
        else:
            ruamel.yaml.main.round_trip_dump(self._data, out)
        self._changed = False
        return True

    def check_version(self):
        """this should be specified by subclass if needed"""
        pass
