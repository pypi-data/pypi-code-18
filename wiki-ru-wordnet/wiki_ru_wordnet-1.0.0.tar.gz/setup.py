from setuptools import setup, find_packages

setup(
      name = 'wiki_ru_wordnet',
      version = '1.0.0',
      license='MIT',
      packages=['wiki_ru_wordnet'],
      scripts=['wiki_ru_wordnet/synset.py', 'wiki_ru_wordnet/word.py', 'wiki_ru_wordnet/wordnet.py', 'wiki_ru_wordnet/wordnet_db_connector.py'],
      package_data={'wiki_ru_wordnet': ['wordnet/wordnet.db']},
      author = 'jamsic',
      author_email = 'jamsic@yandex.ru',
      description = 'wordnet for russian language',
      url='https://github.com/jamsic/ru-wordnet',
      classifiers=[
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Intended Audience :: Science/Research',
          'Topic :: Text Processing :: Linguistic',
          'Intended Audience :: Science/Research',
          'Natural Language :: Russian',
          'License :: OSI Approved :: MIT License',
          'Development Status :: 3 - Alpha',
      ],
    )

