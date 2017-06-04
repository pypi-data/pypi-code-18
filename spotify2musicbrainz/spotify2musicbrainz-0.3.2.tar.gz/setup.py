"""Setup module for Spotify2MusicBrainz."""

from setuptools import setup

def long_description():
    "Function to parse the README file into the long_description field."
    from os import path
    rootdir = path.realpath(path.dirname(__file__))
    with open(path.join(rootdir, "README.rst")) as readme:
        return readme.read()

setup(
    name="spotify2musicbrainz",
    use_scm_version=True,
    description="An aid to add information from Spotify to MusicBrainz.",
    long_description=long_description(),
    url="https://gitlab.com/Freso/spotify2musicbrainz",
    author="Frederik “Freso” S. Olesen",
    author_email="spotify2musicbrainz@freso.dk",
    license="GPLv3+",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Multimedia :: Sound/Audio",
        "Topic :: Utilities",
    ],
    keywords="spotify musicbrainz music metadata data",
    py_modules=["spotify2musicbrainz"],
    setup_requires=['setuptools_scm'],
    install_requires=[
        "musicbrainzngs",  # for interacting with MusicBrainz
        "spotipy",  # for interacting with Spotify
    ],
    entry_points={
        "console_scripts": [
            "spotify2musicbrainz=spotify2musicbrainz:main",
        ],
    },
)
