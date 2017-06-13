# -*- coding: utf-8 -*-
import django_rq_dashboard
from setuptools import find_packages, setup

setup(
    name='django-rq-dashboard',
    version=django_rq_dashboard.__version__,
    author='Bruno Renié',
    author_email='bruno@renie.fr',
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/brutasse/django-rq-dashboard',
    license='BSD licence, see LICENCE file',
    description='A dashboard for managing RQ in the Django admin',
    long_description=open('README.rst').read(),
    install_requires=[
        'pytz',
        'rq',
        'Django>=1.5',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    zip_safe=False,
)
