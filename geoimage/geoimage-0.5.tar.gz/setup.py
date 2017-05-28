from setuptools import setup


setup(
    name='geoimage',
    version='0.5',
    url="https://github.com/suvarchal/GeoLocateImage",
    author='Suvarchal Kumar Cheedela',
    author_email='suvarchal.kumar@gmail.com',
    license="MIT",
    packages=['geoimage'],
    install_requires=['PIL'],
    description="A utility to geolocate images",
    classifiers=[
    'Development Status :: 4 - Beta',

    'Topic :: Software Development :: Build Tools',
     'License :: OSI Approved :: MIT License',

    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
],
    long_description=open('README').read()
)
