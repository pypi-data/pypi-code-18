from setuptools import setup

long_description = open('README.rst').read()

setup(
    name='marduk',
    version='0.0.0.alpha1',
    description='Transpile your Python 3.6 code to older python versions',
    long_description=long_description,
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
    ],
    author='Thomas Grainger',
    author_email='marduk@graingert.co.uk',
    url='https://github.com/graingert/marduk',
    license='AGPL3+',
    py_modules=['marduk'],
    python_requires='>=3.5',
    zip_safe=True,
)
