import os

def get_proxy():
    return os.environ.get('HTTPS_PROXY', os.environ.get('https_proxy', None))

