from setuptools import setup

setup(
    name='water_ebmas',
    version='0.2.dev1',
    description='Just test python project',
    author='LYB',
    author_email='lyb10944@163.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='python water-II',
    packages=['bin','ebmas'],
    include_package_data=True,
    zip_safe=True,
)