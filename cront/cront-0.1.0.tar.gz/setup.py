try:
    from setuptools import setup, find_packages
except ImportError:
    import ez_setup
    ez_setup.use_setuptools()
    from setuptools import setup, find_packages

from cront import version


setup(
    name='cront',
    version=version,
    description="cront is a library that can make the task apps like crontab.",
    long_description=open('README.md').read(),
    keywords='tornado crontab',
    author='Asmodius',
    author_email='asmodius.a@gmail.com',
    license='MIT',
    url='https://github.com/asmodius/cront',
    download_url='https://github.com/asmodius/cront/archive/master.zip',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'License :: OSI Approved',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],
    zip_safe=False,
    packages=find_packages(),
    setup_requires=open("requirements.txt").read().split("\n"),
    install_requires=open("requirements.txt").read().split("\n"),
)
