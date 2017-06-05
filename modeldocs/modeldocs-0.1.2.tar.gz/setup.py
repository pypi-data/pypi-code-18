import os
from setuptools import setup

# modeldocs
# Documentation generator for your model subclasses.


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="modeldocs",
    version="0.1.2",
    description="Documentation generator for your model subclasses.",
    author="Johan Nestaas",
    author_email="johannestaas@gmail.com",
    license="MIT",
    keywords="",
    url="https://github.com/johannestaas/modeldocs",
    packages=['modeldocs'],
    package_dir={'modeldocs': 'modeldocs'},
    long_description=read('README.rst'),
    classifiers=[
        # 'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        'Development Status :: 3 - Alpha',
        # 'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        'License :: OSI Approved :: MIT License',
        'Environment :: Console',
        'Environment :: X11 Applications :: Qt',
        'Environment :: MacOS X',
        'Environment :: Win32 (MS Windows)',
        'Operating System :: POSIX',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
    ],
    install_requires=[
    ],
    entry_points={
        'console_scripts': [
            'modeldocs=modeldocs:main',
        ],
    },
    # If you get errors running setup.py install:
    # zip_safe=False,
    #
    # For including non-python files:
    package_data={
        'modeldocs': [
            'templates/*.js',
            'templates/*.css',
            'templates/*.html',
            'templates/css/*.css',
            'templates/img/*.ico',
            'templates/locales/*.js',
            'templates/locales/*.css',
            'templates/utils/*.js',
            'templates/utils/*.css',
            'templates/vendor/*.js',
            'templates/vendor/*.css',
            'templates/vendor/path-to-regexp/LICENSE',
            'templates/vendor/path-to-regexp/index.js',
            'templates/vendor/prettify/*.js',
            'templates/vendor/prettify/*.css',
        ],
    },
    include_package_data=True,
)
