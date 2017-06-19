import numpy as np

def plot_displacement(Th,U,**kwargs):
  assert Th.dim==3
  from mayavi import mlab
  import fc_simesh_mayavi.siMesh as simlab
  from fc_tools.mayavi import mlab_latex3D
  import copy
  colorbar=kwargs.pop('colorbar',False)
  magnitude=kwargs.pop('magnitude',None)
  iso=kwargs.pop('iso',False)
  Thm=copy.deepcopy(Th)
  Thm.move(U)
  if magnitude is None:
    simlab.plotmesh(Thm,d=2,**kwargs)
  else:
    simlab.plot(Thm,magnitude,d=2,**kwargs)
    simlab.plotiso(Thm,magnitude,d=2,color='white',line_width=2)
  if colorbar:
    mlab.colorbar()
  
  
# plot_mayavi_video(Th,eigVal,eigVec,magnification=6,Nf=50,filebase='videos/tidal_turbine_mod0')
def sequence_images(Th,eigVal,U,**kwargs):
  from fc_tools.others import mkdir_p
  from mayavi import mlab
  import fc_simesh_mayavi.siMesh as simlab
  import os
  from fc_tools.others import latex_tag
  assert Th.dim==3
  L=np.max(Th.bbox[[1,3,5]]-Th.bbox[[0,2,4]])
  filebase=kwargs.pop('filebase','test')
  max_displacement=kwargs.pop('max_displacement',L/20.) # in meter
  magnification=kwargs.pop('magnification',3)
  size=kwargs.pop('size',(1024,768))
  scalefont=kwargs.pop('scalefont',3)
  scaleview=kwargs.pop('scaleview',1)
  directory=kwargs.pop('directory','.')
  tag_latex=kwargs.pop('tag_latex',None)
  view=kwargs.pop('view',None)
  Nf=kwargs.pop('Nf',25)
  if not os.path.isdir(directory):
    mkdir_p(directory)
  mU=np.sqrt(U[0]**2+U[1]**2+U[2]**2)
  for l in range(3):
    U[l]=max_displacement*U[l]/np.max(mU)
  mU=np.sqrt(U[0]**2+U[1]**2+U[2]**2)
  mlab.close(all=True)
  h=2*np.pi/Nf
  t=np.arange(0,2*np.pi,h)
  
  V=Th.dim*[None]
  for k in range(Nf):
    st=np.sin(t[k])
    print('st=%.5f'%st)
    for l in range(3):
      V[l]=st*U[l]
    mlab.figure(size=size)
    plot_displacement(Th,V,magnitude=mU,**kwargs)
    if view is None:
      view=mlab.view()
    mlab.view(azimuth=view[0], elevation=view[1], distance=scaleview*view[2], focalpoint=view[3])
    if filebase is None or len(filebase)==0:
      File='%s%s%5d'%(directory,os.sep,k+1)
    else:
      File='%s%s%s_%5d'%(directory,os.sep,filebase,k+1)
    File=File.replace(' ','0')
    print('save figure in %s'%File)
    mlab.savefig(File+'.png',magnification=magnification)
    mlab.close()
    if tag_latex is not None:
      latex_tag(os.getcwd()+os.sep+File,os.getcwd()+os.sep+File+'.jpg',tag_latex,scalefont=scalefont)

