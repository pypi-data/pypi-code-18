def mkdir(dirname):
  """This function creates a folder if it does not exist.

  Args:
      dirname: A string, the path of the directory to create.

  Returns:
    NULL: There are no returns, a selection of folders is created.
  """
  import os
  if not os.path.exists(dirname):
    os.makedirs(dirname)
