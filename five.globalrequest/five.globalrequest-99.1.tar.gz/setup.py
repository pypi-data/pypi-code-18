from setuptools import setup

setup(
    name='five.globalrequest',
    version='99.1',
    description="DEPRECATED: Zope integration for zope.globalrequest",
    long_description=(open("README.rst").read() + "\n" +
                      open("CHANGES.rst").read()),
    classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Development Status :: 7 - Inactive",
    ],
    keywords='zope global request',
    author='Zope Foundation and Contributors',
    author_email='zope-dev@zope.org',
    url='https://github.com/zopefoundation/five.globalrequest',
    license='ZPL',
    packages=['five', 'five.globalrequest'],
    package_dir={'': 'src'},
    namespace_packages=['five'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'Zope2 >= 4.0a3',
    ],
)
