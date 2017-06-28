from setuptools import setup
 
setup(
    name='quantapp',                                                                # This is the name of your PyPI-package.
    description='QuantApp Libraries for Systematic Investments and Data Science',   # This is the name of your PyPI-package.
    version='0.1.1',                                                                  # Update the version number for new releases
    scripts=['load_libraries'],                                                      # The name of your scipt, and also the command you'll be using for calling it

    url='https://www.quantapp.net',
    author='Arturo Rodriguez',
    author_email='arturo.rodriguez@quantapp.net',
    license='MIT',
    python_requires='>=3'
)