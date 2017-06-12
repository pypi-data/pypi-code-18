"""This module defines the dependency resolver for all java builder."""
import os
import shutil

try:
    from urllib import urlretrieve
except:
    from urllib.request import urlretrieve

class DependencyResolver:
    """Base class for all dependency resolver."""
    def resolve(self, dependency, destination):
        """This method does nothing than to throw an exception because it must be overwritten."""
        raise NotImplementedError('You should instanciate a concrete class!')

class FileDependencyResolver:
    """Resolves the dependencies from a directory."""
    def __init__(self, depdir):
        self.depdir = depdir

    def resolve(self, dependency, destination):
        """Copies the files from the defined `depdir` into the destination directory.
        Args:
            dependency (string): This is the name of the dependency file. It must given relative to
                `depdir`.
            destination (string): This is the directory where the dependencies should be copied to
        """
        shutil.copyfile(os.path.join(self.depdir, dependency),
                        os.path.join(destination, dependency))

class HttpDependencyResolver:
    """Resolves the dependencies from an HTTP server (file download)."""
    def __init__(self, baseurl):
        self.baseurl = baseurl

    def resolve(self, dependency, destionation):
        """Copies the files from the defined `baseurl` into the destination directory.
        Args:
            dependency (string): This is the name of the dependency file. The download url
                is [baseurl]/[dependency].
            destination (string): This is the directory where the dependencies should be copied to
        """
        urlretrieve(self.baseurl + '/' + dependency, os.path.join(destionation, dependency))
