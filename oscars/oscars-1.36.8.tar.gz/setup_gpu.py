import os
#from distutils.core import setup, Extension
from setuptools import setup, Extension

os.environ["CC"] = "g++"
os.environ["CXX"] = "g++"

moduleOSCARSSR = Extension('oscars.sr',
                      include_dirs = ['include'],
                      sources = ['src/OSCARSSR.cc',
                                 'src/OSCARSSR_Python.cc',
                                 'src/T3DScalarContainer.cc',
                                 'src/TField3D_Grid.cc',
                                 'src/TField3D_Gaussian.cc',
                                 'src/TFieldContainer.cc',
                                 'src/TField3D_IdealUndulator.cc',
                                 'src/TField3D_UniformBox.cc',
                                 'src/TFieldPythonFunction.cc',
                                 'src/TParticleA.cc',
                                 'src/TParticleBeam.cc',
                                 'src/TParticleBeamContainer.cc',
                                 'src/TParticleTrajectoryPoints.cc',
                                 'src/TRandomA.cc',
                                 'src/TSpectrumContainer.cc',
                                 'src/TSurfaceOfPoints.cc',
                                 'src/TSurfacePoint.cc',
                                 'src/TSurfacePoints_3D.cc',
                                 'src/TSurfacePoints_Rectangle.cc',
                                 'src/TVector2D.cc',
                                 'src/TVector3D.cc',
                                 'src/TVector3DC.cc',
                                 'src/TVector4D.cc',
                                 'src/TOMATH.cc'],
                      extra_compile_args=['-DCUDA', '-std=c++11', '-Wno-write-strings', '-Wall', '-O3', '-pedantic', '-fPIC', '-pthread'],
                      libraries = ['cuda', 'cudart'],
                      library_dirs = ['/usr/local/cuda/lib64', '/lib64', '/usr/lib64', '/usr/local/cuda/lib'],
                      extra_objects = ['lib/OSCARSSR_Cuda.o']
                     )


moduleOSCARSTH = Extension('oscars.th',
                      include_dirs = ['include'],
                      sources = ['src/OSCARSTH.cc',
                                 'src/OSCARSTH_Python.cc',
                                 'src/T3DScalarContainer.cc',
                                 'src/TField3D_Grid.cc',
                                 'src/TField3D_Gaussian.cc',
                                 'src/TFieldContainer.cc',
                                 'src/TField3D_IdealUndulator.cc',
                                 'src/TField3D_UniformBox.cc',
                                 'src/TFieldPythonFunction.cc',
                                 'src/TParticleA.cc',
                                 'src/TParticleBeam.cc',
                                 'src/TParticleBeamContainer.cc',
                                 'src/TParticleTrajectoryPoints.cc',
                                 'src/TRandomA.cc',
                                 'src/TSpectrumContainer.cc',
                                 'src/TSurfaceOfPoints.cc',
                                 'src/TSurfacePoint.cc',
                                 'src/TSurfacePoints_3D.cc',
                                 'src/TSurfacePoints_Rectangle.cc',
                                 'src/TVector2D.cc',
                                 'src/TVector3D.cc',
                                 'src/TVector3DC.cc',
                                 'src/TVector4D.cc',
                                 'src/TOMATH.cc'],
                      extra_compile_args=['-DCUDA', '-std=c++11', '-Wno-write-strings', '-Wall', '-O3', '-pedantic', '-fPIC', '-pthread'],
                      #libraries = ['cuda', 'cudart'],
                      #library_dirs = ['/usr/local/cuda/lib64', '/lib64', '/usr/lib64', '/usr/local/cuda/lib'],
                      #extra_objects = ['']
                     )




setup(
  name="oscars",
  version="1.36.08",
  description = 'Open Source Code for Advanced Radiation Simulation',
  author = 'Dean Andrew Hidas',
  author_email = 'dhidas@bnl.gov',
  url = 'http://oscars.bnl.gov/',
  license = 'LICENSE.txt',
  long_description = '''The OSCARS Package.''',
  ext_modules = [moduleOSCARSSR, moduleOSCARSTH],
  data_files=[('oscars', ['LICENSE.txt', 'COPYRIGHT.txt'])],
  package_data = {'' : ['LICENSE.txt']},
  package_dir = {'oscars': 'oscars'},
  py_modules = ['oscars.plots_mpl', 'oscars.plots3d_mpl', 'oscars.parametric_surfaces']
)
