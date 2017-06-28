from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()
setup(
    name='scikitcrf_ner',
    version='1.0',
    description='Enity Recognition using ScikitCRF',
    long_description=readme(),
    packages=["scikitcrf_ner", "scikitcrf_ner.entityRecognition"],
    packages_dir={"", "scikitcrf_ner"},
    author='Manikandan Thangavelu',
    author_email='tmanikandan05@gmail.com',
    license='MIT',
    keywords='scikitCRF entity entityrecognition crf ner',
    install_requires=['spacy','sklearn_crfsuite'],
    #scripts=['entityRecognition']
    )