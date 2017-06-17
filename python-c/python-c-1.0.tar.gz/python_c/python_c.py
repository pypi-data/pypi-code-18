#!/usr/bin/env python
import sys, os, os.path

def main():
  if any([x in sys.argv for x in ['--help', '--h', '-help', '-h']]) or len(sys.argv) < 2:
    print "usage: python-c [ file[.py]|dir ] 'some python code'"
    print " (specifying a directory will load all python files in the directory)"
    print " (specifying no directory will load the current directory)"
    return
  # determine modules
  if len(sys.argv) == 2:
    pyloc_str = '.'; runcode = ' '.join(sys.argv[1:]);
  else:
    pyloc_str = sys.argv[1]; runcode = ' '.join(sys.argv[2:]);
  pylocs = pyloc_str.split(',')
  pyfiles = []
  for pyloc in pylocs:
    if os.path.isdir(pyloc):
      dir_items = [os.path.join(pyloc, x) for x in os.listdir(pyloc)]
      pyfiles.extend([x for x in dir_items if os.path.isfile(x) and x.endswith('.py')])
    else:
      pyfiles.append(pyloc)
  # import the module
  for pyfile in pyfiles:
    fdir, fname = os.path.split(pyfile)
    sys.path.insert(0, fdir)
    module = __import__(fname[:-3] if fname.endswith('.py') else fname, globals(), locals(), ['*'])
    for k in dir(module):
      locals()[k] = getattr(module, k)
  try:
    # try to run as eval
    compile(runcode, '<stdin>', 'eval')
    ret = eval(runcode)
    # print the result if any
    if ret:
      print ret
  except SyntaxError:
    # must run exec
    exec(runcode)

if __name__ == '__main__':
    main()
