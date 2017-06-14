import types,inspect,numpy
from inspect import getsource
#from dill.source import getsource
import os,sys,tempfile,shutil,subprocess
def isModuleFound(name,**kwargs):
  verbose=kwargs.get('verbose',False)
  isOk=True
  try:
    __import__(name)
  except ImportError:
    isOk=False
    if verbose:
      print('%s is not founded!'%name)
  return isOk

def LabelBaseName(dim,d):
  if (d==dim):
    return r"\Omega"
  if (d+1==dim):
    return r"\Gamma"
  if (d+2==dim):
    return r"\partial\Gamma"
  if (d+3==dim):
    return r"\partial^2\Gamma"
    
    
def LabelBaseNameSimp(dim,d,ds):
  if (d==dim):
    return LabelBaseName(dim,ds)
  if (d+1==dim):
    return LabelBaseName(dim,ds+1)
  if (d+2==dim):
    return LabelBaseName(dim,ds+2)
  if (d+3==dim):
    return LabelBaseName(dim,ds+3)
  
def print_packages(packages):
  #packages=['fc_tools','fc_hypermesh','fc_oogmsh','fc_simesh','fc_matplotlib4mesh']
  for name in packages:
    print('package %s:'%name)
    if isModuleFound(name):
      f=__import__(name)
      print('  path    : %s'%f.__path__[0])
      print('  version : %s'%f.__version__)
    else:
      print('  not found')
      
def is_lambda_function(obj):
  return isinstance(obj, types.LambdaType) and obj.__name__ == "<lambda>"    

def is_def_function(obj):
  return isinstance(obj, types.FunctionType) and obj.__name__ != "<lambda>"   

def is_vectorized_function(obj):
  return isinstance(obj,numpy.lib.function_base.vectorize)

def is_function(obj):
  return is_lambda_function(obj) or is_def_function(obj) or is_vectorized_function(obj)
    
def func2str(u):
  #assert is_function(u), 'invalid type : %s given'%str(type(u))
  if is_lambda_function(u):
    Str=getsource(u)#.replace('\n','')
    #i=Str.find('lambda')
    #Str=Str[i:-1]
    #i=Str.find(']')
    #if i>=0:
      #Str=Str[:i]
    #i=Str.find('=')+1
    return Str
  if is_def_function(u):
    Str=getsource(u)
    return Str[:-1]
  if is_vectorized_function(u):
    return func2str(u.pyfunc)
  return ''

class TemporaryDirectory(object):
  def __init__(self):
      self.tmp_dir = tempfile.mkdtemp()

  def __enter__(self):
      return self.tmp_dir

  def __exit__(self, type, value, traceback):
      shutil.rmtree(self.tmp_dir)
      self.tmp_dir = None

def latex_tag(imagein,imageout,string,**kwargs):
  density=kwargs.pop('density',100)
  scalefont=kwargs.pop('scalefont',5)
  latex_string = '''
    \\scalefont{%g}
    \\begin{tikzpicture}
    \\node[anchor=south west,inner sep=0] (image) at (0,0,0) {\\includegraphics{%s}};
    %s
    \\end{tikzpicture}
  '''.strip()
  template = '''
  \\documentclass[border=2mm,margin=10pt]{standalone}
  \\usepackage{anyfontsize}
  \\usepackage{scalefnt}
  \\usepackage[x11names,svgnames]{xcolor}
  \\usepackage{tikz}
  \\usepackage{pagecolor}
  \\begin{document}
      %s 
  \\end{document}
  '''.strip()
  S=latex_string % (scalefont,imagein,string)
  document = template % (S)
  with TemporaryDirectory() as tmp_dir:
      print(tmp_dir)
      with open(os.path.join(tmp_dir, 'math.tex'), 'w') as math_file:
          math_file.write(document)
      with open(os.devnull, 'w') as devnull:
          subprocess.check_call(['pdflatex', 'math.tex'], cwd=tmp_dir, stdout=devnull, stderr=devnull)
          #subprocess.check_call(['dvipng', '-bg', 'Transparent', '-D', str(dpi), '-T', 'tight', '-o', 'math.png',
                                  #'math.dvi'], cwd=tmp_dir, stdout=devnull, stderr=devnull)
          subprocess.check_call(['convert', '-density',str(density),'math.pdf', imageout], cwd=tmp_dir, stdout=devnull, stderr=devnull)
   
# kwargs={'cwd': ...}
def run_command(shell_cmd,**kwargs):
  verbose=kwargs.pop('verbose',0)
  try:
    out=None
    out=subprocess.check_output(shell_cmd,shell=True, stderr=subprocess.STDOUT,**kwargs)
  except subprocess.CalledProcessError:
    print('***[fc_tools]: Execution of %s failed!\n'%shell_cmd)
    if out is not None:
      Out=out.decode("utf-8")
      for line in Out.splitlines():
        print(line)
      sys.exit()
    else:
      print('***[fc_tools]: Try manually to see error messages')
      sys.exit()
  if verbose>0:
    if out is not None:
      Out=out.decode("utf-8")
      for line in Out.splitlines():
        print(line)
      print('  -> done!')
   
def latex_overlay(imageout,string,**kwargs):
  density=kwargs.pop('density',100)
  scalefont=kwargs.pop('scalefont',10)
  pagecolor=kwargs.pop('pagecolor','green')
  latex_string = '''
    \\pagecolor{%s}
    \\scalefont{%g}
    \\begin{tikzpicture}
    %s
    \\end{tikzpicture}
  '''.strip()
  template = '''
  \\documentclass{standalone}
  \\usepackage{anyfontsize}
  \\usepackage{scalefnt}
  \\usepackage[x11names,svgnames]{xcolor}
  \\usepackage{tikz}
  \\usepackage{pagecolor}
  \\begin{document}
      %s 
  \\end{document}
  '''.strip()
  S=latex_string % (pagecolor,scalefont,string)
  document = template % (S)
  with TemporaryDirectory() as tmp_dir:
      print(tmp_dir)
      with open(os.path.join(tmp_dir, 'math.tex'), 'w') as math_file:
          math_file.write(document)
      shutil.copyfile(tmp_dir+os.sep+'math.tex', imageout+'.tex')
      run_command('pdflatex math.tex',cwd=tmp_dir,**kwargs)
      shutil.copyfile(tmp_dir+os.sep+'math.pdf', imageout+'.pdf')
      run_command('convert -trim -transparent white -density '+str(density)+' '+imageout+'.pdf '+imageout+'.png',**kwargs)

def build_video(input_format,output):
  import os
  import tempfile
  import shutil
  import subprocess
  # avconv -f image2 -i tmp/%05d.png output.avi
  # avconv -i concat:"output.avi|output.avi|output.avi|output.avi|output.avi|output.avi|output.avi" -c copy output1.avi
  from fc_tools.others import TemporaryDirectory
  verbose=1
  with TemporaryDirectory() as tmp_dir:
    tmp_file=tmp_dir+os.sep+'tmp.avi'
    print('write in %s'%tmp_file)
    #with open(os.devnull, 'w') as devnull:
      #subprocess.check_call(['avconv', '-f', 'image2', '-r' , '50', '-i' , input_format , tmp_file], cwd=tmp_dir, stdout=devnull, stderr=devnull)
      #subprocess.check_call(['avconv', '-i', concat, '-c', 'copy' ,output], cwd=tmp_dir, stdout=devnull, stderr=devnull)
  #print('Creating video %s'%output)
    avconv_cmd="avconv -f image2 -r 50 -i %s %s"%(input_format,tmp_file)
    try:
      out=None
      out=subprocess.check_output(avconv_cmd,shell=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError:
      print('***[fc_vfemp1_eigs]: Execution of %s failed!\n'%avconv_cmd)
      if out is not None:
        Out=out.decode("utf-8")
        for line in Out.splitlines():
          print(line)
        sys.exit()
      else:
        print('***[fc_vfemp1_eigs]: Try manually to see error messages')
        sys.exit()
    if verbose>0:
      if out is not None:
        Out=out.decode("utf-8")
        for line in Out.splitlines():
          print(line)
        print('  -> done!')
    # avconv -i concat:"output.avi|output.avi|output.avi|output.avi|output.avi|output.avi|output.avi" -c copy output1.avi
    strc='|%s'%tmp_file
    concat='concat:"%s%s"'%(tmp_file,9*strc)
    avconv_cmd="avconv -i %s -c copy %s"%(concat,output)
    try:
      out=None
      out=subprocess.check_output(avconv_cmd,shell=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError:
      print('***[fc_vfemp1_eigs]: Execution of %s failed!\n'%avconv_cmd)
      if out is not None:
        Out=out.decode("utf-8")
        for line in Out.splitlines():
          print(line)
        sys.exit()
      else:
        print('***[fc_vfemp1_eigs]: Try manually to see error messages')
        sys.exit()
    if verbose>0:
      if out is not None:
        Out=out.decode("utf-8")
        for line in Out.splitlines():
          print(line)
        print('  -> done!')
    print('Creating video %s'%output)

def mkdir_p(path):
  import os
  try:
      os.makedirs(path)
  except OSError as exc: # Python >2.5
      if exc.errno == errno.EEXIST and os.path.isdir(path):
          pass
      else: raise