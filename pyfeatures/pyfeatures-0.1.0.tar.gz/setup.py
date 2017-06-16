
from distutils.core import setup

setup(
    name='pyfeatures',
    packages=['pyfeatures', 'pyfeatures.storage'],
    version='0.1.0',
    description='Python feature flagging. Similar to Rollout.',
    author='Abram C. Isola',
    author_email='abram@isola.mn',
    url='https://github.com/aisola/pyfeatures',
    download_url="https://github.com/aisola/pyfeatures/archive/v0.1.0.tar.gz",
    keywords=['feature', 'features', 'rollout', 'tagging', 'releases', 'flagging', 'startups'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
    ],
)
