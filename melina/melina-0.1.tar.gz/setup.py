from setuptools import setup, find_packages
import melina

long_description = open('README.rst').read()

setup(
    name = 'melina',
    version = melina.__version__,
    author = 'Krzysztof Laskowski',
    author_email = 'krzysztof.laskowski@nokia.com',
    maintainer = 'Krzysztof Laskowski',
    maintainer_email = 'krzysztof.laskowski@nokia.com',
    license = 'MIT license',
    url = 'https://github.com/aurzenligl/melina',
    description = 'melina: meta/xml converter',
    long_description = long_description,
    py_modules = ['melina'],
    requires = ['lxml'],
    install_requires = ['lxml'],
    keywords = 'idl compiler',
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Telecommunications Industry',
        'Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator',
        'Topic :: Software Development :: Code Generators',
        'Topic :: Software Development :: Compilers',
        'Topic :: Utilities',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
    entry_points = {
        'console_scripts': [
            'melina = melina:main'
        ],
    },
)
