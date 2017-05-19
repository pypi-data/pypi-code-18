from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()


setup(
    name="hornet",
    version="0.1.1",
    description="An approach to stacking configurations made up of nested dictionaries",
    long_description=readme,
    url="https://github.com/bheklilr/hornet",
    author="Aaron Stevens",
    author_email="bheklilr2@gmail.com",
    license="MIT",
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    keywords='config configuration nested stacked json yaml dict dictionary',
    packages=find_packages(exclude=['docs']),
    test_suite='hornet.tests',
    # use_scm_version=True,
    # setup_requires=['setuptools_scm'],
)
