__version__ = '0.8.2'


# Suppress HTTPS security warnings
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning \
    as VendoredInsecureRequestWarning
requests.packages.urllib3.disable_warnings(VendoredInsecureRequestWarning)


try:
    import urllib3
    from urllib3.exceptions import InsecureRequestWarning
    urllib3.disable_warnings(InsecureRequestWarning)
except ImportError:
    pass
