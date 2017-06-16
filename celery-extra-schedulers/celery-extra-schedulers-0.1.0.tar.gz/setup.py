from setuptools import setup, find_packages

setup(
    name='celery-extra-schedulers',
    version='0.1.0',
    url='https://github.com/mixkorshun/celery-extra-schedulers',
    description='Extra schedulers for celery.',
    keywords=['celery', 'celerybeat', 'scheduler'],

    # long_description=open('README.rst', 'r').read(),

    author='Vladislav Bakin',
    author_email='mixkorshun@gmail.com',
    maintainer='Vladislav Bakin',
    maintainer_email='mixkorshun@gmail.com',

    license='MIT',

    install_requires=[
        'celery',

        'redis',
    ],

    packages=find_packages(exclude=['tests.*', 'tests']),

    test_suite='tests',

    classifiers=[
        # 'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
