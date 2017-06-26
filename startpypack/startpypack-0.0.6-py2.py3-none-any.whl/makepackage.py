#def makepackage(pname, wdir='.'):
def makepackage(pname, wdir='.', bbf=[], **kwargs):
  """This function creates the folder and file structure of a new python package.

  Args:
      pname: A string, the name of the python package to create.
      wdir: A string, the path of the directory to create the python package in.
      bbf: A list of strings, the names of functions to create additional barebones template files for.
      **kwargs: Additional arguments to pass into the 'pkmkfiles()' function

  Returns:
    NULL: There are no returns, a selection of folders and files is created.
  """
  import os
  from startpypack import pkdirs
  from startpypack import pkmkfiles
  from startpypack import mkfunc

  # Make the directory structure
  pkdirs(pname=pname,wdir=wdir)

  # Make the standard files within the directory structure
  pkmkfiles(pname=pname,wdir=wdir,**kwargs)

  # Do standard functions (if functions not specified)
  if len(bbf)==0:

    # Define standard function names
    fn = ['func1','func2']

    # Locate standard function contents
    this_dir, this_filename = os.path.split(__file__)
    fl1 = os.path.join(this_dir, "files/data/func1.py")
    fl2 = os.path.join(this_dir, "files/data/func2.py")
    fl = [fl1,fl2]

    # Make function files
    mkfunc(pname=pname, fname=fn[0], wdir=wdir, loadfile=True, fsf=fl[0], docadd=True)
    mkfunc(pname=pname, fname=fn[1], wdir=wdir, loadfile=True, fsf=fl[1], docadd=True)

  # Make barebones function templates (if functions specified)
  else:

    for i in bbf:
      mkfunc(pname=pname, fname=i, wdir=wdir)

