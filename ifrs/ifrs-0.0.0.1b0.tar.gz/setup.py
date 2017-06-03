
from setuptools import setup, find_packages


long_desc = """
This is made for some specific environment.
This contains ...

IFRS Taxonomy : http://www.ifrs.org/Use-around-the-world/IFRS-translations/Pages/IFRS-Taxonomy-in-Korean.aspx

"""

setup(name='ifrs',
        version='0.0.0.1b',
        description='useful tools for Korean Financial Statement disclosured on https://dart.fss.or.kr',
        long_description=long_desc,
        url='http://github.com/pydemia/ifrs',
        author='Young-Ju Kim',
        author_email='pydemia@gmail.com',
        license='MIT License',
        classifiers=[
                # How Mature: 3 - Alpha, 4 - Beta, 5 - Production/Stable
                'Development Status :: 3 - Alpha',
                'Programming Language :: Python :: 3.5'
                ],
        packages=find_packages(exclude=['contrib', 'docs', 'tests']),
        install_requires=['python-xbrl'],
        zip_safe=False)
