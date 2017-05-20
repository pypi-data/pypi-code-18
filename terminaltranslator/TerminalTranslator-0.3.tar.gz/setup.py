
if __name__ == "__main__":
    from distutils.core import setup

    setup(
        name='TerminalTranslator',
        version='0.3',
        author="Veelion chong",
        author_email="veelion@gmail.com",
        license='MIT',
        description=("Linux terminal translating tool implemented in Python"),
        scripts=['t', 'tt', 'translator.py'],
    )

