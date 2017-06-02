import os
import tempfile
import requests


def to_temp_file(url: str) -> str:
    """ 
    """

    fd, path = tempfile.mkstemp(prefix='pipper-')
    os.close(fd)

    return to_file(url, path)


def to_file(url: str, local_path: str) -> str:
    """ 
    """

    response = requests.get(url)
    with open(local_path, 'wb') as f:

        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)

    return local_path
