def mkfunc(pname, fname, wdir='.', loadfile=False, fsf='', docadd=False):
  """This function creates a python .py file containing code for a new python function.

  Args:
      pname: A string, the python package name to create the function file within.
      fname: A string, the name of the function to create a new function file for.
      wdir: A string, the path of the directory to find the python package withiin.
      loadfile: A boolean, whether to bring in content from an external file.
      fsf: A string, the path to the 'function source file' containing the function code.
      docadd: A boolean, whether to add in a template docstring for function documentation.

  Returns:
    NULL: There are no returns, a .py file is created.
  """
  import os
  from startpypack import getlines
  from startpypack import replacelines
  from startpypack import writefile
  from startpypack import addlines

  # Define the installation location of this function
  this_dir, this_filename = os.path.split(__file__)

  # Define the location of the function file
  fdir = os.path.join(wdir, pname, pname, pname, (fname+'.py'))

  # Evaluate what kind of procedure is being done:

  #  1. NOT loading in any content from an external file:
  if not loadfile:
    #print("Making from internal file...")
    #print(pname)
    #print(fname)
    # Load lines of internal package function file
    flines = getlines(os.path.join(this_dir, "files/data/exfunc.py"))

    # Find/Replace to insert name of new function
    frlines = replacelines(flines,'[[funcname]]',fname)

    # Create 'blank' standard template file w/ function name inserted
    writefile(fdir,frlines)


  #  2. Loading content from an external file:
  # 2a. File includes docstring, does not need to add one
  else:
    #print("Not making, loading from external file...")
    #print(pname)
    #print(fname)
    #print(fsf)
    # So, grab the lines from the file
    flines = getlines(os.path.join(this_dir, fsf))

    # 2a. File does not include docstring, needs to add one
    if docadd:
      #print("And, adding in a missing docstring template for documentation...")
      # Read in the docstring lines from an internal package file
      dlines = getlines(os.path.join(this_dir, "files/data/exdocstring.py"))

      # With lines from the file above, add a blank template docstring lines to 2nd line
      flines = addlines(flines,1,dlines)

    # Now write the lines (modified with docstring or not) into a new file
    writefile(fdir,flines)
 

  # Define the location of the __init__.py file that needs to be updated
  ifile = os.path.join(wdir, pname, pname, pname, '__init__.py')

  # Get the lines of the __init.py file that needs to be updated
  ilines = getlines(ifile)

  # Define the import line for this function
  ail = 'from ' + pname + '.' + fname + ' import ' + fname + "\n"

  # Add in the import line for this function
  ilines = addlines(ilines,3,ail)

  # Write the newly updated lines back into the __init__.py file
  writefile(ifile,ilines)

