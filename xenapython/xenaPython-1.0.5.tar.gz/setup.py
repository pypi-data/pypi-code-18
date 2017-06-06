from setuptools import setup, find_packages
print(find_packages())
setup(
    name="xenaPython",
    version="1.0.5",
    packages=find_packages(),
    author = '@jingchunzhu, @GiriB',
    author_email = 'jingchunzhu@gmail.com',
    description = 'XENA python API',
    url = 'https://github.com/ucscXena/xenaPython',
    keywords = ['xena', 'ucsc', 'xenaAPI', 'xenaPython'],
    license='Apache 2.0',
)
