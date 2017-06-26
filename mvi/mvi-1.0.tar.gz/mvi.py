#! /usr/bin/env python3

import os, tempfile, itertools

__version__ = '1.0'


def proceed(*options):
  '''Wait for keyboard input to select option, return index.

  Options can be specifide by either the first character or the full word. No
  checks are performed to confirm that all options have a uniquely identifying
  first character.'''

  while True:
    answer = input('proceed {}? '.format('/'.join(options)))
    for i, option in enumerate(options):
      if answer in (option, option[0]):
        return i


def getrenames(init={}):
  '''Invoke editor to create a rename dictionary.

  A temporary file is created with the alphabetically ordered file and
  directory listing of the current working directory, and opened with the
  default system editor. At exit the list is checked for errors and returned as
  an old->new dictionary limited to changes.'''

  oldnames = sorted(os.listdir())
  editor = os.environ.get('EDITOR', 'vim')
  fd, tmp = tempfile.mkstemp()
  try:
    os.fdopen(fd, 'w').write('\n'.join(init.get(name,name) for name in oldnames))
    while True:
      if os.system(editor + ' ' + tmp) != 0:
        print('editor returned with non-zero status')
      with open(tmp, 'r') as fid:
        newnames = fid.read().splitlines()
      for i, (old,new) in enumerate(itertools.zip_longest(oldnames, newnames, fillvalue='?')):
        if old != new:
          print('line {}: {} -> {}'.format(i+1, old, new))
      if len(newnames) != len(oldnames):
        print('error: invalid length')
      elif len(set(newnames)) < len(newnames):
        print('error: duplicate names')
      elif not all(newnames):
        print('error: empty filenames')
      elif oldnames == newnames or proceed('yes', 'no') == 0:
        return {old: new for old, new in zip(oldnames, newnames) if old != new}
      assert proceed('edit', 'quit') == 0, 'aborted.'
  finally:
    os.remove(tmp)


def poprename(renames):
  '''Pop a dictionary item and perform the rename operation.

  The first rename operation is performed that has a free destination path. If
  renames occur in a "a->b->..->a" cycle then a temporary path is introduced
  and added to the dictionary of renames. The rename item is popped only after
  the move operation is succesfully completed to ensure that the dictionary
  remains in sync with the on-disk state at all times. Returns True in case of
  a successful move, or False otherwise.'''

  # get random starting point
  assert renames, 'nothing to rename'
  for name in renames:
    break

  # follow rename chain to find either a free target or a closed loop
  cycle = [name]
  while renames[name] in renames and renames[name] != cycle[0]:
    name = renames[name]
    cycle.append(name)

  # modify target in case of closed loop
  target = renames[name]
  if target == cycle[0]:
    print('cycle detected:', ' '.join(cycle))
    while os.path.exists(target):
      target += '_'

  # check that target is free
  assert not os.path.exists(target), 'cannot rename {} to {}: target exists'.format(name,target)

  # perform rename
  os.renames(name, target)

  # update dictionary
  print('renamed {} to {}'.format(name, target))
  if target != renames[name]: # closed loop
    renames[target] = renames[name]
  del renames[name]


def rename():
  '''Coordinate aqcuisition and execution of renames.

  Call getrenames to obtain text editor input and feed the resuling renames
  dictionary into poprename until empty. In case of errors, repeat the above,
  while feeding the leftover renames back into getrenames to ensure that edits
  are not lost.'''

  renames = getrenames()
  while renames:
    try:
      poprename(renames)
    except Exception as e:
      print(e)
      assert proceed('edit', 'quit') == 0, 'aborted.'
      renames = getrenames(init=renames)
