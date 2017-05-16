import textwrap

from setuptools import find_packages, setup

setup(
    name='win32compat',
    description='Python for Window Extensions',
    long_description=textwrap.dedent('''
        Python extensions for Microsoft Windows'
        Provides access to much of the Win32 API, the
        ability to create and use COM objects, and the
        Pythonwin environment
        
        This provides backward compatibility.
        '''),
    author='Mark Hammond (et al)',
    author_email='mhammond@users.sourceforge.net',
    url='http://sourceforge.net/projects/pywin32/',
    license='GNU GPL v3',
    packages=find_packages(),
    setup_requires=['setuptools_scm'],
    use_scm_version=True)
