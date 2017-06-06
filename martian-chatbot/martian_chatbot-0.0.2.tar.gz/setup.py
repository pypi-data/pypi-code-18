from setuptools import setup

setup(name='martian_chatbot',
      version='0.0.2',
      description='Chatbot creation module',
      url='https://jzitkovic@gitlab.martianandmachine.com/service/martian-chatbot.git',
      author='Josip Zitkovic',
      author_email='josip@martian.agency',
      license='MIT',
      packages=['chatbot'],
      install_requires=[
          'pymongo',
          'ChatterBot',
          'requests',
          'simplejson'
      ],
      zip_safe=False)
