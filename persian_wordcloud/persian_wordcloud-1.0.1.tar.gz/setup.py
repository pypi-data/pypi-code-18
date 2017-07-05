"""
See:
https://github.com/Mehotkhan/persian-word-cloud
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))


setup(
    name='persian_wordcloud',
    version='1.0.1',
    description='Persian Word Cloud Generator',
    long_description='Persian Word Cloud Generator',
    url='https://github.com/Mehotkhan/persian-word-cloud',
    author='Ali Zemani',
    author_email='mehot1@gmail.coom',
    license='MIT',
    packages=['persian_wordcloud'],
    package_data={'persian_wordcloud': ['stopwords', 'fonts/Vazir-Light.ttf']},
    # What does your project relate to?
    keywords='persian , wordcloud',
    install_requires=['arabic_reshaper', 'python-bidi', 'wordcloud'],
)
