import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='drf-spirit',
    version='0.0.2',
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',
    description='A pluggable django forum application build with Django Rest Framework',
    long_description=README,
    url='https://github.com/alaminopu/drf-spirit',
    author='Md. Al-Amin Opu',
    author_email='alamin.opu10@gmail.com',
    keywords=['forum', 'drf forum', 'API Based forum'],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=[
        'django>=1.8,<1.11',
        'djangorestframework>=3.5',
        'django-autoslug>=1.9.3',
        'django-filter>=1.0.1',
    ],
    test_suite='runtests.runtests',
)
