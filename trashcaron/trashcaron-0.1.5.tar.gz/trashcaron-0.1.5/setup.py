from distutils.core import setup
from setuptools import find_packages

setup(
    name="trashcaron",
    version="0.1.5",
    author="eayin2",
    author_email="eayin2 at gmail dot com",
    packages=find_packages(),
    url="https://github.com/eayin2/trashcaron",
    description="Trashbin script with btrfs support and automatic trash purge feature.",
    install_requires=[],
    entry_points={
        'console_scripts': [
            'trashcaron = trashcaron.trashcaron:main',
        ]
    }
)
