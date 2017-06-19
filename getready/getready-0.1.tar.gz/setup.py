""" Get Ready setup """

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup  # pylint: disable=E0611,F0401


setup(
    name='getready',
    version=0.1,
    install_requires=[],
    packages=['getready'],
    author='Werner Van Geit',
    author_email='werner.vangeit@gmail.com',
    description='Get Ready Forever !',
    entry_points={'console_scripts': ['getready=getready.getready:main'], },
    license="LGPLv3",
    keywords=(),
    classifiers=[
        'Development Status :: 4 - Beta'])
