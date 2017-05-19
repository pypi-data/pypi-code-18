from distutils.core import setup
setup(
    name="trashcaron",
    version="0.1.4",
    author="eayin2",
    author_email="eayin2 at gmail dot com",
    include_package_data=True,
    url="https://github.com/eayin2/trashcaron",
    description="Trashbin script with btrfs support and automatic trash purge feature.",
    install_requires=[],
    entry_points={
        'console_scripts': [
            'trashcaron = trashcaron.trashcaron:main',
        ]
    }
)
