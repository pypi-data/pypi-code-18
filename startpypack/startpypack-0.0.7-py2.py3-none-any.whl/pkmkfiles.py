def pkmkfiles(pname,wdir='.',pd='does some cool stuff',pu='http://engineering.case.edu/centers/sdle/',vn='0.0.1',an='author name',ae='author@email',pl='GPL3'):
  """A function to populate a python package folder structure in a specified directory with initial files.

  Args:
      pname: A string, the name of the package to create.
      wdir: A string, the path to where to create the python package folder structure. Defaults to '.'.
      pd: A string, the package description.  Defaults to 'does some cool stuff'.
      pu: A string, the package url.  Defaults to 'www.python.org/'.
      vn: A string, the package version number.  Defaults to '0.0.1'.
      an: A string, the author name.  Defaults to 'author name'.
      ae: A string, the author email.  Defaults to 'author@email.com'.
      pl: A string, the package license.  Defaults to 'GPL3'.
  Returns:
      NULL: There are no returns, a selection of files is created.
  """
  import os
  from startpypack import getlines
  from startpypack import writefile
  from startpypack import replacelines

  # File list:
  #  Second level folder
  #    build.py (l1bf - 'build file') (ok as is)
  #    install.py (l1if - 'install file') (requires modification)
  #    upload.py (l1uf - 'upload file') (ok as is)
  #    README.rst (l1rf - 'readme file') (requires modification)
  #    setup.py (l1sf - 'setup file') (requires modification)
  #    MANIFEST.py (l1mf - 'manifest file') (requires modification)
  #  Third level folder
  #    __init__.py (l2if - 'init file') (ok as is for now, modify when adding funcs)

  # Get installation location of this package
  this_dir, this_filename = os.path.split(__file__)
  # Get lines from stored versions of files (with replace targets)
  dpath = os.path.join(this_dir, "files/data/build.py")
  l1bf = getlines(dpath)
  dpath = os.path.join(this_dir, "files/data/install.py")
  l1if = getlines(dpath)
  dpath = os.path.join(this_dir, "files/data/upload.py")
  l1uf = getlines(dpath)
  dpath = os.path.join(this_dir, "files/data/README.rst")
  l1rf = getlines(dpath)
  dpath = os.path.join(this_dir, "files/data/setup.py")
  l1sf = getlines(dpath)
  dpath = os.path.join(this_dir, "files/data/MANIFEST.in")
  l1mf = getlines(dpath)
  dpath = os.path.join(this_dir, "files/data/__init__.py")
  l2if = getlines(dpath)

  # Make 'target-replaced' versions, using the input arguments to this function

  # targets to replace - variable name:
  #  [[packagename]] - pn
  #  [[packagedescription]] - pd
  #  [[packageurl]] - pu
  #  [[versionnumber]] - vn
  #  [[authorname]] - an
  #  [[authoremail]] - ae
  #  [[packagelicense]] - pl

  # install.py section
  l1ifr = l1if
  tar = '[[packagename]]'
  l1ifr = replacelines(l1ifr,tar,pname)

  # README.rst section
  l1rfr = l1rf
  tar = '[[packagename]]'
  l1rfr = replacelines(l1rfr,tar,pname)

  # setup.py section
  l1sfr = l1sf
  tar = '[[packagename]]'
  l1sfr = replacelines(l1sfr,tar,pname)
  tar ='[[packagedescription]]'
  l1sfr = replacelines(l1sfr,tar,pd)
  tar ='[[packageurl]]'
  l1sfr = replacelines(l1sfr,tar,pu)
  tar ='[[versionnumber]]'
  l1sfr = replacelines(l1sfr,tar,vn)
  tar ='[[authorname]]'
  l1sfr = replacelines(l1sfr,tar,an)
  tar ='[[authoremail]]'
  l1sfr = replacelines(l1sfr,tar,ae)
  tar ='[[packagelicense]]'
  l1sfr = replacelines(l1sfr,tar,pl)

  # MANIFEST.in section
  l1mfr = l1mf
  tar = '[[packagename]]'
  l1mfr = replacelines(l1mfr,tar,pname)

  # __init__.py section
  l2ifr = l2if
  tar = '[[packagedescription]]'
  l2ifr = replacelines(l2ifr,tar,pd)

  # Make the paths for the new versions of the files
  l1bfp =wdir + '/' + pname + '/' + pname + '/build.py'
  l1ifp =wdir + '/' + pname + '/' + pname + '/install.py'
  l1ufp =wdir + '/' + pname + '/' + pname + '/upload.py'
  l1rfp =wdir + '/' + pname + '/' + pname + '/README.rst'
  l1sfp =wdir + '/' + pname + '/' + pname + '/setup.py'
  l1mfp =wdir + '/' + pname + '/' + pname + '/MANIFEST.in'
  l2ifp =wdir + '/' + pname + '/' + pname + '/' + pname + '/__init__.py'

  # Write the replaced versions into new versions of the files
  writefile(l1bfp,l1bf)
  writefile(l1ufp,l1uf)

  writefile(l1ifp,l1ifr)
  writefile(l1rfp,l1rfr)
  writefile(l1sfp,l1sfr)
  writefile(l1mfp,l1mfr)
  writefile(l2ifp,l2ifr)
