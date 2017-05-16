from setuptools import setup

setup(name="solidus",
      version="0.10.2",
      description="Solidus Security Agent for OSX",
      url="http://github.com/SolidusSecurity/SolidusOSX",
      author="Joe Kovacic",
      author_email="j.kovacic@SolidusSecurity.com",
      packages=['solidus'],
      package_data={'solidus' : ['solidus/*']},
      zip_safe= False)


      
