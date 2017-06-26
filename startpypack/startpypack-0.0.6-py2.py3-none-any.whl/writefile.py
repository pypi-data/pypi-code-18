def writefile(fpath,flines):
  """This function writes lines into a new plaintext file.

  Args:
      fpath: A string, the path to the file to write into.
      flines: A 'str' object, the lines to write into the file.

  Returns:
      NULL: A file is written.
  """
  # Write the list of strings back into the file
  f = open(fpath,'w+')
  f.writelines(flines)
  f.close()
