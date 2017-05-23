from setuptools import setup


setup(
    name='QuarkUtilities',
    version="0.0.9",
    license='BSD',
    author='Ali Arda Orhan',
    author_email='arda.orhan@dogantv.com.tr',
    description='Quark-CMS Utilities.',
    long_description=__doc__,
    packages=['quark_utilities'],
    platforms='any',
    install_requires=[
        'FlaskyTornado==0.0.28',
        'PyJWT==1.4.2',
        'jsonschema==2.6.0',
        'pymongo==3.4.0',
        'user_agents==1.1.0'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
