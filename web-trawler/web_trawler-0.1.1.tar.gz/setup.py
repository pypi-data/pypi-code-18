import setuptools

from web_trawler import version

setuptools.setup(
    name="web_trawler",
    version=version.__version__,
    description="Trawl web pages for files to download",
    url="https://gitlab.com/dlab-indecol/web_trawler",
    author="Gorm Roedder",
    author_email="gormroedder@gmail.com",
    license="GPLv3",
    packages=["web_trawler"],
    package_data={"web_trawler": ["config.json", "bin/web_trawler"]},
    zip_safe=False,
    install_requires=[
        'lxml>=3.7.3',
        'cssselect>=1.0.1'
    ],
    entry_points={'console_scripts': ['web_trawler = web_trawler:main']},
)