# -*- coding: utf-8 -*-
import os
from setuptools import find_packages
from setuptools import setup

try:
    from pypandoc import convert
    def read_md(f):
        return convert(f, 'rst')
except ImportError:
    def read_md(f):
        return open(f, 'r').read()


from pypackt.settings import PROJECT_DESC
from pypackt.settings import PROJECT_URL

README_PATH = os.path.join(
    os.path.abspath(os.path.dirname(__file__)), 'README.md'
)


setup(
    name='pypackt',
    version='1.0.0',
    description=PROJECT_DESC,
    long_description=read_md(README_PATH),
    url=PROJECT_URL,
    author='Krzysztof Chomski',
    author_email='krzysztof.chomski@gmail.com',
    license='MIT',
    keywords=['ebooks', 'learning', 'education'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Education',
    ],
    packages=find_packages(),
    install_requires=['python-crontab', 'requests', 'scrapy'],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'pypackt=pypackt.run:main',
        ],
    },
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'pytest-mock']
)
