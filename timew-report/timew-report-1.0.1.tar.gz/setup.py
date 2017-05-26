from setuptools import setup

config = {
    'name': 'timew-report',
    'version': '1.0.1',
    'description': 'An interface for TimeWarrior report data',
    'long_description': '\n' + open('README.md').read(),
    'url': 'https://github.com/lauft/timew-report.git',
    'author': 'Thomas Lauf',
    'author_email': 'Thomas.Lauf@tngtech.com',
    'license': 'MIT License',
    'classifiers': [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Topic :: Utilities',
    ],
    'keywords': 'timewarrior taskwarrior time-tracking',
    'packages': ['timewreport'],
    'install_requires': ['python-dateutil'],
}

setup(**config)
