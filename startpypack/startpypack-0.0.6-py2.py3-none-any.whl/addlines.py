def addlines(clines,inloc,inline):
  """This function inserts a new line into a provided location in a 'str' object list.

  Args:
      clines: A 'str' list object, the lines of text to add a new line into.
      inloc: A numeric, the line number where the new line is to be inserted directly 'after'.
      inline: A 'str', the character string which is the new line to insert.

  Returns:
    a 'str' list object: The results of inserting the new line.
  """
  import itertools

  # If it is a single line (one string) make it a list with one element
  if isinstance(inline,str):
    inline = [inline]

  # Evaulate the position along the initial list of lines
  if inloc == 0:
    clines = [inline,clines]
  elif inloc>len(clines):
    clines = [clines,inline]
  else:
    clines = [clines[0:inloc],inline,clines[inloc:len(clines)]]

  # Flatten the return list
  clines = list(itertools.chain(*clines))

  # Return the list
  return(clines)
