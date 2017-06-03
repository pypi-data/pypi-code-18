from setuptools import setup, find_packages

setup(name='twitter_controller',
      version='0.4',
      description='This is a package to analyze tweets of a certain person',
      url='https://github.com/AGHPythonCourse2017/zad3-kanes115.git',
      author='Dominik Stanaszek',
      author_email='dominikstanaszek@icloud.com',
      license='NONE',
      packages=['twitter_controller'],
      package_data={'': ['twitter_controller/resources/*']},
      install_requires=[
        'numpy',
        'indicoio',
        'pytest'
      ],
      zip_safe=False)