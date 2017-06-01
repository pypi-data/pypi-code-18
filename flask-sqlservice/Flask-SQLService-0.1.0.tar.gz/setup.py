# -*- coding: utf-8 -*-
from setuptools import setup


setup(
    name='Flask-SQLService',
    version='0.1.0',
    url='https://github.com/robinandeer/flask-sqlservice',
    license='MIT',
    author='Robin Andeer',
    author_email='robin.andeer@gmail.com',
    description='Flask extension for sqlservice',
    py_modules=['flask_sqlservice'],
    install_requires=[
        'sqlservice',
        'Flask',
    ],
    keywords='flask sqlservice sqlalchemy databases',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Framework :: Flask',
        'Programming Language :: Python',
        'License :: OSI Approved :: MIT License',
    ],
)
