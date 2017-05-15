from setuptools import setup, find_packages


setup(
    name='django-datefilterspec',
    version='1.3.0',
    description='Allow to filter by a custom date range on the Django Admin',
    long_description=open('README.rst').read(-1),
    author='Diego Ponciano',
    author_email='dgo.ponciano@gmail.com',
    url='http://github.com/diegoponciano/django-datefilterspec',
    keywords=[
        'django admin',
        'django date range',
    ],
    install_requires=[
        "Django",
    ],
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Framework :: Django',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.4',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Environment :: Web Environment',
        'Operating System :: OS Independent'
    ],
    license = 'License :: OSI Approved :: BSD License',
)
