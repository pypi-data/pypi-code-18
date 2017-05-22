import os
import sys

from setuptools import find_packages, setup


# cx_Freeze: we added a undocumented option to enable building frozen versions
# of our packages. This should be refactored for a more safe approach in the
# future.
setup_kwargs = {}
if '--cx-freeze' in sys.argv:
    from cx_Freeze import setup, Executable

    build_options = {
        'include_files': [],
        'packages': ['os', 'pytunol', 'pygments', 'transpyler'],
        'excludes': [
            'tkinter', 'redis', 'lxml',
            'qturtle.qsci.widgets',
            'nltk', 'textblob',
            'matplotlib', 'scipy', 'numpy', 'sklearn',
            'notebook',
            'java',
            'sphinx', 'PIL', 'PyQt4'
        ],
        'optimize': 1,
    }
    base = 'Win32GUI' if sys.platform == 'win32' else None

    setup_kwargs['executables'] = [
        Executable(
            'src/pytunol/__main__.py',
            base=base,
            targetName='pytunol.exe' if sys.platform == 'win32' else 'pytunol',
            shortcutName='pytunol',
            shortcutDir='DesktopFolder',
        )
    ]
    setup_kwargs['options'] = {'build_exe': build_options}
    sys.argv.remove('--cx-freeze')


# Save version and author to __meta__.py
version = open('VERSION').read().strip()
dirname = os.path.dirname(__file__)
path = os.path.join(dirname, 'src', 'pytunol', '__meta__.py')
meta = '''# Automatically created. Please do not edit.
__version__ = '%s'
__author__ = 'F\\xe1bio Mac\\xeado Mendes'
''' % version
with open(path, 'w') as F:
    F.write(meta)


# Wraps command classes to register pytunol kernel during installation
def wrapped_cmd(cmd):
    class Command(cmd):
        def run(self):
            if 'src' not in sys.path:
                sys.path.append('src')

            from transpyler.jupyter.setup import setup_assets
            setup_assets(True)
            cmd.run(self)

    return Command


# Run setup() function
setup(
    name='pytunol',
    version=version,
    description='Interpretador de Escocia: un Python con acento lusitano.',
    author='Fábio Macêdo Mendes',
    author_email='fabiomacedomendes@gmail.com',
    url='https://github.com/transpyler/pytunol',
    long_description=('''
    Es un lenguaje de programación que modifica la sintaxis de Python para
    aceptar comandos en portugués. El lenguaje fue desarrollado como una
    extensión del Python que acepta comandos en portugués.

    El único objetivo de Pytuñol es facilitar el aprendizaje de programación.
    Una vez que los conceptos básicos se incautan, la transición a un lenguaje
    real (en el caso Python) se vuelve gradual y natural.
    '''),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries',
    ],

    # Packages and dependencies
    package_dir={'': 'src'},
    packages=find_packages('src'),
    install_requires=[
        'transpyler>=0.3.1'
    ],
    extra_requires={
        'gui': ['qturtle>=0.3.0']
    },

    # Wrapped commands (for ipytunol)
    # cmdclass={
    #    'install': wrapped_cmd(_install),
    #    'develop': wrapped_cmd(_develop),
    # },

    # Scripts
    entry_points={
        'console_scripts': [
            'pytunol = pytunol.__main__:main',
        ],
    },

    # Data files
    package_data={
        'pytunol': [
            'assets/*.*',
            'doc/html/*.*',
            'doc/html/_modules/*.*',
            'doc/html/_modules/tugalib/*.*',
            'doc/html/_sources/*.*',
            'doc/html/_static/*.*',
            'examples/*.pytg'
        ],
        'pytunol': [
            'ipytunol/assets/*.*',
        ],
    },
    # data_files=DATA_FILES,
    zip_safe=False,
    **setup_kwargs
)
