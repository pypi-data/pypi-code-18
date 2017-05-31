from setuptools import setup

setup(
    name='rbx',
    version='1.0.0',
    license='Apache 2.0',
    description='Scoota Platform for the Rig',
    url='http://scoota.com/',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Topic :: Internet',
    ],
    zip_safe=True,
    author='The Scoota Engineering Team',
    author_email='engineering@scoota.com',
    install_requires=[
        'docker-compose',
        'invoke==0.13.0',
        'twine',
    ],
)
