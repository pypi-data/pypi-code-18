from setuptools import setup

setup(name='dsbox-datapreprocessing',
      version='0.0.2',
      url='https://github.com/usc-isi-i2/dsbox-cleaning.git',
      maintainer_email='kyao@isi.edu',
      maintainer='Ke-Thia Yao',
      description='DSBox data preprocssing tooles',
      license='MIT',
      packages=['dsbox', 'dsbox.datapreprocessing'],
      zip_safe=False,
      install_requires=['pandas', 'langdetect']
      )
