from setuptools import setup
setup(name='promisepay',
      description='Python SDK for PromisePay/ Assemblypayments',
      version='1.5',
      url='https://github.com/Rekvant/promisepay-python',
      author='Anish Menon',
      author_email='info@rekvant.com',
      license='Apache2',
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: Apache Software License',
          'Programming Language :: Python :: 2.7'
      ],

      packages=['promisepay'],
      install_requires=[
          'requests >=2.14',
      ],
     
)
