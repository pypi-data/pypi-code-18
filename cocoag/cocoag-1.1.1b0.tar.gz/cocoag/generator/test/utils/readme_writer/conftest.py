import os
import pytest
import tempfile


"""
Fixture taken from:
https://docs.pytest.org/en/latest/fixture.html
"""
@pytest.fixture()
def cleandir():
    newpath = tempfile.mkdtemp()
    os.chdir(newpath)


@pytest.fixture()
def existing_readme():
    newpath = tempfile.mkdtemp()
    os.chdir(newpath)
    new_file_path = os.path.join(newpath, "README.md")
    readme = open(new_file_path, 'w')
    readme.write("DONT REPLACE ME\n")
    readme.write("===============\n")
    readme.write("[![Codecov](WWW.REPLACEME.COM)]()")
    readme.close()