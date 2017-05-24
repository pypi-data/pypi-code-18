from setuptools import setup

with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    the_license = f.read()

setup(
    name='pcaplib',
    version='1.0.0',
    description='A very simple PCAP library',
    long_description=readme,
    classifiers=[
        'Topic :: System :: Networking',
        'Topic :: System :: Networking :: Monitoring',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: Log Analysis',
    ],
    author='Salah Gherdaoui',
    author_email='salah.gherdaoui@gmail.com',
    py_modules=['pcaplib'],
    license=the_license,
    packages=['pcaplib'],
    python_requires='>=3.4',
    test_suite='pytest.collector',
    tests_require=['pytest', 'pytest-cov'],
    zip_safe=False,
)
