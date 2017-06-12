import importlib
import pkgutil

from pkg_resources import get_distribution, DistributionNotFound


def get_package_version():
    """Get package version

    Returns:
         str: Installed package version, or 0.0.0.dev if not fully installed
    """
    try:
        return get_distribution(__name__.split('.')[0]).version
    except DistributionNotFound:
        return '0.0.0.dev'


def get_file_extension(filepath):
    """Return full file extension from filepath"""
    filename = filepath.split('/')[-1]

    return filename[filename.index('.'):]


def get_full_qualname(cls):
    """Return fully qualified class name"""
    return cls.__module__ + '.' + cls.__name__


def get_recursive_subclasses(cls):
    """Return list of all subclasses for a class, including subclasses of direct subclasses"""
    return cls.__subclasses__() + [g for s in cls.__subclasses__() for g in get_recursive_subclasses(s)]


def import_submodules(package):
    """Return list of imported module instances from beneath root_package"""

    if isinstance(package, str):
        package = importlib.import_module(package)

    results = {}

    if hasattr(package, '__path__'):
        for _, name, is_pkg in pkgutil.walk_packages(package.__path__):
            full_name = package.__name__ + '.' + name
            try:
                results[full_name] = importlib.import_module(full_name)

                if is_pkg:
                    results.update(import_submodules(full_name))
            except ImportError:
                # Ignore import failures for now; Quickest fix to support contrib serializers as extras with just deps
                continue

    return results
