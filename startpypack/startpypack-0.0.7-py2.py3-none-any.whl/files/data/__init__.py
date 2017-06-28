"""
A package that [[packagedescription]].
"""

def readme():
  """This function displays the contents of the README.rst file.

  Args:
      NULL (NA): There are no parameters.

  Returns:
    NULL: There are no returns, a print statement is executed.
  """
  import os
  this_dir, this_filename = os.path.split(__file__)
  DATA_PATH = os.path.join(this_dir, "../README.rst")
  with open(DATA_PATH) as f:
      print(f.read())
