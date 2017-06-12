from setuptools import setup, find_packages

setup(
    name='blast_score_ratio',
    description='''Get BLAST Score Ratios (BSR; as described in Rasko et al (2006) doi:10.1186/1471-2105-6-2)
for a reference proteome compared to other proteomes. Produce charts of the data.''',
    version='1.0.4',
    license=' GNU GPLv3',
    author='John C. Thomas',
    author_email='jaytee00@gmail.com',
    include_data_files = True,
    # keys are specific package folders to include, value are globs eg '*.txt'
    package_data={'blast_score_ratio': ['*.txt'], 'Examples':['Examples/*.faa']},
    install_requires = ['biopython >= 1.43', 'matplotlib'],
    #extras_require = {'Excel':'openpyxl >= 2'},
    classifiers= ['Programming Language :: Python :: 3',
                  'Development Status :: 4 - beta',],
    keywords = "comparative genomics biopython bioinformatics protein blast BSR",
    packages = find_packages(),
)