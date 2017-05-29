from setuptools import setup

def _requires_from_file(filename):
    return open(filename).read().splitlines()

setup(name='funniest_noga',
      version='0.1',
      description='The funniest_noga joke in the world',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Topic :: Text Processing :: Linguistic',
      ],
      keywords='funniest_noga joke comedy flying circus',
      url='http://github.com/storborg/funniest_noga',
      author='Flying Circus',
      author_email='flyingcircus@example.com',
      license='MIT',
      packages=['funniest_noga'],
      install_requires=_requires_from_file('requirements.txt'),
      include_package_data=True,
      zip_safe=False,
    test_suite='test.test_joke',
    scripts=['bin/funniest-joke'],
)
