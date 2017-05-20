from distutils.core import setup
from setuptools import find_packages

setup(
    name="rtorrentinotify",
    version="0.0.2",
    author="eayin2",
    author_email="eayin2@gmail.com",
    packages=find_packages(),
    description="Watches a directory for torrents and moves them to the actual rtorrent watch dir",
    install_requires=["helputils", "pyinotify"],
    entry_points={
        'console_scripts': [
            'rtorrentinotify = rtorrentinotify.core:clidoor',
        ]
    }
)
