from setuptools import setup

if __name__ == "__main__":
    setup(
        name='pytest-pycodestyle',
        description='pytest plugin to check PEP8 requirements',
        long_description=open("README.txt").read(),
        license="MIT license",
        version='1.0.6',
        author='Holger Krekel and Ronny Pfannschmidt',
        author_email='holger.krekel@gmail.com',
        url='https://bitbucket.org/pytest-dev/pytest-pep8',
        py_modules=['pytest_pep8'],
        entry_points={'pytest11': ['pep8 = pytest_pep8']},
        install_requires=['pytest-cache', 'pytest>=2.4.2', 'pycodestyle>=1.3', ],
        classifiers=[
            'Programming Language :: Python',
            'Programming Language :: Python :: 2.6',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4'
        ],
    )
