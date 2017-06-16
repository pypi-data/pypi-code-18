from setuptools import setup

setup(name='gotocorepy',
      version='0.0.5',
      description='mvc framework, for python',
      url='https://github.com/varadig/GotoCorePy',
      author='Gabor Varadi',
      author_email='varadi83gabor@gmail.com ',
      license='MIT',
      packages=['core',
                'core.base',
                'core.context',
                'core.filesystem',
                'core.logger',
                'core.logger.base',
                'core.notification',
                'core.python',
                'core.service',
                'core.utils'],
    install_requires=[
          'hurry.filesize',
      ],
      zip_safe=False)
