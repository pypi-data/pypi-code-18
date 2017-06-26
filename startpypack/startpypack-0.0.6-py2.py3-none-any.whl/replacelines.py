def replacelines(clines,target,replacement):
  """This function executes the .replace() method on each element of a 'str' object list.

  Args:
      clines: A 'str' list object, the lines of text to read through to find and replace.
      target: A 'str', what to search for to replace.
      replacement: A 'str', what to replace the target with.

  Returns:
    a 'str' list object: The results of running the find and replace on the input text.
  """
  for i in range(0,len(clines),1):
    clines[i] = clines[i].replace(target,replacement)
  return(clines)
