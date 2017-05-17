from distutils.core import setup
import os
with open(os.path.join(os.path.dirname(__file__), 'README.txt')) as f:
    long_description = f.read()
setup(
    name='resttest',
    version='0.1dev',
    packages=['resttest', 'lib'],
    url='https://github.com/pupattan/resttest',
    license='MIT',
    author='pulakpattanayak',
    author_email='pulak.pattanayak@gmail.com',
    description='REST test API',
    long_description=long_description,
    keywords="rest http",
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',

    ]
)
