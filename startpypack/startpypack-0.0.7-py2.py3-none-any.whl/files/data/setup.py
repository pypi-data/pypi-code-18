from setuptools import setup

setup(name='[[packagename]]',
      version='[[versionnumber]]',
      description='[[packagedescription]]',
      url='[[packageurl]]',
      author='[[authorname]]',
      author_email='[[authoremail]]',
      license='[[packagelicense]]',
      packages=['[[packagename]]'],
      package_dir={'[[packagename]]': './[[packagename]]'},
      package_data={'[[packagename]]': ['files/data/*','files/docs/*','README.rst']},
      install_requires=['markdown'],
      include_package_data=True,
      zip_safe=False)
