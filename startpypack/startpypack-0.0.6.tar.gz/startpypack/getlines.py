def getlines(fpath):
  """This function reads in lines from a plaintext file and returns them as a 'str' object.

  Args:
      fpath: A string, the path to the file to read.

  Returns:
    a 'str' object: The text contents of the file that was specified.
  """
  f = open(fpath,'r')
  rl = f.readlines()
  f.close()
  return(rl)
