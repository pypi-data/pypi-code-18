"""Setup.py file for atemon.EmailValidator package."""
from distutils.core import setup

setup(
    name='Atemon-EmailValidator',
    version='0.1.2.3',
    packages=['atemon', 'atemon.EmailValidator'],
    long_description="""Check if the given email address is valid or not using nslookup.EmailValidator
==============

Check if the given email address is valid or not using nslookup

We can get a brief idea of if email address is valid or not using regular expressions. Currently with thousands of new TLDs its bit too hard. This tool uses nslookup command to check if a mail exchange server is configured for a domain. This could be the best level of email validation other than actually sending (unsolicited) mail.

You need the tool ```nslookup``` installed on the machine running this tool.

To install nslookup, run the command

#### CentOS/RHEL
    # yum install bind-utils

#### Ubuntu/Debian

    # sudo apt-get update
    # sudo apt-get install dnsutils

#### Install this from PIP

    # pip install Atemon-EmailValidator

#### Usage

    from atemon.EmailValidator import EmailValidator
    v = EmailValidator()
    v.is_valid('something@gmail.com')

Happy coding :)
""",
    author="Varghese Chacko",
    author_email="varghese@atemon.com",
    url="https://github.com/atemon/Python-EmailValidator",
    provides=["EmailValidator"],
    license="MIT License",
)
