def pkdirs(pname,wdir='.'):
  """This function creates a python package folder structure in a specified directory.

  Args:
      pname: A string, the name of the package to create.
      wdir: A string, the path to where to create the python package folder structure. Defaults to '.'.

  Returns:
    NULL: There are no returns, a selection of folders is created.
  """
  from startpypack import mkdir    

  # Make the top level folder
  mkdir(wdir + '/' + pname)
  # Make the second level folder
  mkdir(wdir + '/' + pname + '/' + pname)
  # Make the third level folder
  mkdir(wdir + '/' + pname + '/' + pname + '/' + pname)
  # Make the files folder
  mkdir(wdir + '/' + pname + '/' + pname + '/' + pname + '/files')
  # Make the data folder
  mkdir(wdir + '/' + pname + '/' + pname + '/' + pname + '/files/data')
  # Make the docs folder
  mkdir(wdir + '/' + pname + '/' + pname + '/' + pname + '/files/docs')

