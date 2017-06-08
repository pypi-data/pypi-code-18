setup(
    name='aysclient',
    version='9.0.0',
    description='AtYourService client (AYS)',
    url="https://github.com/Jumpscale/ays9/tree/master/clients/sync_client",
    author='Ahmed T. Youssef',
    author_email='xmonader@gmail.com',
    maintainer='Ahmed T. Youssef',
    maintainer_email='xmonader@gmail.com',
    package_dir = {
        'aysclient': 'JumpScale9AYS/clients/sync_client'
    },
    packages=['aysclient'],
    license='Apache',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python',
    ],
    install_requires=[
        'requests',
    ],

)
