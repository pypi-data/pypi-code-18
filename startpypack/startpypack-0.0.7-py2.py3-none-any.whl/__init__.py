"""
A python package for making python packages.
"""
from .mkdir import mkdir
from .pkdirs import pkdirs
from .getlines import getlines
from .replacelines import replacelines
from .writefile import writefile
from .pkmkfiles import pkmkfiles
from .makepackage import makepackage
from .addlines import addlines
from .mkfunc import mkfunc

def readme():
  """This function displays the contents of the README.rst file.

  Args:
      NULL (NA): There are no parameters.

  Returns:
    NULL: There are no returns, a print statement is executed.
  """
  import os
  this_dir, this_filename = os.path.split(__file__)
  DATA_PATH = os.path.join(this_dir, "README.rst")
  with open(DATA_PATH) as f:
      print(f.read())
