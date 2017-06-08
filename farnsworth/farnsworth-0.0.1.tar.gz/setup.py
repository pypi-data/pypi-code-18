from setuptools import setup

setup(
    name='farnsworth',
    packages=['farnsworth'],
    version="0.0.1",
    description='A small Python library for rendering React components.',
    license='MIT',
    author='Jack Valinsky',
    author_email='jvalinsk@u.rochester.edu',
    url='http://github.com/jvalinsky/farnsworth',
    download_url = 'https://github.com/jvalinsky/farnsworth/archive/0.0.1.tar.gz',
    install_requires=[
        'py_mini_racer',
    ],
    zip_safe=False,
    include_package_data=True,
    test_suite='farnsworth.tests',
    keywords=['react', 'server-side rendering', 'web'],
)
