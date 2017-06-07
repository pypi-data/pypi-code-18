import os
import requests


uri = "https://minify.pelicandd.com/api/v1/less"


def minify_less_file(source, destination):
    """
    Minifies a LESS file to CSS and stores the result to the specified
    destination.
    """
    source_name = os.path.basename(source)
    r = requests.post(
        uri, files={"source": (source_name, open(source, "rb"))})
    r.raise_for_status()
    with open(destination, "w") as f:
        f.write(r.text)


def minify_less(less_code):
    """
    Minifies a LESS script to CSS and returns the resulting CSS code.
    """
    r = requests.post(uri, data={"source": less_code})
    r.raise_for_status()
    return r.text
