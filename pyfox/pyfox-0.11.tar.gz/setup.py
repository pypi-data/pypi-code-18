from distutils.core import setup
setup(
    name = 'pyfox',
    packages = ['pyfox'], # this must be the same as the name above
    version = '0.11',
    description = 'Shell for foxtrot',
    author = 'Shubham Sharma',
    author_email = 'shubham.sha12@gmail.com',
    url = 'https://github.com/gabber12/pyfox', # use the URL to the github repo
    download_url = 'https://github.com/gabber12/pyfox/archive/0.1.tar.gz', # I'll explain this in a second
    keywords = ['shell', 'foxtrot', 'cli'], # arbitrary keywords
    classifiers = [],
    entry_points = {
                    'console_scripts': ['foxtrot=pyfox.commands:boot'],
    },
    install_requires=[
              'click',
              'json-logic',
              'requests',
              'prompt_toolkit'
    ]
)
