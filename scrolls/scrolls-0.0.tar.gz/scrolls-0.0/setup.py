from setuptools import setup, find_packages


requires = []
with open('requirements.txt') as f:
    requires = f.read().splitlines()

setup(name='scrolls',
      version='0.0',
      description='Log manager.',
      url='https://github.com/ilogue/scrolls',
      long_description='',
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='Jasper J.F. van den Bosch',
      author_email='japsai@gmail.com',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      scripts=['exe/scrolls'],
      test_suite="tests",
      entry_points="""\
      [paste.app_factory]
      main = webtasks:main
      """,
      )
