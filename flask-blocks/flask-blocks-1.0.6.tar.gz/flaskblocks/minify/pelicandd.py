import os
import requests


uri = "https://minify.pelicandd.com/api/v1/less"


def minify_less_file(source, destination, force_update=False):
    """
    Minifies a LESS file to CSS and stores the result to the specified
    destination.
    """
    if force_update or _should_update(source, destination):
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


def _should_update(source, destination):
    """
    Ensures the destination is outdated, i.e. that the source was modified
    after the destination was effectively changed.
    """
    source_time = os.path.getmtime(source)
    try:
        destination_time = os.path.getmtime(destination)
    except OSError:
        # The destination file doesn't exist.
        return True

    return destination_time <= source_time
