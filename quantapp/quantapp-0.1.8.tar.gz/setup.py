from setuptools import setup
import distutils.sysconfig
 
setup(
    name='quantapp',                                                                # This is the name of your PyPI-package.
    description='QuantApp Libraries for Systematic Investments and Data Science',   # This is the name of your PyPI-package.
    version='0.1.8',                                                                  # Update the version number for new releases
    packages=['quantapp'],                                                      # The name of your scipt, and also the command you'll be using for calling it

    url='https://www.quantapp.net',
    author='Arturo Rodriguez',
    author_email='arturo.rodriguez@quantapp.net',
    license='MIT',
    python_requires='>=3',
    
    
    #package_data={
    #   'quantapp': ['*.dll'],     # All files from folder A       
    #   },
    include_package_data=True,
)