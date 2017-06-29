from setuptools import setup


def readme():
    with open("README.rst") as f:
        return f.read()

setup(name='didsho',
      version='1.5',
      description='Didsho SDK for python telegram bot @didshobot',
      long_description=readme(),
      classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: Freely Distributable',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries',
      ],
      url='https://github.com/mdisepehr/didshoPython',
      author='Sadeq Hajizadeh',
      author_email='sadegh.h.2007@hotmail.com',
      license='FREE TO USE',
      keywords='didsho sdk didshoPython didshosdk',
      packages=['didsho'],
      install_requires=[
          'requests',
      ],
      include_package_data=True,
      zip_safe=False)
