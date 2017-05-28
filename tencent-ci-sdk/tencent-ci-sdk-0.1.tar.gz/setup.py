#coding=utf=8
from setuptools import setup, find_packages

setup(
    name = 'tencent-ci-sdk',
    version = '0.1',
    keywords = ('tencent', 'qcloud', 'ci', '万象优图', '腾讯云', 'python-sdk'),
    description = '腾讯云万象优图官方 Python SDK 的改进版本',
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
      ],
    license = 'MIT License',
    install_requires = ['requests'],

    author = 'kongkongyzt',
    author_email = 'kongkongyzt@gmail.com',

    packages = find_packages(),
    platforms = 'any',
)
