from setuptools import setup

setup(name='sample-app-arvind',
      version='0.2.1',
      description='The funniest joke in the world',
      url='http://github.com/storborg/funniest',
      author='Flying Circus',
      author_email='flyingcircus@example.com',
      license='MIT',python_requires='>=3',
      packages=['code'],
	install_requires=['markdown'],
      zip_safe=False)
