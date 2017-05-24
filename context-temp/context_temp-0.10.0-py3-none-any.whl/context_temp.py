__version__ = '0.10.0'

import contextlib, os, shutil, tempfile

# =============================================================================
# Context Managers
# =============================================================================

@contextlib.contextmanager
def temp_directory():
    """This ``Context Manager`` creates a temporary directory and yields its
    path.  Upon exit the directory is removed.

    Example:

    .. code-block:: python

        with temp_directory() as td:
            filename = os.path.join(td, 'foo.txt')
            with open(filename, 'w') as f:
                f.write('stuff')

        # got here? => td is now gone, foo.txt is gone too
    """
    tempdir = tempfile.mkdtemp()
    try:
        yield tempdir
    finally:
        shutil.rmtree(tempdir)


@contextlib.contextmanager
def temp_file():
    """This ``Context Manager`` creates a temporary file which is readable and
    writable by the current user and yields its path.  Once the ``Context``
    exits, the file is removed.

    Example:

    .. code-block:: python

        with temp_file() as filename:
            with open(filename, 'w') as f:
                f.write('stuff')
                
        # got here? => file called "filename" is now gone
    """
    _, filename = tempfile.mkstemp()
    try:
        yield filename
    finally:
        os.remove(filename)
