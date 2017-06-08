from setuptools import find_packages, setup

import taggit


with open('README.rst') as f:
    readme = f.read()

setup(
    name='django-taggit-tronc',
    version='.'.join(str(i) for i in taggit.VERSION),
    description='django-taggit is a reusable Django application for simple tagging.',
    long_description=readme,
    author='Maintained by Charley Bodkin / Tronc. Originally by Alex Gaynor',
    author_email='charley.bodkin@latimes.com',
    url='https://github.com/troncx/django-taggit',
    packages=find_packages(exclude=('tests*',)),
    package_data = {
        'taggit': [
            'locale/*/LC_MESSAGES/*',
        ],
    },
    license='BSD',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.7',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 1.10',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    include_package_data=True,
    zip_safe=False,
    setup_requires=[
        'isort'
    ],
)
