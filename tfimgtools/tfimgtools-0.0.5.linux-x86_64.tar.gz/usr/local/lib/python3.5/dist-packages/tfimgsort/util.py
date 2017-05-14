"""Utilities for manipulating directories and files.

These utilities are convenience methods for use by the
tfimgsort driver.
"""


import os
import sys
import ntpath
from functools import reduce

def stringify(lst):
  """Turns a list into a csv string.

  Parameters:

  lst : list
    the list to be turned into a csv string
  """
  string = reduce((lambda x, y: str(x) + ',' + str(y)), lst)
  string += '\n'
  return string

def write_csv_line(csv_file, lst):
  """Given an open file, and a string, writes a csv line to disk.

  Parameters
  ----------

  csv_file : file
    An open file to be written to
  lst : list
    a list of things to be written as a csv line
  """
  csv_file.write(stringify(lst))

def ls(img_dir):
  """Given a path returns a list of the child subdirectories."""
  return [os.path.join(img_dir, img) for img in os.listdir(img_dir)]

def mv(from_file, to_dir):
  """Given a non-relative file, moves it to a preferred directory.

  Parameters
  ----------

  from_file : string
    a non-relative path to a file
  to_dir : string
    the desired directory to move to
  """
  base = ntpath.basename(from_file)
  os.rename(from_file, os.path.join(to_dir, base))

def setup_dirs(labels, directory):
  """Given a list of labels creates corresponding subdirectories in the target directory.

  Given the labels ['a', 'b', 'c'] and the directory '1' the following directory structure
  would be created.

  1/
  ├── a
  ├── b
  └── c

  If the parent directory does not exist it, and it's parents if necessary, will be created.

  Parameters
  ----------

  labels : list
    the child directories to be created
  directory : string
    the parent directory to place the children under
  """
  if not os.path.isdir(directory):
    os.makedirs(directory)

  if os.path.isdir(directory):
    if len(os.listdir(directory)):
      print("ERROR: %s needs to be an empty directory." % (directory))
      sys.exit(1)

  sub_dirs = list(map((lambda x: os.path.join(directory, x)), labels))

  for d in sub_dirs:
    os.makedirs(d)
