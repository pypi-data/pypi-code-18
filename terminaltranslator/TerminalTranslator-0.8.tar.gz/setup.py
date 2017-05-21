
if __name__ == "__main__":
    from setuptools import setup

    setup(
        name='TerminalTranslator',
        version='0.8',
        author="Veelion chong",
        author_email="veelion@gmail.com",
        license='MIT',
        url='https://github.com/veelion/tt',
        description=("Linux terminal translating tool implemented in Python"),
        scripts=['t', 'tt', 'terminaltranslator.py'],
    )

