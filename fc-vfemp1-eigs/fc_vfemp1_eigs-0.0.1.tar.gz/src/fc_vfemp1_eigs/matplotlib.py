import numpy as np
import matplotlib.pyplot as plt
import fc_simesh_matplotlib.siMesh as siplt
from fc_tools.matplotlib import set_axes_equal,DisplayFigures
from fc_tools.colors import selectColors

def ploteigs(Th,eigValues,eigVectors,**kwargs):
  modulus=kwargs.pop('modulus',True)
  split=kwargs.pop('split',False)
  title=kwargs.pop('title','')
  detail=kwargs.pop('detail',False)
  #m=eigVectors.shape[0]//Th.nq
  #assert m*Th.nq==eigVectors.shape[0]
  assert eigValues.shape[0]==eigVectors.shape[1]
       
  def ploteig(Th,V,**kwargs):
    colorbar=kwargs.pop('colorbar',False)
    format=kwargs.pop('format','%.3f')
    scale=kwargs.pop('scale',True) # scale each eigenvector in [-1,1]
    if scale:
      amax=np.max(np.abs(V))
      V=V/amax
      vmin=-1;vmax=1
    else:
      vmin=V.min();vmax=V.max()
    h=siplt.plot(Th,V,vmin=vmin,vmax=vmax,**kwargs)
    if colorbar:
      plt.colorbar(h,format=format)
    siplt.plotiso(Th,V,isorange=[0],color='Black',linewidth=2)
    set_axes_equal()
    plt.axis('off')
    
  def eigenvalue2str(eigenvalue,i):
    if abs(eigenvalue.imag)<1e-14:
      return '$\lambda_{%d}=%.4f$'%(i,eigenvalue.real)
    else:
      return '$\lambda_{%d}=(%.4f,%.4f)$'%(i,eigenvalue.real,eigenvalue.imag)
    
  def strtitle(eigenvalue,i,title,streigfun,detail):
    if detail:
      if title=='':
        return '%s %s'%(streigfun,eigenvalue2str(eigenvalue,i))
      else:
        return '%s: %s %s'%(title,streigfun,eigenvalue2str(eigenvalue,i))
    else:
      return '%s'%(eigenvalue2str(eigenvalue,i))
  
  n=eigValues.shape[0]
  isComplex=np.max(np.abs(eigVectors.imag))>1e-14
  for i in range(n):
    if isComplex:
      if modulus:
        plt.figure()
        V=np.abs(eigVectors[:,i])
        ploteig(Th,V,**kwargs)
        #plt.title('%s: Eigenfunction modulus for %s'%(title,eigenvalue2str(eigValues[i],i+1)))
        plt.title(strtitle(eigValues[i],i+1,title,'Eigenfunction modulus for',detail))
        #ax1.colorbar()
        set_axes_equal();plt.axis('off')
      else:  
        if split:
          plt.figure()
          ploteig(Th,eigVectors[:,i].real,**kwargs)
          #plt.title('%s: Eigenfunction (real part) for %s'%(title,eigenvalue2str(eigValues[i],i+1)))
          plt.title(strtitle(eigValues[i],i+1,title,'Eigenfunction (real part) for',detail))
          set_axes_equal();plt.axis('off')
          plt.figure()
          ploteig(Th,eigVectors[:,i].imag,**kwargs)
          #plt.title('%s: Eigenfunction (imag part) for %s'%(title,eigenvalue2str(eigValues[i],i+1)))
          plt.title(strtitle(eigValues[i],i+1,title,'Eigenfunction (imag part) for',detail))
          set_axes_equal();plt.axis('off')
        else:
          f, (ax1, ax2) = plt.subplots(1, 2)
          plt.sca(ax1)
          ploteig(Th,eigVectors[:,i].real,**kwargs)
          #ax1.title('%s: Eigenfunction (real part) for %s'%(title,eigenvalue2str(eigValues[i],i+1)))
          ax1.title(strtitle(eigValues[i],i+1,title,'Eigenfunction (real part) for',detail))
          set_axes_equal();plt.axis('off')
          plt.sca(ax2)
          ploteig(Th,eigVectors[:,i].imag,**kwargs)
          #ax2.title('%s: Eigenfunction (imag part) for %s'%(title,eigenvalue2str(eigValues[i],i+1)))
          ax2.title(strtitle(eigValues[i],i+1,title,'Eigenfunction (imag part) for',detail))
          set_axes_equal();plt.axis('off')
    else:    
      plt.figure()
      ploteig(Th,eigVectors[:,i].real,**kwargs)
      #plt.title('%s: Eigenfunction (real part) for %s'%(title,eigenvalue2str(eigValues[i],i+1)))
      plt.title(strtitle(eigValues[i],i+1,title,'Eigenfunction (real part) for',detail))
      set_axes_equal();plt.axis('off')
  
def plot_orders(res_order):
  Lh=res_order['Lh']
  Lu_errL2=res_order['Lu_errL2'];Lu_errH1=res_order['Lu_errH1']
  L_eVal=res_order['L_eVal']
  NumEigs=L_eVal.shape[1]
  colors = selectColors(NumEigs)
  hds=[]
  plt.close('all')
  plt.ion()
  plt.figure(1)
  for i in range(NumEigs):
    hd=plt.loglog(Lh,L_eVal[:,i],color=colors[i],label='$\lambda_{%d}$'%(i+1))
  plt.loglog(Lh,0.1*Lh,color=(0,0,0),label='$O(h)$',ls=':',marker='s')
  plt.loglog(Lh,Lh**2,color=(0,0,0),label='$O(h^2)$',ls='-.',marker='o')
  plt.legend(bbox_to_anchor=(0.95, 1), loc=2, borderaxespad=0.)
  plt.xlabel('$h$')
  plt.ylabel('$E_\lambda(h)$')
  plt.title('Relative error for eigenvalues')
  plt.figure(2)
  for i in range(NumEigs):
    hd=plt.loglog(Lh,Lu_errL2[:,i],color=colors[i],label='$\lambda_{%d}$'%(i+1))
  plt.loglog(Lh,0.1*Lh,color=(0,0,0),label='$O(h)$',ls=':',marker='s')
  plt.loglog(Lh,Lh**2,color=(0,0,0),label='$O(h^2)$',ls='-.',marker='o')
  plt.legend(bbox_to_anchor=(0.95, 1), loc=2, borderaxespad=0.)
  plt.xlabel('$h$')
  plt.ylabel('$E_{L^2}(h)$')
  plt.title('Relative $L^2$-error for eigenfunctions')
  plt.figure(3)
  for i in range(NumEigs):
    hd=plt.loglog(Lh,Lu_errH1[:,i],color=colors[i],label='$\lambda_{%d}$'%(i+1))
  plt.loglog(Lh,0.1*Lh,color=(0,0,0),label='$O(h)$',ls=':',marker='s')
  plt.loglog(Lh,Lh**2,color=(0,0,0),label='$O(h^2)$',ls='-.',marker='o')
  plt.legend(bbox_to_anchor=(0.95, 1), loc=2, borderaxespad=0.)
  plt.xlabel('$h$')
  plt.ylabel('$E_{H^1}(h)$')
  plt.title('Relative $H^1$-error for eigenfunctions')
  
def plot_aligned_eigenvectors(Th,V1,V2,**kwargs):
  title=kwargs.pop('title',None)
  aVecs=elib.aligned_eigenvectors(Th,V1,V2,**kwargs)
  for V in aVecs:
    if V is not None:
      plt.figure()
      siplt.plot(Th,V,vmin=-1,vmax=1,cmap='viridis')
      #plt.colorbar()
      siplt.plotiso(Th,V,isorange=[0],color='LightGray',linewidth=2)
      set_axes_equal()
      plt.axis('off')
      if title is not None:
        plt.title(title)
  
def plot_displacement(Th,U,**kwargs):
  assert Th.dim==2
  import matplotlib.pyplot as plt
  import fc_simesh_matplotlib.siMesh as siplt
  from fc_tools.matplotlib import set_axes_equal
  import copy
  #L=np.max(Th.bbox[[1,3]]-Th.bbox[[0,2]])
  #max_displacement=kwargs.pop('max_displacement',L/20.)
  colorbar=kwargs.pop('colorbar',False)
  #title=kwargs.pop('title',None) 
  magnitude=kwargs.pop('magnitude',None) 
  #mU=np.sqrt(U[0]**2+U[1]**2)
  #for k in range(2):
    #U[k]=max_displacement*U[k]/np.max(mU)
  Thm=copy.deepcopy(Th)
  Thm.move(U)
  if magnitude is None:
    siplt.plotmesh(Thm,**kwargs)
  else:
    siplt.plot(Thm,magnitude,**kwargs)
  if colorbar:
    plt.colorbar()
  siplt.plotmesh(Thm,d=1,color='black')
  set_axes_equal()
  plt.axis('off')
  #if isinstance(title,str):
    #plt.title('freq[%d]=$%.3f$Hz, [max.=%g]'%(i+1,freq[i],max_displacement))  
  #elif isinstance(title,str):
    #plt.title(title)

def sequence_images(Th,eigVal,U,**kwargs):
  import matplotlib.pyplot as plt
  from fc_tools.others import mkdir_p
  from fc_tools.matplotlib import set_axes_equal,SaveFigAsFile
  import os
  from fc_tools.others import latex_tag
  assert Th.dim==2
  L=np.max(Th.bbox[[1,3]]-Th.bbox[[0,2]])
  filebase=kwargs.pop('filebase','test')
  max_displacement=kwargs.pop('max_displacement',L/20.) # in meter
  magnification=kwargs.pop('magnification',3) # in meter
  directory=kwargs.pop('directory','.')
  tag_latex=kwargs.pop('tag_latex',None)
  axis=kwargs.pop('axis',None)
  Nf=kwargs.pop('Nf',25)
  if not os.path.isdir(directory):
    mkdir_p(directory)
  mU=np.sqrt(U[0]**2+U[1]**2)
  for l in range(Th.dim):
    U[l]=max_displacement*U[l]/np.max(mU)
  mU=np.sqrt(U[0]**2+U[1]**2)
  plt.close('all')
  plt.ion()
  t=np.linspace(0,2*np.pi,Nf)
  V=Th.dim*[None]
  for k in range(Nf):
    st=np.sin(t[k])
    for l in range(Th.dim):
      V[l]=st*U[l]
    fig=plt.figure()
    plot_displacement(Th,V,magnitude=mU,**kwargs)
    if axis is None:
      axis=np.array(plt.axis())
    else:
      plt.axis(axis)
    if filebase is None or len(filebase)==0:
      File='%s%s%5d'%(directory,os.sep,k+1)
    else:
      File='%s%s%s_%5d'%(directory,os.sep,filebase,k+1)
    File=File.replace(' ','0')
    print('save figure in %s'%File)
    SaveFigAsFile(fig.number,File,scale=magnification)
    plt.close(fig.number)
    if tag_latex is not None:
      latex_tag(os.getcwd()+os.sep+File+'.png',os.getcwd()+os.sep+File+'.jpg',tag_latex)
  
import fc_vfemp1_eigs.lib as elib